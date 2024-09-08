import os
import zipfile
import geopandas as gpd
import pandas as pd
import fiona
from osgeo import gdal
from tqdm import tqdm

print("GDAL version:", gdal.__version__)


def unzip_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                extract_dir = os.path.splitext(file_path)[0]
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"Extracted: {file}")


def find_shapefiles(directory):
    shapefiles = []
    for root, _, files in os.walk(directory):
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
    check_dependencies()

    shp_files = find_shapefiles(input_dir)
    print(f"Found {len(shp_files)} shapefiles")

    combined_gdf = gpd.GeoDataFrame()
    for shp_file in tqdm(shp_files, desc="Combining shapefiles"):
        gdf = gpd.read_file(shp_file)
        combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)

    combined_gdf.to_file(output_gpkg, driver='GPKG')
    print(f"Combined shapefiles saved to {output_gpkg}")


def prepare_data(input_dir):
    print("Step 1: Unzipping files")
    unzip_files(input_dir)

    print("\nStep 2: Combining shapefiles")
    output_gpkg = os.path.join(input_dir, "combined_output.gpkg")
    combine_shapefiles(input_dir, output_gpkg)


if __name__ == "__main__":
    input_directory = input(
        "Enter the directory path containing ZIP files and/or shapefiles: ").strip('"')
    prepare_data(input_directory)
