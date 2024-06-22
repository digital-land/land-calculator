#!/usr/bin/env python

# split a dataset into a file per local authority district (LAD)
# LADs tesselate inside regions whereas LPAs don't

import os
import sys
import csv
import geopandas as gpd

gpd.options.io_engine = "pyogrio"

cache_dir = "var/cache/"
lad_dir = "var/lad/"

if __name__ == "__main__":

    dataset = sys.argv[1]
    dataset_path = f"{cache_dir}{dataset}.geojson"
    lad_dataset_path = f"{cache_dir}local-authority-district.geojson"

    lads = {}
    for o in csv.DictReader(open("data/local-authority.csv")):
        if o["local-planning-authority"] and not o["end-date"]:
            lad = o["local-authority-district"]
            lads[lad] = o

    loaded = False
    clip = dataset != "local-authority-district"

    for lad, o in sorted(lads.items()):
        directory = lad_dir + lad
        if not os.path.exists(directory):
            os.makedirs(directory)

        path = f"{directory}/{dataset}.geojson"
        if os.path.isfile(path):
            # touch file for make dependency
            os.utime(path)
            continue

        if not loaded:
            if clip:
                gdf = gpd.read_file(dataset_path)
                gdf = gdf[["geometry"]]

                if (dataset == "flood-risk-zone"):
                    gdf = gdf.make_valid()

            ladf = gpd.read_file(lad_dataset_path)
            loaded = True

        s = boundary = ladf.loc[ladf['reference'] == lad]

        if clip:
            s = gpd.clip(gdf, boundary)

        s = s.simplify(0.0001)
        s = s.make_valid()
        s.to_file(path, driver='GeoJSON')
