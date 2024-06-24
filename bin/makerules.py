#!/usr/bin/env python3

import csv


exclude_datasets = [
    "ancient-woodland",
    "area-of-outstanding-natural-beauty",
    "battlefield",
    "built-up-area",
    "conservation-area",
    "flood-risk-zone",
    "green-belt",
    "green-space",
    "heritage-coast",
    "local-nature-reserve",
    "national-nature-reserve",
    "national-park",
    "park-and-garden",
    "ramsar",
    "scheduled-monument",
    "site-of-special-scientific-interest",
    "special-area-of-conservation",
    "special-protection-area",
    "world-heritage-site",
    "world-heritage-site-buffer-zone",
]

within_datasets = [
    "green-belt",
]

# datasets to partition / split locally
local_datasets = list(
    set(["local-authority-district"]) | set(exclude_datasets) | set(within_datasets)
)
datasets = list(set(["region"]) | set(local_datasets))

options = {
    "excludes": {
        "excludes": exclude_datasets,
        "within": "local-authority-district",
    },
}
x = {
    "within-green-belt": {
        "excludes": list(set(exclude_datasets) - set("green-belt")),
        "within": "green-belt",
    },
}

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

    print("\n# national data")
    print("DATASETS=", end="")
    for dataset in sorted(datasets):
        print(f"{sep}$(CACHE_DIR){dataset}.geojson", end="")
    print()

    print("\n# regional data")
    print("REGION_DATA=", end="")
    print(f"{sep}$(REGION_DIR)/areas.json", end="")
    for region in sorted(regions):
        print(f"{sep}$(REGION_DIR){region}/region.geojson", end="")
        for option in options:
            print(f"{sep}$(REGION_DIR){region}/{option}.geojson", end="")
    print()

    print("\n# local-authority-district data")
    print("LAD_DATA=", end="")
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

    print("# build local datasets")
    for dataset in local_datasets:
        area = "local-authority-district"
        for lad in sorted(lads):
            print(f"$(LAD_DIR){lad}/{dataset}.geojson ", end="")

        print(
            f"&:"
            f" $(CACHE_DIR){dataset}.geojson"
            f" $(CACHE_DIR){area}.geojson"
            f" bin/local-dataset.py"
        )
        print(f"\tpython3 bin/local-dataset.py {dataset}")
        print()

    print("# build local options")
    for lad in sorted(lads):
        name = lads[lad]["name"].replace("'", """'"'"'""")
        for option, o in options.items():
            boundary = f" $(LAD_DIR){lad}/{o['within']}.geojson"
            paths = []
            for dataset in o["excludes"]:
                paths.append(f"$(LAD_DIR){lad}/{dataset}.geojson")
            paths = " ".join(paths)

            print(
                f"$(LAD_DIR){lad}/{option}.geojson: {paths} {boundary} bin/excludes.py"
            )
            print(f"\tpython3 bin/excludes.py $@ '{name}' {boundary} {paths}")
            print()

    print("# build region boundaries")
    for region in sorted(regions):
        print(f"$(REGION_DIR){region}/region.geojson ", end="")
    print("&: $(CACHE_DIR)region.geojson bin/region-boundary.py")
    print("\tpython3 bin/region-boundary.py")
    print()

    print("# build region options")
    for region in sorted(regions):
        for option in options:
            paths = []
            for lad in regions[region]:
                paths.append(f"$(LAD_DIR){lad}/{option}.geojson")
            paths = " ".join(paths)

            print(f"$(REGION_DIR){region}/{option}.geojson: {paths} bin/combine.py")
            print(f"\tpython3 bin/combine.py $@ {paths}")
            print()

    print("# calculate areas")
    paths = []
    for region in sorted(regions):
        for option in options:
            paths.append(f"$(REGION_DIR){region}/{option}.geojson")
    paths = " ".join(paths)
    print(f"$(REGION_DIR)/areas.json: {paths} bin/areas.py")
    print(f"\tpython3 bin/areas.py $@ {paths}")
