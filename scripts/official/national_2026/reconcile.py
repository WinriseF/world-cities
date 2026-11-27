"""Join official cities by name, province and, where available, the official polygon."""

from national import ROOT, norm, rosters
import json
import re
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
import gzip, math, tarfile
from shapely.geometry import Point


def strip_label(cc, name):
    if cc == "RO":
        return re.sub(r"^(?:Municipiul|Oraşul|Orașul) +", "", name, flags=re.I)
    if cc == "HR":
        return re.sub(r"^Grad\s+", "", name, flags=re.I)
    if cc == "KR":
        return re.sub(r"-si$", "", name, flags=re.I)
    return name


def key(cc, name):
    return norm(strip_label(cc, name))


def distance(a, b):
    return 111.2 * math.hypot(
        (a[0] - b[0]) * math.cos(math.radians((a[1] + b[1]) / 2)), a[1] - b[1]
    )


import os
import sys
from pypdf import PdfReader

os.chdir(Path(sys.argv[1]).resolve())
for stem, suffix in [("fi-guide", ".pdf"), ("si-cities", ".pdf"), ("sk", ".raw")]:
    text = "\n".join(
        p.extract_text(extraction_mode="layout") for p in PdfReader(stem + suffix).pages
    )
    Path(stem + ".txt").write_text(text)
with tarfile.open(ROOT / "artifacts/winrisef-world-cities-0.1.6.tgz") as t:
    load = lambda p: json.load(t.extractfile("package/data/" + p + ".json"))
    region = {r["id"]: load("regions/" + r["id"]) for r in load("countries")}
    old = {cc: load("cities/" + cc) for cc in region}
states = {r["id"]: r for lst in region.values() for r in lst}
statecodes = {r["code"]: r for r in states.values() if r["code"]}
gnstate = {}
name_to_state = {
    cc: {norm(r["en"]): r["code"] for r in regs} for cc, regs in region.items()
}
gnfix = {
    "hrcountyofosijekbaranja": "HR-14",
    "hrvukovarsrijem": "HR-16",
    "hrzagrebcounty": "HR-01",
    "hrzagreb": "HR-21",
    "bgsofiacapital": "BG-22",
    "roarges": "RO-AG",
    "robucuresti": "RO-B",
    "robucurestimunicipality": "RO-B",
}
for line in Path("admin.raw").read_text().splitlines():
    ident, nm, _, _ = line.split("\t")
    cc = ident.split(".")[0]
    n = norm(re.sub(r" (Region|County|Province|Division)$", "", nm))
    gnstate[ident] = gnfix.get(cc.lower() + norm(nm), name_to_state.get(cc, {}).get(n))
for ident, name, *_ in (
    l.split("\t")
    for l in Path("admin.raw").read_text().splitlines()
    if l.startswith(("UY.", "SI."))
):
    cc = ident[:2]
    gnstate[ident] = name_to_state[cc].get(
        norm(
            name.removeprefix("Municipality of ")
            .removeprefix("City Municipality of ")
            .removesuffix(" Department")
            .removesuffix(" Municipality")
        )
    )
gnstate["BW.13"] = "BW-FR"
gnstate["GE.71"] = "GE-SZ"
for ident, name, *_ in (
    l.split("\t")
    for l in Path("admin.raw").read_text().splitlines()
    if l.startswith("HU.")
):
    gnstate[ident] = next(
        (
            r["code"]
            for r in region["HU"]
            if norm(r["en"].removesuffix(" County"))
            == norm(name.removesuffix(" County"))
        ),
        None,
    )
gnstate.update(
    {
        "FI.11": "FI-15",
        "FI.02": "FI-19",
        "FI.10": "FI-04",
        "FI.17": "FI-14",
        "FI.14": "FI-03",
        "FI.05": "FI-06",
        "FI.07": "FI-16",
    }
)
gnstate["HU.23"] = "HU-VE"
gnstate.update(
    {
        "KR.06": "KR-42",
        "KR.13": "KR-41",
        "KR.17": "KR-44",
        "KR.05": "KR-43",
        "KR.03": "KR-45",
        "KR.14": "KR-47",
        "KR.20": "KR-48",
        "KR.01": "KR-49",
    }
)
rawstates = {
    r["id"]: r for r in json.loads((ROOT / ".cache/csc/regions.json").read_bytes())
}


