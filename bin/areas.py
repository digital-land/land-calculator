#!/usr/bin/env python

# combine shapes

import sys
import geopandas as gpd
from decimal import Decimal
import simplejson as json

gpd.options.io_engine = "pyogrio"


def hectares(gdf):
    gdf = gdf.to_crs({'proj':'cea'})
    try:
        total = sum(gdf['geometry'].area)
    except KeyError:
        total = sum(gdf.area)
    total = Decimal(total) / Decimal(10000)
    total = round(total, 2)
    return total


if __name__ == "__main__":
    output_path = sys.argv[1]
    dataset_paths = sys.argv[2:]

    areas = {}
    for dataset_path in dataset_paths:
        gdf = gpd.read_file(dataset_path)
        areas[dataset_path] = hectares(gdf)

    with open(output_path, 'w') as f:
        json.dump(areas, f)

