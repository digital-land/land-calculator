#!/usr/bin/env python

import os
import sys
import csv
import simplejson as json
from decimal import Decimal
from itertools import combinations
from collections import OrderedDict
import geopandas as gpd
from shapely.ops import cascaded_union


gpd.options.io_engine = "pyogrio"


cache = "var/cache/"
outdir = "shapes/"
areas = {}
shapes = {}

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
    "flood-risk-zone",
#    "green-belt",
]

def hectares(gdf):
    gdf = gdf.to_crs({'proj':'cea'})
    try:
        total = sum(gdf['geometry'].area)
    except KeyError:
        total = sum(gdf.area)

    return round(Decimal(total) / Decimal(10000), 0)


def load(path):
    print(f"loading {path}")
    return gpd.read_file(path)


def save(gdf, path):
    print(f"saving {path}")
    gdf.to_file(path, driver='GeoJSON')


def dump(o, path):
    print(f"dumping {path}:", o)
    with open(path, 'w') as f:
        json.dump(o, f)


def load_regions():
    england = load(f"{cache}england.geojson")
    regions = load(f"{cache}region.geojson")

    # Region goes to low-tide, England is high-tide
    regions = gpd.clip(regions, england)
    regions = regions[['reference', 'geometry']]
    return regions


def simplify(s, tolerance=0.0001):
    #print(f"simplifying {tolerance}")
    #s = s.simplify(tolerance)

    print("making valid")
    s = s.make_valid()
    return s


if __name__ == '__main__':
    regions = load_regions()

    for reference in sorted(regions["reference"]):

        if reference not in ["E12000001"]:
            print(f"ignoring {reference}")
            continue

        excludes_path = f"{outdir}{reference}-excludes.geojson"
        if os.path.isfile(excludes_path):
            print(f"skipping {reference}")
            continue

        region = regions[regions["reference"] == reference]
        save(region, f"{outdir}{reference}.geojson")

        areas[reference] = {}
        areas[reference]["region"] = hectares(region)

        land = region.unary_union

        for dataset in excludes:
            path = f"{outdir}{reference}-excludes-{dataset}.geojson"
            if os.path.isfile(path):
                land = load(path)
            else:
                path = f"{outdir}{reference}-{dataset}.geojson"
                if os.path.isfile(path):
                    gdf = load(path)
                else:
                    gdf = load(f"{cache}{dataset}.geojson")
                    gdf = gdf[['geometry']]
                    gdf = gpd.clip(gdf, region)

                    gdf = simplify(gdf)
                    save(gdf, path)

                areas[reference][dataset] = hectares(gdf)
                dump(areas[reference][dataset], f'{outdir}{reference}-{dataset}.json')

                print("differencing")
                land = land.difference(gdf.unary_union)

                gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[land])
                save(gdf, f"{outdir}{reference}-excludes-{dataset}.geojson")

        gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[land])

        areas[reference]["excludes"] = hectares(gdf)
        dump(areas[reference], f'{outdir}{reference}.json')

        gdf = simplify(gdf)
        save(gdf, excludes_path)

        # excluding green-belt

    dump(areas, f'{outdir}areas.json')