def parent(raw):
    st = rawstates.get(raw["state_id"])
    while st and str(st.get("level")) != "1":
        st = rawstates.get(int(st["parent_id"] or 0))
    return st and st["iso3166_2"]


from additional_national import extend

countries = rosters(region)
extend(countries)
raw_by = defaultdict(list)
for row in json.load(gzip.open(ROOT / ".cache/csc/cities.json.gz")):
    cc = row["country_code"]
    if cc in countries:
        raw_by[cc].append(row)
wiki = {
    **json.load(gzip.open(ROOT / "sources/wikidata-city-status.json.gz")),
    **json.loads((ROOT / "sources/wikidata-names.json").read_bytes()),
}


def add_index(index, cc, rec, names):
    for k in {key(cc, n) for n in names if n}:
        index[k].append(rec)


def choose(cc, spec, options):
    candidates = {a["id"]: a for a in options}
    geom = spec["geom"]
    state = spec["state"]
    valid = [
        r
        for r in candidates.values()
        if r["state"] == state
        or (
            cc == "HU"
            and r["state"]
            and norm(statecodes[r["state"]]["en"]) == norm(spec["name"])
        )
        or (geom is not None and geom.covers(Point(r["xy"])))
    ]
    if geom is not None:
        inside = [r for r in valid if geom.covers(Point(r["xy"]))]
        if inside:
            valid = inside
        else:
            valid = [r for r in valid if geom.distance(Point(r["xy"])) < 0.025]
    if not valid:
        return None
    rank = lambda x: (x.get("priority", 0), x.get("pop", 0))
    valid.sort(key=rank, reverse=True)
    if len(valid) > 1 and any(distance(valid[0]["xy"], v["xy"]) > 4 for v in valid[1:]):
        return None
    return valid[0]


FILE = {
    "CZ": "geo",
    "CA": "cageo",
    "SK": "skgeo",
    "RO": "rogeo",
    "HR": "hrgeo",
    "BG": "bggeo",
    "KR": "krgeo",
    "LK": "lkg",
    **{
        c: c + "geo"
        for c in [
            "BD",
            "UG",
            "NZ",
            "KE",
            "GE",
            "UY",
            "HU",
            "FI",
            "IE",
            "EE",
            "SI",
            "ZA",
            "BW",
            "NP",
            "IN",
        ]
    },
}


