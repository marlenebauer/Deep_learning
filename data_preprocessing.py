import geopandas as gpd

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
