"""Additional verified national classifications and cross-referenced boundary sources."""

import json, re
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
from shapely.geometry import shape
from national import item, norm


def extend(rows):
    # Botswana: city councils expressly listed in the national directory.
    for name, code in [("Francistown", "FR"), ("Gaborone", "GA")]:
        rows["BW"].append(item("BW", "BW-" + code, name))
    # State government distinguishes corporations and municipalities from all other bodies.
    official = BeautifulSoup(Path("inkl.raw").read_bytes(), "html.parser")
    from zipfile import ZipFile

    with ZipFile("in-geom.zip") as z:
        local = json.load(z.open("Kerala_localbody_boundaries.geojson"))["features"]
    polygons = {
        (f["properties"]["DistName"].lower(), norm(f["properties"]["name"])): f
        for f in local
        if f["properties"]["Lsgd_Type"] in ("Municipality", "Corporation")
    }
    spelling = {
        "Vatakara": "Vadakara",
        "Paravur": "North Paravur",
        "Paravoor": "Paravur",
        "Thrippunithura": "Tripunithura",
        "Taliparamba": "Thaliparamba",
        "Palai": "Pala",
        "Chittur-Thathamangalam": "Chittoor Thathamangalam",
        "Shoranur": "Shornur",
        "Chalakudy": "Chalakkudy",
        "Guruvayoor": "Guruvayur",
    }
    for tr in official.select("tr"):
        r = [c.get_text(" ", strip=True) for c in tr.select("td")]
        if len(r) >= 4 and r[-2] in ("Municipality", "Municipal Corporation"):
            name = r[1].strip().title()
            boundary = polygons.pop(
                (
                    r[-1].lower().replace("kozhikkode", "kozhikode"),
                    norm(spelling.get(name, name)),
                )
            )
            feature = boundary["properties"]
            city = item(
                "IN",
                "IN-KL",
                name,
                feature["lb_code"],
                geom=shape(boundary["geometry"]),
                aliases=[feature["name"]],
            )
            if name == "Paravur" and r[-1] == "Ernakulam":
                city["name"] = "North Paravur"
                city["aliases"].append("Paravur")
            if name == "Paravoor" and r[-1] == "Kollam":
                city["aliases"].append("Paravur")
            city["districtName"] = r[-1]
            rows["IN"].append(city)
    assert not polygons and len(rows["IN"]) == 93
    # Nepal's current census site lists both official romanized spellings and spelling variants.
    s = BeautifulSoup(Path("np-census.raw").read_bytes(), "html.parser")
    census = json.loads(s.select_one("#__NEXT_DATA__").string)["props"]["pageProps"][
        "_nextI18Next"
    ]["initialI18nStore"]["en"]["common"]
    ends = {
        "Nagarpalika": r" (?:Municipality|Nagarpalika)$",
        "Upamahanagarpalika": r" Sub[- ]Metropolit(?:ian|an) City$",
        "Mahanagarpalika": r" Metropolit(?:ian|an) City$",
    }
    official = {}
    for kind, suffix in ends.items():
        for title in census:
            if re.search(suffix, title, re.I) and "rural" not in title.lower():
                name = re.sub(suffix, "", title, flags=re.I)
                official[kind, norm(name)] = name
    aliases = dict(
        line.strip().split(" | ")
        for line in Path(__file__)
        .with_name("np-spellings.txt")
        .read_text()
        .splitlines()
        if line.strip()
    )
    geography = defaultdict(list)
    for f in json.loads(Path("np-geo.json").read_bytes())["features"]:
        p = f["properties"]
        kind = p["Type_GN"]
        if kind not in ends:
            continue
        key = (p["STATE_CODE"], p["DISTRICT"], kind, p["GaPa_NaPa"])
        geography[key].append(shape(f["geometry"]))
    from shapely.ops import unary_union

    for (province, district, kind, local), polys in geography.items():
        spelling = aliases.get(local, local)
        if local == "Mahakali" and district == "KANCHANPUR":
            spelling = "Dodhara Chandani"
        official_name = official.get((kind, norm(spelling)))
        if not official_name:
            raise ValueError((district, kind, spelling))
        r = item(
            "NP",
            "NP-P" + str(province),
            official_name,
            geom=unary_union(polys),
            aliases=[local] if local != official_name else [],
        )
        r["fallbackId"] = "np:" + norm(district) + "-" + norm(official_name)
        r["districtName"] = district
        rows["NP"].append(r)
    assert len(rows["NP"]) == 293
