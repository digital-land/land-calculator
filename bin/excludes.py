#!/usr/bin/env python

# create a net of areas within a boundary not in the listed dataset files

import sys
import geopandas as gpd
from shapely import Polygon, MultiPolygon, GeometryCollection
from shapely import make_valid
from pyproj import Geod
from decimal import Decimal

import warnings

warnings.filterwarnings("ignore", "GeoSeries.notna", UserWarning)


geod = Geod(ellps="WGS84")


def filter_slivers(multipolygon, min_area=3700):
    if type(s) is Polygon:
        multipolygon = MultiPolygon([multipolygon])
    polygons = []
    for polygon in list(multipolygon.geoms):
        area, perimiter = geod.geometry_area_perimeter(polygon)

        area = abs(area)
        perimiter = abs(perimiter)

        if abs(area) < min_area:
            continue

        polygons.append(polygon)

    return MultiPolygon(polygons)


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

    series = gpd.GeoSeries(shapes, crs="epsg:4326")
    series = series.make_valid()

    shape = series.union_all()
    shape = make_valid(shape)

    return shape


if __name__ == "__main__":
    output_path = sys.argv[1]
    name = sys.argv[2]
    boundary_path = sys.argv[3]
    dataset_paths = sys.argv[4:]

    boundary = gpd.read_file(boundary_path)
    boundary = make_valid(boundary)
    s = boundary

    for dataset_path in dataset_paths:
        gdf = gpd.read_file(dataset_path)
        if len(gdf):
            print(dataset_path)
            gdf = gdf.make_valid()

            p = gdf.union_all()
            p = fix_shapes(p)

            s = s.difference(p)
            s = fix_shapes(s)

    s = gpd.GeoSeries(s, crs="epsg:4326")
    s = s.simplify(0.0001)
    s = s.make_valid()

    s = fix_shapes(s)
    s = filter_slivers(s)

    gdf = gpd.GeoDataFrame(
        [
            {
                "geometry": s,
                "name": name,
            }
        ],
        crs="epsg:4326",
    )

    gdf.to_file(output_path, driver="GeoJSON")
