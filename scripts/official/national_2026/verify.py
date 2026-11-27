"""Compare actual tarball records to the decoded registers and their boundary features."""

import csv
import json
import os
import sys
import tarfile
from collections import defaultdict
from pathlib import Path
from shapely.geometry import Point
from national import rosters, norm
from additional_national import extend

archive, folder = map(lambda p: Path(p).resolve(), sys.argv[1:])
root = Path(__file__).resolve().parents[3]
os.chdir(folder)
with tarfile.open(archive) as package:

    def load(name):
        return json.load(package.extractfile("package/data/" + name + ".json"))

    countries = load("countries")
    regions = {r["id"]: load("regions/" + r["id"]) for r in countries}
    cities = {cc: {p["id"]: p for p in load("cities/" + cc)} for cc in regions}
    coverage = load("coverage")
with (root / "audit/2026-11-21/national-matches.csv").open() as f:
    matches = defaultdict(dict)
    for row in csv.DictReader(f):
        key = (row["region"], norm(row["officialName"]), row["officialCodes"])
        assert key not in matches[row["country"]], (key, row)
        matches[row["country"]][key] = row
registers = rosters(regions)
extend(registers)
checked = inside = 0
for cc, specs in registers.items():
    refs = matches[cc].copy()
    assigned = set()
    for spec in specs:
        codes = spec.get("partCodes") or ([spec["key"]] if spec["key"] else [])
        if cc == "ZA" and spec["name"] == "Ekurhuleni":
            codes = ["EKU"]
        link = refs.pop((spec["state"] or "", norm(spec["name"]), "|".join(codes)))
        city = cities[cc][link["cityId"]]
        assert city["id"] not in assigned
        assigned.add(city["id"])
        assert city["country"] == cc
        if spec["state"]:
            assert city["region"] == next(
                r["id"] for r in regions[cc] if r["code"] == spec["state"]
            )
        if spec["key"]:
            assert city["officialId"] == spec["key"]
        if spec.get("partCodes"):
            assert set(link["officialCodes"].split("|")) == set(spec["partCodes"])
        assert norm(spec["name"]) in {
            norm(n) for n in [city["en"], *city.get("aliases", [])]
        }
        if spec["geom"] is not None:
            assert spec["geom"].covers(Point(city["lon"], city["lat"])), (
                cc,
                spec["name"],
            )
            inside += 1
        checked += 1
    assert not refs
ax = cities["AX"]["csc:160425"]
assert ax["officialId"] == "478" and "Maarianhamina" in ax["aliases"]
assert checked + 1 == sum(map(len, matches.values()))
with (root / "audit/2026-11-21/retired.csv").open() as f:
    assert all(r["cityId"] not in cities[r["country"]] for r in csv.DictReader(f))
assert sum(map(len, cities.values())) == coverage["totals"]["cities"]
print(
    f"{checked + 1} city identities verified in {len(matches)} country/area groups; {inside} exported coordinates inside their respective boundaries."
)
