"""Verify the published shards against the 2026-11-21 register crosswalk and prior release."""
import csv
import json
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "audit/2026-11-21/single-city-review"


def records(package, path):
    return json.load(package.extractfile("package/data/" + path + ".json"))


def read_csv(name):
    with (AUDIT / name).open() as file:
        return list(csv.DictReader(file))


def verify(previous, release):
    places = read_csv("matches.csv")
    reviews = {r["country"]: r for r in read_csv("country-review.csv")}
    before = records(previous, "coverage")["byCountry"]
    coverage = records(release, "coverage")
    after = coverage["byCountry"]
    assert set(before) == set(after)
    assert {cc for cc in before if before[cc]["cities"] == 1} <= reviews.keys()
    referenced = {}
    for r in places:
        key = (r["country"], r["id"])
        assert key not in referenced, key
        referenced[key] = r
    for cc in before:
        old = records(previous, "cities/" + cc)
        new = records(release, "cities/" + cc)
        if cc not in reviews:
            assert old == new, cc
            continue
        scope = reviews[cc]
        assert len(old) == int(scope["before"])
        assert len(new) == int(scope["after"]) == after[cc]["cities"]
        assert after[cc]["cityReference"]["status"] == scope["status"]
        old_ids = {p["id"] for p in old}
        removed = old_ids - {p["id"] for p in new}
        assert removed == ({"csc:150061"} if cc == "BQ" else set()), cc
        for p in new:
            r = referenced.pop((cc, p["id"]), None)
            if r is None:
                assert p["id"] in old_ids
                continue
            assert p["en"] == r["name"]
            assert (p["zh"] or "") == r["zh"]
            assert (p["region"] or "") == r["region"]
            assert p.get("officialId", "") == r["registerCode"]
            assert p["kind"] == r["kind"]
            assert p.get("aliases", []) == json.loads(r["aliases"])
            assert p["lat"] == float(r["latitude"]) and p["lon"] == float(r["longitude"])
    assert not referenced, list(referenced)
    assert coverage["totals"]["cities"] == sum(v["cities"] for v in after.values())
    return len(places)


if __name__ == "__main__":
    with tarfile.open(sys.argv[1]) as previous, tarfile.open(sys.argv[2]) as release:
        print(f"Verified {verify(previous, release)} crosswalk records against the package.")
