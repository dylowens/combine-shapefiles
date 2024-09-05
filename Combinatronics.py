import os
import geopandas as gpd
from tqdm import tqdm
import pandas as pd
import fiona
from osgeo import gdal
print("GDAL version:", gdal.__version__)


def find_shapefiles(directory):
    shapefiles = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.shp'):
                shapefiles.append(os.path.join(root, file))
    return shapefiles


def check_dependencies():
    print("Available drivers:", fiona.supported_drivers)
    print("GDAL version:", gdal.__version__)
    if 'GPKG' not in fiona.supported_drivers:
        fiona.supported_drivers['GPKG'] = 'rw'
    print("All necessary drivers are available.")


def combine_shapefiles(input_dir, output_gpkg):
    # Check dependencies before processing
    check_dependencies()

    output_dir = os.path.dirname(output_gpkg)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find all shapefiles in the input directory and its subdirectories
    shp_files = find_shapefiles(input_dir)
    print(f"Found {len(shp_files)} shapefiles")

    combined_polygon_gdf = gpd.GeoDataFrame()
    combined_line_gdf = gpd.GeoDataFrame()
    combined_point_gdf = gpd.GeoDataFrame()

    # Process shapefiles
    for shp_file in tqdm(shp_files, desc="Processing shapefiles"):
        try:
            gdf = gpd.read_file(shp_file)
            state_name = os.path.basename(os.path.dirname(shp_file))
            gdf['state'] = state_name

            polygon_gdf = gdf[gdf.geometry.type.isin(
                ['Polygon', 'MultiPolygon'])]
            line_gdf = gdf[gdf.geometry.type.isin(
                ['LineString', 'MultiLineString'])]
            point_gdf = gdf[gdf.geometry.type.isin(['Point', 'MultiPoint'])]

            combined_polygon_gdf = pd.concat(
                [combined_polygon_gdf, polygon_gdf], ignore_index=True)
            combined_line_gdf = pd.concat(
                [combined_line_gdf, line_gdf], ignore_index=True)
            combined_point_gdf = pd.concat(
                [combined_point_gdf, point_gdf], ignore_index=True)

        except Exception as e:
            print(f"Error processing {shp_file}: {str(e)}")

    # Save to GeoPackage
    print("Saving to GeoPackage...")
    with tqdm(total=3, desc="Saving layers") as pbar:
        if not combined_polygon_gdf.empty:
            print("Simplifying polygon geometries...")
            combined_polygon_gdf['geometry'] = combined_polygon_gdf.geometry.simplify(
                tolerance=0.01)
            print("Saving polygon layer...")
            combined_polygon_gdf.to_file(
                output_gpkg, layer='combined_polygons', driver="GPKG")
            pbar.update(1)

        if not combined_line_gdf.empty:
            print("Simplifying line geometries...")
            combined_line_gdf['geometry'] = combined_line_gdf.geometry.simplify(
                tolerance=0.01)
            print("Saving line layer...")
            combined_line_gdf.to_file(
                output_gpkg, layer='combined_lines', driver="GPKG")
            pbar.update(1)

        if not combined_point_gdf.empty:
            print("Saving point layer...")
            combined_point_gdf.to_file(
                output_gpkg, layer='combined_points', driver="GPKG")
            pbar.update(1)

    print(f"Combined data saved to {output_gpkg}")


# Usage
input_directory = r'C:\Users\dylow\OneDrive\Desktop\US_State_Shapefiles\CombinatronicsTest'
print(f"Input directory: {input_directory}")
print(f"Directory exists: {os.path.exists(input_directory)}")
output_gpkg = r'C:\Users\dylow\OneDrive\Desktop\US_State_Shapefiles\CombinatronicsTest\combined_states.gpkg'
combine_shapefiles(input_directory, output_gpkg)
