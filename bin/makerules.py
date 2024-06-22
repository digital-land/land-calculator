#!/usr/bin/env python3

import csv


excludes = [
    "national-park",
    "area-of-outstanding-natural-beauty",
    "ancient-woodland",
    "green-space",
    "heritage-coast",
    "park-and-garden",
    "local-nature-reserve",
    "national-nature-reserve",
    "ramsar",
    "site-of-special-scientific-interest",
    "special-area-of-conservation",
    "special-protection-area",
    "battlefield",
    "conservation-area",
    "scheduled-monument",
    "world-heritage-site",
    "world-heritage-site-buffer-zone",
    "built-up-area",
    "green-belt",
    "flood-risk-zone",
]

datasets = [
    "region",
    "local-authority-district",
] + excludes

lads = {}
regions = {}
sep = "\\\n    "


if __name__ == "__main__":

    for o in csv.DictReader(open("var/cache/organisation.csv")):
        if o["local-planning-authority"] and not o["end-date"]:
            lad = o["local-authority-district"]
            lads[lad] = o

            region = o["region"]
            regions.setdefault(region, [])
            regions[region].append(lad)

    print("all::\n\t@:\n")

    print("\nDATASETS=", end="")
    for dataset in sorted(datasets):
        print(f"{sep}$(CACHE_DIR){dataset}.geojson", end="")
    print()

    print("\nREGION_DATA=", end="")
    for region in sorted(regions):
        print(f"{sep}$(REGION_DIR){region}/region.geojson", end="")
    print()

    print("\nLAD_DATA=", end="")
    for dataset in datasets:
        if dataset in ["region"]:
            continue

        for lad, o in sorted(lads.items()):
            print(
                f"{sep}$(LAD_DIR)"
                f"{o['local-authority-district']}"
                f"/{dataset}.geojson",
                end="",
            )
    print()

    print()
    for dataset in datasets:
        if dataset in ["region"]:
            continue

        for lad in sorted(lads):
            print(f"$(LAD_DIR){lad}/{dataset}.geojson ", end="")

        print(
            f"&:"
            f" $(CACHE_DIR){dataset}.geojson"
            f" $(CACHE_DIR)local-authority-district.geojson"
            f" bin/shard-dataset.py"
        )
        print(f"\tpython3 bin/shard-dataset.py {dataset}")
        print()


    print()
    for region in sorted(regions):
        print(f"$(REGION_DIR){region}/region.geojson ", end="")
    print(
        f"&:"
        f" $(CACHE_DIR)region.geojson"
        f" bin/shard-region.py"
    )
    print(f"\tpython3 bin/shard-region.py")
    print()