def make_country(cc, specs):
    oldindex = defaultdict(list)
    rawindex = defaultdict(list)
    gindex = defaultdict(list)
    geo_by_id = {}
    existing_by_id = {r["id"]: r for r in old[cc]}
    for r in old[cc]:
        add_index(
            oldindex,
            cc,
            dict(
                id=r["id"],
                state=states.get(r["region"], {}).get("code"),
                xy=(r["lon"], r["lat"]),
                record=r,
            ),
            [r["en"], *(r.get("aliases") or [])],
        )
    for r in raw_by[cc]:
        if r["latitude"] is None or r["longitude"] is None:
            continue
        tr = r["translations"] or {}
        existing = existing_by_id.get("csc:" + str(r["id"]))
        if existing:
            add_index(
                oldindex,
                cc,
                dict(
                    id=existing["id"],
                    state=states.get(existing["region"], {}).get("code"),
                    xy=(existing["lon"], existing["lat"]),
                    record=existing,
                ),
                [r["name"], r["native"], tr.get("en")],
            )
        add_index(
            rawindex,
            cc,
            dict(
                id="csc:" + str(r["id"]),
                state=parent(r),
                xy=(float(r["longitude"]), float(r["latitude"])),
                name=r["name"],
                zh=tr.get("zh-CN") or tr.get("zh") or wiki.get(r["wikiDataId"]),
            ),
            [r["name"], r["native"], tr.get("en")],
        )
    langs = defaultdict(list)
    with ZipFile(cc + "-alts.raw") as z:
        for line in z.open(cc + ".txt"):
            f = line.decode().rstrip("\r\n").split("\t")
            if f[2] in ("zh", "zh-CN", "zh-Hans", "zh-TW", "zh-Hant") and re.search(
                r"[\u3400-\u9fff]", f[3]
            ):
                langs[f[1]].append(
                    (f[2] not in ("zh-CN", "zh-Hans"), f[2] != "zh", f[4] != "1", f[3])
                )
    with ZipFile(FILE[cc] + ".raw") as z:
        for line in z.open(cc + ".txt"):
            f = line.decode().rstrip("\r\n").split("\t")
            if f[6] != "P" or (
                f[0] != "728978"
                and f[7]
                not in (
                    "PPL",
                    "PPLA",
                    "PPLA2",
                    "PPLA3",
                    "PPLA4",
                    "PPLC",
                    "PPLG",
                    "PPLA5",
                )
            ):
                continue
            rec = dict(
                id=f[0],
                name=f[1],
                state=gnstate.get(cc + "." + f[10]),
                xy=(float(f[5]), float(f[4])),
                priority=int(f[7] != "PPL"),
                pop=int(f[14] or 0),
                zh=min(langs[f[0]])[-1] if langs[f[0]] else None,
            )
            add_index(
                gindex,
                cc,
                rec,
                [
                    f[1],
                    f[2],
                    *(f[3].split(",") if cc == "IN" and f[10] == "13" else []),
                ],
            )
            geo_by_id[f[0]] = rec
    updates = []
    missing = []
    used = set()
    evidence[cc] = []
    alias_by_name = {
        "NP": {"Birgunj": ["Birgañj", "Birganj"]},
        "KR": {"Dangjin": ["Tangjin"]},
        "GE": {
            "Zestaponi": ["Zestafoni"],
            "Tqibuli": ["Tkibuli"],
            "Tsqaltubo": ["Tskaltubo"],
            "Dedoplistsqaro": ["Dedoplistskaro", "Dedop’listsq’aro"],
            "Tetritsqaro": ["Tetritskaro", "Tetrits’q’aro"],
            "Sighnagi": ["Sighnaghi"],
        },
        "CZ": {"Praha": ["Prague"], "Plzeň": ["Pilsen"]},
        "BG": {"Galabovo": ["Gŭlŭbovo"], "Veliko Tarnovo": ["Veliko Tŭrnovo"]},
        "RO": {"București": ["Bucharest"], "Roșiori De Vede": ["Roșiorii de Vede"]},
        "BD": {
            "Barishal": ["Barisal"],
            "Cumilla": ["Comilla"],
            "Chattogram": ["Chittagong"],
        },
        "LK": {
            "Akkaraipattu": ["Akkaraipattu", "Akkaripattu"],
            "Dehiwala-Mount Lavinia": ["Dehiwala-Mount Lavinia", "Mount Lavinia"],
            "Sri Jayewardenepura Kotte": ["Sri Jayawardenepura Kotte"],
        },
    }
    for spec in specs:
        spec["aliases"].extend(alias_by_name.get(cc, {}).get(spec["name"], []))
        state = spec["state"]
        name = spec["name"]
        geom = spec["geom"]
        keys = {key(cc, n) for n in [name, *spec["aliases"]]}
        look = lambda idx: choose(cc, spec, [x for k in keys for x in idx[k]])
        prev = look(oldindex)
        raw = look(rawindex)
        g = look(gindex)
        # Same-name settlements in the same province: use the seat and district identifiers.
        geoid = {
            ("RO", "Liteni"): "674697",
            ("BG", "Kostenets"): "730093",
            ("UY", "Ciudad del Plata"): "10098634",
        }.get((cc, name))
        if geoid:
            g = next(q for k in keys for q in gindex[k] if q["id"] == geoid)
            if prev and distance(g["xy"], prev["xy"]) > 4:
                prev = None
            if raw and distance(g["xy"], raw["xy"]) > 4:
                raw = None
        if (
            cc == "KR"
            and name == "Gyeryong"
            and prev
            and g
            and distance(g["xy"], prev["xy"]) > 15
        ):
            g = None
        if spec.get("pointGid"):
            g = {**geo_by_id[spec["pointGid"]], "zh": None}
            assert g["state"] == state
        if not (prev or raw or g or (geom is not None and not geom.is_empty)):
            missing.append([state, name])
            continue
        # The geometry validates the point independently. Prefer the existing point when valid.
        candidates = [
            q["xy"]
            for q in (
                [g, prev, raw] if cc == "FI" and name == "Kokkola" else [prev, g, raw]
            )
            if q
        ]
        if geom is not None:
            candidates = [pt for pt in candidates if geom.covers(Point(pt))]
        if candidates:
            xy = candidates[0]
        else:
            p = geom.representative_point()
            xy = (p.x, p.y)
        if cc == "SK" and not any(
            x
            and key(cc, x.get("name") or x.get("record", {}).get("en", ""))
            == key(cc, name)
            for x in [prev, raw, g]
        ):
            raise ValueError(name)
        if prev:
            id = prev["id"]
        elif raw and raw["id"] not in {r["id"] for r in old[cc]}:
            id = raw["id"]
        elif spec["key"]:
            id = cc.lower() + ":" + spec["key"]
        elif spec.get("pointGid"):
            id = cc.lower() + ":" + norm(name)
        elif spec.get("fallbackId"):
            id = spec["fallbackId"]
        elif g:
            id = "gn:" + g["id"]
        else:
            missing.append([state, name])
            continue
        if id in used:
            missing.append([state, name, "entity collision " + id])
            continue
        used.add(id)
        prior = prev["record"] if prev else {}
        if cc == "SK":
            name = next(
                (
                    v
                    for v in [
                        prior.get("en"),
                        (g or {}).get("name"),
                        (raw or {}).get("name"),
                    ]
                    if v and key(cc, v) == key(cc, name)
                ),
                name,
            )
        en = prior.get("en") or name
        if (cc == "HR" and en.startswith("Grad ")) or cc in ("FI", "UY"):
            en = name
        chinese = prior.get("zh") or (raw or {}).get("zh") or (g or {}).get("zh")
        if not isinstance(chinese, str) or not re.search(r"[\u3400-\u9fff]", chinese):
            chinese = None
        aliases = sorted(
            {
                s
                for s in [
                    name,
                    *spec["aliases"],
                    prior.get("en"),
                    *prior.get("aliases", []),
                ]
                if s and s not in (en, chinese)
            }
        )
        record = dict(
            id=id,
            region=statecodes[state]["id"] if state else None,
            en=en,
            zh=chinese,
            lat=xy[1],
            lon=xy[0],
            kind=prior.get("kind", "city"),
        )
        if spec["key"]:
            record["officialId"] = spec["key"]
        if aliases:
            record["aliases"] = aliases
        updates.append(record)
        evidence[cc].append(
            dict(
                name=spec["name"],
                city=id,
                province=state,
                officialCodes=spec.get("partCodes")
                or ([spec["key"]] if spec["key"] else []),
                geoNames=g and g["id"],
                previous=prior.get("id"),
                pointSource=next(
                    (
                        label
                        for label, ref in [
                            ("previous", prev),
                            ("GeoNames", g),
                            ("CSC", raw),
                        ]
                        if ref and ref["xy"] == xy
                    ),
                    "reference-polygon",
                ),
            )
        )
    print(
        cc,
        len(specs),
        "matched",
        len(updates),
        "new",
        len(used - {r["id"] for r in old[cc]}),
        "missing",
        missing[:50],
    )
    return updates, missing


evidence = {}
out = {}
issues = {}
for cc, spec in countries.items():
    out[cc], issues[cc] = make_country(cc, spec)
Path("joined.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
Path("matches.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=1))
Path("issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1))
