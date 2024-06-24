#!/usr/bin/env python

# create a net of areas within a boundary not in the listed dataset files

import sys
import geopandas as gpd
from shapely import Polygon, MultiPolygon, GeometryCollection
from shapely import make_valid

import warnings
warnings.filterwarnings('ignore', 'GeoSeries.notna', UserWarning)

gpd.options.io_engine = "pyogrio"


# ensure we only work with polygons
def fix_shapes(series):
    if type(series) is not gpd.GeoSeries:
        series = [series]

    shapes = []
    for s in series:
        if type(s) is Polygon or type(s) is MultiPolygon:
            shapes.append(s)
        elif type(s) is GeometryCollection:
            for shape in s.geoms:
                if type(shape) is Polygon or type(shape) is MultiPolygon:
                    shapes.append(shape)

    series = gpd.GeoSeries(shapes, crs='epsg:4326')
    series = series.make_valid()

    shape = series.unary_union
    shape = make_valid(shape)

    return shape


if __name__ == "__main__":
    output_path = sys.argv[1]
    name = sys.argv[2]
    boundary_path = sys.argv[3]
    dataset_paths = sys.argv[4:]

    boundary = gpd.read_file(boundary_path)
    s = boundary

    for dataset_path in dataset_paths:
        gdf = gpd.read_file(dataset_path)
        if len(gdf):
            print(dataset_path)
            gdf = gdf.make_valid()

            p = gdf.unary_union
            p = fix_shapes(p)

            s = s.difference(p)
            s = fix_shapes(s)

    s = gpd.GeoSeries(s, crs='epsg:4326')
    s = s.simplify(0.0001)
    s = s.make_valid()

    gdf = gpd.GeoDataFrame({
        'geometry': s,
        'name': name,
    })

    gdf.to_file(output_path, driver="GeoJSON")
