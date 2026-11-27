"""Screen a packed release against country returns in UN Demographic Yearbook table 8."""

import csv
import json
import re
import sys
import tarfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree
from bs4 import BeautifulSoup

archive, inputs, output = map(Path, sys.argv[1:])
ns = "{urn:schemas-microsoft-com:office:spreadsheet}"


def normalize(value):
    return "".join(
        c for c in unicodedata.normalize("NFKD", value.casefold()) if c.isalnum()
    )


def variants(value):
    names = [
        value,
        re.sub(r"\([^()]*\)", "", value),
        *re.findall(r"\(([^()]+)\)", value),
    ]
    return {normalize(name) for name in names if normalize(name)}


with tarfile.open(archive) as package:

    def read(name):
        return json.load(package.extractfile("package/data/" + name + ".json"))

    countries = read("countries")
    coverage = read("coverage")["byCountry"]
    regions = {cc: read("regions/" + cc) for cc in coverage}
    cities = {cc: read("cities/" + cc) for cc in coverage}

names = {normalize(c["en"]): c["id"] for c in countries}
m49 = BeautifulSoup((inputs / "m49.csv").read_bytes(), "html.parser")
for row in m49.select("#downloadTableEN tr")[1:]:
    cells = [td.get_text(strip=True) for td in row.select("td")]
    names[normalize(cells[8])] = cells[10]
alternates = {
    "United States Virgin Islands": "VI",
    "Republic of South Sudan": "SS",
    "Saint Helena ex. dep.": "SH",
    "Reunion": "RE",
    "China, Hong Kong SAR": "HK",
    "China, Macao SAR": "MO",
    "State of Palestine": "PS",
    "Micronesia (Fed. States of)": "FM",
    "Kosovo": "XK",
    "Bolivia (Plurinational State of)": "BO",
    "Netherlands (Kingdom of the)": "NL",
    "Türkiye": "TR",
    "Turkey": "TR",
}
names.update({normalize(name): code for name, code in alternates.items()})
cn_views = {
    r["id"]: r["code"][3:]
    for r in regions["CN"]
    if r["code"] in ("CN-HK", "CN-MO", "CN-TW")
}
index = defaultdict(lambda: defaultdict(set))
for cc, rows in cities.items():
    for city in rows:
        area = cn_views.get(city["region"], cc) if cc == "CN" else cc
        for label in [city["en"], *city.get("aliases", [])]:
            for spelling in variants(label):
                index[area][spelling].add(city["id"])

results = defaultdict(Counter)
differences = []
sheet = next(ElementTree.parse(inputs / "un.xls").iter(ns + "Worksheet"))
for row in sheet.iter(ns + "Row"):
    cell = row.find(ns + "Cell")
    if cell is None:
        continue
    data = cell.find(ns + "Data")
    if data is None:
        continue
    value = (
        (data.text or "")
        + "".join(
            ("" if child.tag.endswith("Sup") else "".join(child.itertext()))
            + (child.tail or "")
            for child in data
        )
    ).strip()
    style = cell.get(ns + "StyleID")
    if style == "sCountryName":
        area = names[normalize(value.split(" - ")[0].strip())]
    elif style == "sRefDate":
        date = value
    elif style == "sCityName":
        country = "CN" if area in cn_views.values() else area
        assert country in coverage, country
        ids = set().union(*(index[area].get(key, set()) for key in variants(value)))
        result = "unmatched" if not ids else "ambiguous" if len(ids) > 1 else "unique"
        results[country][result] += 1
        if result != "unique":
            differences.append(
                (country, area, date, value, result, "|".join(sorted(ids)))
            )

with (output / "un-name-review.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "country",
            "sourceArea",
            "referenceDate",
            "yearbookName",
            "match",
            "candidateIds",
        ]
    )
    writer.writerows(differences)
with (output / "country-review.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "country",
            "name",
            "packageCities",
            "nationalStatus",
            "scope",
            "source",
            "UNrows",
            "uniqueName",
            "ambiguousName",
            "unmatchedName",
        ]
    )
    for c in countries:
        cc = c["id"]
        ref = coverage[cc]["cityReference"]
        parts = ref.get("parts", {}).values()
        url = ref.get("source") or " | ".join(
            p["source"] for p in parts if "source" in p
        )
        count = results.get(cc, Counter())
        writer.writerow(
            (
                cc,
                c["zh"] or c["en"],
                len(cities[cc]),
                ref["status"],
                ref.get("scope"),
                url,
                sum(count.values()),
                count["unique"],
                count["ambiguous"],
                count["unmatched"],
            )
        )
print(
    "Country groups with UN table rows:",
    len(results),
    "rows:",
    sum(sum(v.values()) for v in results.values()),
    "review rows:",
    len(differences),
)
