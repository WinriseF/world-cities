from pathlib import Path
import csv, hashlib, gzip, json
import sys
import tarfile

root = Path(__file__).resolve().parents[3]
raw = Path(sys.argv[1]).resolve()
review = root / "audit/2026-11-21"
cc_by = json.loads((raw / "joined.json").read_bytes())
evidence = json.loads((raw / "matches.json").read_bytes())
extras = json.loads((root / "sources/national-review-zh.json").read_bytes())
issues = json.loads((raw / "issues.json").read_bytes())
assert not any(issues.values())

with tarfile.open(root / "artifacts/winrisef-world-cities-0.1.6.tgz") as t:
    old_ax = json.load(t.extractfile("package/data/cities/AX.json"))[0]
ax = {k: v for k, v in old_ax.items() if k not in ("country", "pinyin")}
ax.update(officialId="478", aliases=["Maarianhamina"])
cc_by["AX"] = [ax]
evidence["AX"] = [
    dict(
        name="Mariehamn",
        city=ax["id"],
        province="AX",
        officialCodes=["478"],
        geoNames=None,
        previous=ax["id"],
        pointSource="previous",
    )
]
retired = {
    "CZ": {"csc:22971": "city district Praha 1"},
    "RO": {"csc:95445": "duplicate of csc:95163"},
    "SI": {
        "csc:" + str(n): "ordinary municipal seat outside both state city-status lists"
        for n in [104063, 104071, 104110, 104151, 104209, 104311]
    },
}
kr = {
    "csc:65515": "csc:65519",
    "csc:65533": "csc:65534",
    "csc:65426": "csc:65338",
    "csc:65458": "csc:65455",
    "csc:65296": "csc:65418",
    "csc:65435": "csc:65329",
}
retired["KR"] = {k: "duplicate English spelling of " + v for k, v in kr.items()}

with tarfile.open(root / "artifacts/winrisef-world-cities-0.1.6.tgz") as t:
    old = {
        cc: {
            r["id"]: r
            for r in json.load(t.extractfile("package/data/cities/" + cc + ".json"))
        }
        for cc in cc_by
    }
for removed, keep in kr.items():
    r = next(r for r in cc_by["KR"] if r["id"] == keep)
    r["aliases"] = sorted(
        set([*r.get("aliases", []), old["KR"][removed]["en"], old["KR"][removed]["zh"]])
        - set([None, r["zh"], r["en"]])
    )
for cc, rows in cc_by.items():
    for r in rows:
        if r["id"] in extras and not r["zh"]:
            r["zh"] = extras[r["id"]]["zh"]
        if cc == "ZA" and r["en"] == "Ekurhuleni":
            r["officialId"] = "EKU"
    dataids = {r["id"] for r in rows}
    assert not dataids.intersection(retired.get(cc, {})) and len(dataids) == len(rows)
snapshot = {
    cc: dict(cities=rows, retired=sorted(retired.get(cc, {})))
    for cc, rows in sorted(cc_by.items())
}


def write_gz(path, obj):
    data = json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    path.write_bytes(gzip.compress(data, mtime=0))


path = root / "sources/national-review-2026.json.gz"
write_gz(path, snapshot)
lockfile = root / "sources.lock.json"
lock = json.loads(lockfile.read_bytes())
lock["nationalReview"] = dict(
    file=str(path.relative_to(root)),
    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    provenance="licenses/national-review.md",
)
lockfile.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")
with (review / "national-matches.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "country",
            "officialName",
            "officialCodes",
            "region",
            "cityId",
            "in_0.1.6",
            "coordinateSource",
            "matchedGeoNames",
            "chineseWikidata",
        ]
    )
    for cc in sorted(evidence):
        for x in evidence[cc]:
            writer.writerow(
                [
                    cc,
                    x["name"],
                    "|".join(x["officialCodes"])
                    if (cc, x["name"]) != ("ZA", "Ekurhuleni")
                    else "EKU",
                    x["province"],
                    x["city"],
                    int(x["city"] in old[cc]),
                    x["pointSource"].replace("official-polygon", "reference-polygon"),
                    x["geoNames"],
                    extras.get(x["city"], {}).get("entity", ""),
                ]
            )
with (review / "retired.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["country", "cityId", "name", "reason"])
    for cc, rr in retired.items():
        for id, why in rr.items():
            w.writerow([cc, id, old[cc][id]["en"], why])
print(
    [
        (
            cc,
            len(rows),
            len([r for r in rows if r["id"] not in old[cc]]),
            len(retired.get(cc, {})),
        )
        for cc, rows in cc_by.items()
    ]
)
