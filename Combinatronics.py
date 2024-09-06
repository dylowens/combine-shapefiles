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


def combine_shapefiles(input_dir, output_gpkg, progress_callback=None):
    # Check dependencies before processing
    check_dependencies()

    output_dir = os.path.dirname(output_gpkg)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find all shapefiles in the input directory and its subdirectories
    shp_files = find_shapefiles(input_dir)
    print(f"Found {len(shp_files)} shapefiles")

    # Read and combine all shapefiles
    combined_gdf = gpd.GeoDataFrame()
    for i, shp_file in enumerate(shp_files):
        gdf = gpd.read_file(shp_file)
        combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)
        if progress_callback:
            progress_callback(i + 1, len(shp_files))

    # Save the combined GeoDataFrame to a GeoPackage
    combined_gdf.to_file(output_gpkg, driver='GPKG')
    print(f"Combined shapefiles saved to {output_gpkg}")


# Remove the hardcoded usage at the end of the file
