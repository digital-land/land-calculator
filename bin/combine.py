#!/usr/bin/env python

# combine shapes

import sys
import geopandas as gpd


if __name__ == "__main__":
    output_path = sys.argv[1]
    dataset_paths = sys.argv[2:]

    rows = []
    for dataset_path in dataset_paths:
        df = gpd.read_file(dataset_path)
        for index, row in df.iterrows():
            if len(row["geometry"].geoms):
                rows.append({"geometry": row["geometry"], "name": row["name"]})

    if not len(rows):
        print(f"{output_path}: empty", file=sys.stderr)
        with open(output_path, "w") as w:
            print('{}', file=w)
    else:
        gdf = gpd.GeoDataFrame(rows, crs="epsg:4326")
        gdf.to_file(output_path, driver="GeoJSON")
