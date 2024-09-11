import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
import numpy as np
from shapely.geometry import mapping

# Read parking polygons from OSM query
parking_osm = gpd.read_file("/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/OSM/Wue_OSM_parking_polygons.gpkg")

# Get types of parking
parking_types = parking_osm['parking'].unique()
#['surface', 'street_side', None, 'underground', 'multi-storey', 'garage', 'rooftop', 'lane', 'carports', 'layby']
# Exclude parking types not needed for analysis
exclude_parkings = ['multi-storey', 'underground', 'rooftop', 'garage', 'carports']
# Filter the gdf to exclude the specified parking types
filtered_parking_osm = parking_osm[~parking_osm['parking'].isin(exclude_parkings)]
# Save filtered gdf to new geopackage
filtered_parking_osm.to_file("/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/OSM/filtered_parking_OSM.gpkg", layer='filtered_parking', driver='GPKG')


#
# Filter Polygons that have Non-NAN values in aerial image
#
# Read filtered OSM parking polygons
path_filtered_osm = "/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/OSM/filtered_parking_OSM.gpkg"
filtered_parking_osm = gpd.read_file(path_filtered_osm)

# Load the raster layer using Rasterio
raster_path = "/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/Wuerzburg_Aerial/merged_wuerzburg.tif"
with rasterio.open(raster_path) as src:
    # Read the raster data and mask NaN (black) areas
    raster_data = src.read(1)  # Reading the first band
    nodata_value = src.nodata  # Assume NoData is defined, otherwise manually set it
    if nodata_value is None:
        nodata_value = 0  # Set this according to how your NaN values are represented

    # Create a mask for all non-NaN areas (True for valid data, False for NaN)
    valid_data_mask = ~np.isnan(raster_data) if nodata_value is np.nan else (raster_data != nodata_value)

# Ensure both layers have to same crs
target_crs = "EPSG:25832" # EPSG from aerial image
if filtered_parking_osm.crs != target_crs:
    filtered_parking_osm = filtered_parking_osm.to_crs(target_crs)

# Rasterize the polygon layer to match the raster layer resolution and extent
transform = src.transform  # Get the affine transform of the raster
rasterized_osm = geometry_mask([mapping(geom) for geom in filtered_parking_osm.geometry],
                                    transform=transform,
                                    invert=True,  # Invert to get the polygon areas
                                    out_shape=raster_data.shape)

# Mask the rasterized polygons by the valid data mask
masked_polygons = np.logical_and(rasterized_osm, valid_data_mask)  # Logical AND operation to mask out NaN areas

# Save the masked raster
masked_polygons_uint8 = masked_polygons.astype(np.uint8)
masked_raster_path = "/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/Data_Preprocessing/masked_polygons.tif"

with rasterio.open(
    masked_raster_path,
    'w',
    driver='GTiff',
    height=masked_polygons.shape[0],
    width=masked_polygons.shape[1],
    count=1,
    dtype=masked_polygons_uint8.dtype,
    crs=src.crs,  # Use the CRS from the original raster
    transform=src.transform  # Use the transform from the original raster
) as dst:
    dst.write(masked_polygons, 1)  # Write the masked polygons as the first band

import matplotlib.pyplot as plt
plt.imshow(masked_polygons, cmap = 'grey')
plt.show()