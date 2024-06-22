#!/usr/bin/env python

import os
import sys
import csv
import geopandas as gpd

gpd.options.io_engine = "pyogrio"

cache_dir = "var/cache/"
region_dir = "region/"

if __name__ == "__main__":

    gdf = gpd.read_file(f"{cache_dir}region.geojson")

    for row in gdf.itertuples():
        region = row.reference

        directory = region_dir + region
        if not os.path.exists(directory):
            os.makedirs(directory)

        s = gpd.GeoSeries(row.geometry, crs='epsg:4326')
        s = s.simplify(0.0001)
        s = s.make_valid()
        s.to_file(f"{region_dir}/{region}/region.geojson", driver='GeoJSON')
