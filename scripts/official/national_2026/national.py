"""Read dated official enumeration files. Coordinate matching is a separate step."""

import csv
import io
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
import xlrd
from bs4 import BeautifulSoup
from shapely import make_valid, union_all
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[3]


def norm(s):
    return "".join(
        c for c in unicodedata.normalize("NFKD", (s or "").casefold()) if c.isalnum()
    )


def csv_zip(name):
    with ZipFile(name + ".raw") as z:
        return list(
            csv.DictReader(
                io.StringIO(z.read(z.namelist()[0]).decode("cp1250")), delimiter=";"
            )
        )


def item(cc, state, name, key=None, *, geom=None, aliases=()):
    # Rounded ESRI exports can contain touching rings or encode multiple shells in one polygon.
    if geom is not None and not geom.is_valid:
        geom = make_valid(geom)
        if geom.geom_type == "GeometryCollection":
            geom = union_all([part for part in geom.geoms if part.geom_type in ("Polygon", "MultiPolygon")])
        assert not geom.is_empty and geom.area > 0
    return dict(
        cc=cc, state=state, name=name, key=key, geom=geom, aliases=list(aliases)
    )


def rosters(regions):
    rows = defaultdict(list)
    states = {
        cc: {norm(r["en"]): r["code"] for r in regs} for cc, regs in regions.items()
    }
    # RÚIAN municipal status, district and province; independent geometry by identical municipal code.
    statuses = {r["KOD"]: r["NAZEV"] for r in csv_zip("stat")}
    districts = {r["KOD"]: r["VUSC_KOD"] for r in csv_zip("okres") if not r["PLATI_DO"]}
    kraje = {
        r["KOD"]: "CZ-" + r["NUTS_LAU"][-2:]
        for r in csv_zip("regions")
        if not r["PLATI_DO"]
    }
    geo = json.loads(Path("cz-polys.raw").read_bytes())
    shapes = {str(f["properties"]["kod"]): f for f in geo["features"]}
    for r in csv_zip("cz"):
        if r["PLATI_DO"] or statuses[r["STATUS_KOD"]] not in {
            "Město",
            "Statutární město",
            "Hlavní město",
        }:
            continue
        f = shapes.pop(r["KOD"])
        assert (
            f["properties"]["nazev"] == r["NAZEV"]
            and str(f["properties"]["statuskod"]) == r["STATUS_KOD"]
        )
        rows["CZ"].append(
            item(
                "CZ",
                kraje[districts[r["OKRES_KOD"]]],
                r["NAZEV"],
                r["KOD"],
                geom=shape(f["geometry"]),
            )
        )
    assert not shapes and len(rows["CZ"]) == 610
    # Canada: current census subdivision types for City / Cité / Ville.
    provinces = dict(
        zip(
            "10 11 12 13 24 35 46 47 48 59 60 61 62".split(),
            "NL PE NS NB QC ON MB SK AB BC YT NT NU".split(),
        )
    )
    ca = json.loads(Path("ca-polys.raw").read_bytes())
    assert not ca.get("exceededTransferLimit")
    for f in ca["features"]:
        r = f["properties"]
        assert r["CSDTYPE"] in ("C", "CY", "CV", "V")
        city = r["CSDENAME"] or r["CSDNAME"]
        rows["CA"].append(
            item(
                "CA",
                "CA-" + provinces[r["PRUID"]],
                city,
                r["CSDUID"],
                geom=shape(f["geometry"]),
                aliases=[r["CSDFNAME"]] if r["CSDFNAME"] else [],
            )
        )
    # Spans two provinces. The two census parts describe one city.
    from shapely.geometry import Point

    with ZipFile("cageo.raw") as z:
        seats = [
            line.split("\t")
            for line in z.read("CA.txt").decode().splitlines()
            if line.split("\t", 2)[1] in ("Lloydminster", "Flin Flon")
        ]
    for nm in ("Lloydminster", "Flin Flon"):
        parts = [r for r in rows["CA"] if r["name"] == nm + " (Part)"]
        assert len(parts) == 2
        for r in parts:
            rows["CA"].remove(r)
        seat = next(
            q for q in seats if q[1] == nm and q[6] == "P" and q[7] in ("PPL", "PPLA2")
        )
        point = Point(float(seat[5]), float(seat[4]))
        r = min(parts, key=lambda part: part["geom"].distance(point))
        combined = item(
            "CA",
            r["state"],
            nm,
            r["key"],
            geom=parts[0]["geom"].union(parts[1]["geom"]),
        )
        combined["partCodes"] = sorted(p["key"] for p in parts)
        rows["CA"].append(combined)
    # Croatia. The Roman county number in the ministry spreadsheet is the ISO suffix.
    roman = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI".split()
    sh = xlrd.open_workbook("hr2.raw").sheet_by_index(0)
    for i in range(1, sh.nrows):
        county, kind, name = sh.row_values(i)
        if kind.strip() == "Grad":
            rows["HR"].append(
                item(
                    "HR", "HR-%02d" % (roman.index(county.split()[0]) + 1), name.strip()
                )
            )
    assert len(rows["HR"]) == 128
    # Slovak Interior Ministry list of 140, followed by Nesvady's 2020 promotion.
    skstates = "BL TA TC NI ZI BC PV KI".split()
    for line in Path("sk.txt").read_text().splitlines():
        m = re.match(r"^(\d+)\.\s+(.+)", line.strip())
        if not m:
            continue
        text = m[2].strip()
        if "kraj" in text:
            state = "SK-" + skstates[int(m[1]) - 1]
            continue
        name = re.split(r"\s+\d+\s*$", text)[0].strip()
        if norm(name).startswith("hlavnemestoslovenskejrepubliky"):
            name = "Bratislava"
        if norm(name) == "mestokosice":
            name = "Košice"
        if norm(name) == "banovcenadbeberavou":
            name = "Bánovce nad Bebravou"
        rows["SK"].append(item("SK", state, name))
    assert len(rows["SK"]) == 140
    rows["SK"].append(item("SK", "SK-NI", "Nesvady"))
    # Romania. Level 2 with urban UAT type; never the component settlements or sectors.
    ro = list(
        csv.DictReader(
            Path("roreg.raw").read_text(encoding="utf-8-sig").splitlines(),
            delimiter=";",
        )
    )
    counties = {
        r["SIRUTA"]: r["DENLOC"].replace("JUDEŢUL ", "").replace("JUDEȚUL ", "")
        for r in ro
        if r["NIV"] == "1"
    }
    ro_states = {
        **states["RO"],
        "municipiulbucuresti": "RO-B",
        "caras­severin".replace("­", ""): "RO-CS",
    }
    for r in ro:
        if r["NIV"] != "2" or r["TIP"] not in {"1", "2", "4", "9"}:
            continue
        name = (
            re.sub(r"^(MUNICIPIUL|ORAŞ|ORAȘ|ORAŞUL|ORAȘUL)\s+", "", r["DENLOC"])
            .translate(str.maketrans("ŞŢ", "ȘȚ"))
            .title()
        )
        rows["RO"].append(
            item("RO", ro_states[norm(counties[r["SIRSUP"]])], name, r["SIRUTA"])
        )
    # Bulgaria. EKATTE explicitly distinguishes grad (гр.) from selo (с.).
    with ZipFile("bg2025.raw") as z:
        read = lambda key: json.loads(
            z.read(
                next(n for n in z.namelist() if n.lower().endswith(key + ".json"))
            ).decode("utf-8-sig")
        )
        oblast = {r["oblast"]: r["name_en"] for r in read("ek_obl") if "oblast" in r}
        for r in read("ek_atte"):
            if r.get("t_v_m") != "гр.":
                continue
            ob = r["oblast"]
            state = {"SOF": "BG-22", "SFO": "BG-23"}.get(ob) or states["BG"][
                norm(oblast[ob])
            ]
            rows["BG"].append(
                item("BG", state, r["name_en"], r["ekatte"], aliases=[r["name"]])
            )
    # These official subnational and national rosters are scoped to specified legal classes.
    provinces = {
        "gyeonggi": "41",
        "gangwon": "42",
        "chungbuk": "43",
        "chungnam": "44",
        "jeonbuk": "45",
        "gyeongbuk": "47",
        "gyeongnam": "48",
        "jeju": "49",
    }
    kr = BeautifulSoup(Path("kr.raw").read_bytes(), "html.parser")
    for slug, iso in provinces.items():
        block = kr.find("div", id=slug)
        for a in block.select("ul.area-list a"):
            label = a.get_text(" ", strip=True)
            if re.search(r"-si(?:$| \()", label):
                rows["KR"].append(item("KR", "KR-" + iso, label.split("-si")[0]))
    # March 2025 election gazette, February municipal-council schedule, and Kalmunai (EC).
    lk = {
        "1": [
            "Colombo",
            "Dehiwala-Mount Lavinia",
            "Sri Jayewardenepura Kotte",
            "Moratuwa",
            "Kaduwela",
            "Gampaha",
            "Negombo",
            "Kalutara",
        ],
        "2": ["Kandy", "Matale", "Dambulla", "Nuwara Eliya"],
        "3": ["Galle", "Matara", "Hambantota", "Tangalle"],
        "4": ["Jaffna", "Vavuniya"],
        "5": ["Akkaraipattu", "Batticaloa", "Trincomalee", "Kalmunai"],
        "6": ["Kurunegala", "Puttalam"],
        "7": ["Anuradhapura", "Polonnaruwa"],
        "8": ["Badulla", "Bandarawela"],
        "9": ["Kegalle", "Ratnapura"],
    }
    for s, names in lk.items():
        for n in names:
            rows["LK"].append(item("LK", "LK-" + s, n))
    # Twelve Bangladesh city corporations include the two halves of Dhaka.
    bd = {
        "A": ["Barishal"],
        "B": ["Chattogram", "Cumilla"],
        "C": ["Dhaka", "Gazipur", "Narayanganj"],
        "D": ["Khulna"],
        "E": ["Rajshahi"],
        "F": ["Rangpur"],
        "G": ["Sylhet"],
        "H": ["Mymensingh"],
    }
    for s, names in bd.items():
        for n in names:
            rows["BD"].append(item("BD", "BD-" + s, n))
    # Ten operational charter cities (UCMID) and the capital. City districts are separate from surrounding districts.
    for n in [
        "Jinja",
        "Mbarara",
        "Gulu",
        "Arua",
        "Hoima",
        "Mbale",
        "Soroti",
        "Lira",
        "Masaka",
        "Fort Portal",
        "Kampala",
    ]:
        rows["UG"].append(item("UG", "UG-102" if n == "Kampala" else None, n))
    for n, s in [
        ("Eldoret", "44"),
        ("Kisumu", "17"),
        ("Mombasa", "28"),
        ("Nairobi", "30"),
        ("Nakuru", "31"),
    ]:
        rows["KE"].append(item("KE", "KE-" + s, n))
    # Stats NZ's twelve councils explicitly named City, plus Auckland Council.
    nz = {
        "Hamilton": "WKO",
        "Tauranga": "BOP",
        "Napier": "HKB",
        "Palmerston North": "MWT",
        "Lower Hutt": "WGN",
        "Upper Hutt": "WGN",
        "Wellington": "WGN",
        "Porirua": "WGN",
        "Nelson": "NSN",
        "Christchurch": "CAN",
        "Dunedin": "OTA",
        "Invercargill": "STL",
        "Auckland": "AUK",
    }
    for f in json.loads(Path("nz.raw").read_bytes())["features"]:
        a = f["attributes"]
        label = a["TA2026_V1_00_NAME"]
        if label.endswith(" City") or label == "Auckland":
            name = label.removesuffix(" City")
            rows["NZ"].append(
                item("NZ", "NZ-" + nz[name], name, a["TA2026_V1_00"], aliases=[label])
            )
    import openpyxl

    province = "GE-TB"
    for row in openpyxl.load_workbook("GE.xlsx", read_only=True).active.values:
        label = str(row[0] or "").strip()
        province = states["GE"].get(norm(label.replace(" A.R.", "")), province)
        if (
            re.match(r"^C\. ", label, re.I)
            and isinstance(row[-3], (float, int))
            and row[-3] > 0
        ):
            name = label[3:].removesuffix(" Municipality").strip("* ").capitalize()
            rows["GE"].append(item("GE", province, name))
    hu_counties = {
        norm(r["en"].removesuffix(" County")): r["code"] for r in regions["HU"]
    }
    hu_counties["csongradcsanad"] = "HU-CS"
    for row in openpyxl.load_workbook("HU26.xlsx", read_only=True).active.values:
        name, code, status, county = row[:4]
        if (status or "").strip() not in {
            "város",
            "megyei jogú város",
            "megyeszékhely, megyei jogú város",
            "főváros",
        }:
            continue
        province = hu_counties[norm(county)] if county else "HU-BU"
        if "megyei jogú város" in status:
            province = states["HU"].get(norm(name), province)
        rows["HU"].append(item("HU", province, name, code))
    assert len(rows["HU"]) == 348
    # Estonia. Tallinn and Kohtla-Järve have city districts in the settlement layer.
    import shapefile
    from pyproj import Transformer
    from shapely.ops import transform

    projected = Transformer.from_crs(3301, 4326, always_xy=True).transform
    estonian = {}
    for filename, prefix in [("ee-municipalities", "O"), ("ee-settlements", "A")]:
        with ZipFile(filename + ".zip") as z:
            member = lambda ext: io.BytesIO(
                z.read(next(n for n in z.namelist() if n.endswith(ext)))
            )
            reader = shapefile.Reader(
                shp=member(".shp"),
                shx=member(".shx"),
                dbf=member(".dbf"),
                encoding="cp1257",
            )
            for i, row in enumerate(reader.iterRecords()):
                if row.TYYP not in {"4", "5"}:
                    continue
                name = row[prefix + "NIMI"].removesuffix(" linn")
                state = "EE-" + row.MKOOD[-2:]
                estonian[state, name] = item(
                    "EE",
                    state,
                    name,
                    row[prefix + "KOOD"],
                    geom=transform(projected, shape(reader.shape(i).__geo_interface__)),
                )
    rows["EE"] = list(estonian.values())
    assert len(rows["EE"]) == 47
    # The ministry PDF enumerates city status, independently of the status of the council.
    si_text = Path("si-cities.txt").read_text().split("Sklep Državnega")[0]
    capitals = {
        "Višnja Gora": "Ivančna Gorica",
        "Šempeter pri Gorici": "Šempeter–Vrtojba",
        "Lenart v Slovenskih goricah": "Lenart",
    }
    for line in si_text.splitlines():
        for m in re.finditer(r"\b\d+\.\s+([^\d]+?)(?=\s+\d+\.|$)", line):
            name = m[1].strip()
            rows["SI"].append(
                item("SI", states["SI"][norm(capitals.get(name, name))], name)
            )
    assert len(rows["SI"]) == 69
    # Finland's own UNGEGN country submission, with municipal self-designations checked on six council sites.
    guide = (
        Path("fi-guide.txt")
        .read_text()
        .split("List 1. The municipalities of Finland (in 2025)")[-1]
        .split("Äänekoski* Fi 13")[0]
        + "Äänekoski* Fi 13"
    )
    cities = {
        re.split(r" – | - ", col.split("*")[0])[0]
        for line in guide.splitlines()
        for col in re.split(r"\s{2,}", line.strip())
        if "*" in col
    }
    cities.update(["Akaa", "Kaarina", "Kangasala", "Kuusamo", "Laitila", "Lieto"])
    assert len(cities) == 108
    iso = dict(
        zip(
            "01 02 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 21".split(),
            "18 19 17 06 11 16 09 02 04 15 13 08 03 12 07 14 05 10 01".split(),
        )
    )
    for fin, code, swe, eng, province, *_ in openpyxl.load_workbook(
        "fi-regions.xlsx", read_only=True
    ).active.values:
        if not fin or not code:
            continue
        finnish = fin.split(" - ")[0]
        if finnish not in cities:
            continue
        cities.remove(finnish)
        if code == "478":
            continue  # Already belongs to the separate AX shard.
        city = item("FI", "FI-" + iso[province], eng, code, aliases=[finnish, swe])
        if eng == "Mänttä-Vilppula":
            city["pointGid"] = "646705"
        rows["FI"].append(city)
    assert not cities and len(rows["FI"]) == 107
    for name in ["Cork", "Dublin", "Galway", "Limerick", "Waterford"]:
        rows["IE"].append(item("IE", states["IE"][norm(name)], name))
    za = [
        ("East London", "Buffalo City", "EC"),
        ("Cape Town", "City of Cape Town", "WC"),
        ("Durban", "eThekwini", "KZN"),
        ("Johannesburg", "City of Johannesburg", "GP"),
        ("Bloemfontein", "Mangaung", "FS"),
        ("Gqeberha", "Nelson Mandela Bay", "EC"),
        ("Pretoria", "City of Tshwane", "GP"),
    ]
    for seat, authority, region in za:
        rows["ZA"].append(item("ZA", "ZA-" + region, seat, aliases=[authority]))
    metro = item(
        "ZA",
        "ZA-GP",
        "Ekurhuleni",
        aliases=["City of Ekurhuleni", "Ekurhuleni Metropolitan Municipality"],
    )
    metro["pointGid"] = "1002108"  # Germiston, the municipal seat.
    rows["ZA"].append(metro)
    # Uruguay's legal name changes and promotions, by named department.
    for name, state, aliases in [
        ("Ciudad del Carmen", "DU", ["Villa del Carmen"]),
        ("Rodríguez", "SJ", ["Villa Rodríguez"]),
        ("Ciudad del Plata", "SJ", []),
        ("Quebracho", "PA", []),
        ("Guichón", "PA", []),
    ]:
        rows["UY"].append(item("UY", "UY-" + state, name, aliases=aliases))
    mayo = item("UY", "UY-CA", "18 de Mayo")
    mayo["pointGid"] = "3480814"
    rows["UY"].append(mayo)
    capitals_uy = {
        "AR": "Artigas",
        "CA": "Canelones",
        "CL": "Melo",
        "CO": "Colonia del Sacramento",
        "DU": "Durazno",
        "FS": "Trinidad",
        "FD": "Florida",
        "LA": "Minas",
        "MA": "Maldonado",
        "MO": "Montevideo",
        "PA": "Paysandú",
        "RN": "Fray Bentos",
        "RV": "Rivera",
        "RO": "Rocha",
        "SA": "Salto",
        "SJ": "San José de Mayo",
        "SO": "Mercedes",
        "TA": "Tacuarembó",
        "TT": "Treinta y Tres",
    }
    for state, name in capitals_uy.items():
        rows["UY"].append(item("UY", "UY-" + state, name))
    return rows
