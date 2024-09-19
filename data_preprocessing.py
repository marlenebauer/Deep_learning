import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from rasterio.features import geometry_mask
import numpy as np
from shapely.geometry import mapping
import os
import glob


# Read raster and vector data into one list
def read_all_files(directory):
    """
    Reads all raster (.tif) and geopackage (.gpkg) files from the specified directory.
    Pairs raster and vector files with the same filename (different extensions).

    Returns:
        paired_files: A list of tuples, each containing (filename, raster_data, vector_data)
    """

    # Create a dictionary to store paired data
    paired_files = []

    # Find all raster (.tif) and geopackage (.gpkg) files in the directory
    raster_files = glob.glob(os.path.join(directory, "*.tif"))
    geopackage_files = glob.glob(os.path.join(directory, "*.gpkg"))

    # Create a set of filenames without extensions for pairing
    raster_names = {os.path.splitext(os.path.basename(f))[0]: f for f in raster_files}
    vector_names = {os.path.splitext(os.path.basename(f))[0]: f for f in geopackage_files}

    # Pair the files based on filename without extension
    common_filenames = set(raster_names.keys()) & set(vector_names.keys())

    # Read paired files
    for name in common_filenames:
        # Read raster data
        raster_file = raster_names[name]
        with rasterio.open(raster_file) as src:
            raster_data = src.read()

        # Read vector data
        vector_file = vector_names[name]
        gdf = gpd.read_file(vector_file)

        # Append the paired data as a tuple (filename, raster_data, vector_data)
        paired_files.append((name, raster_data, gdf))

    return paired_files

directory = "/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/data"
paired_files = read_all_files(directory)

#%%
# Rasterize parking lot polygons to binary mask
def rasterize_vector_to_raster_extent(directory, paired_files):
    """
    Masks raster data using vector data to match the extent, resolution, and CRS of the corresponding raster data.

    Args:
        directory (str): Directory path where the raster files are located.
        paired_files (list): List of tuples containing (filename, raster_data, vector_data).

    Returns:
        rasterized_list (list): A list of tuples (filename, raster_data, masked_raster).
    """

    rasterized_list = []

    for filename, raster_data, vector_data in paired_files:
        # Get the shape (rows, cols) of the raster data
        raster_shape = raster_data.shape[1:]  # raster_data has shape (bands, rows, cols)

        # Get the transform (affine matrix) and CRS from the raster
        with rasterio.open(f"{directory}/{filename}.tif") as src:
            raster_transform = src.transform
            raster_crs = src.crs

        # Ensure the vector data is in the same CRS as the raster
        if vector_data.crs != raster_crs:
            vector_data = vector_data.to_crs(raster_crs)

        # Get the geometries from the vector data
        geometries = [mapping(geom) for geom in vector_data.geometry]

        # Create the mask using geometry_mask
        mask_array = geometry_mask(
            geometries,
            transform=raster_transform,
            invert=True,  # Invert the mask to get 1 inside the polygons
            out_shape=raster_shape
        )

        # Apply the mask to the raster data
        masked_raster = np.where(mask_array, raster_data, np.nan)  # Mask the raster data

        # Convert to binary mask (0 and 1)
        binary_mask = np.where(mask_array, 1, 0)
        # Count the occurrences of 0 and 1 in the binary mask
        unique, counts = np.unique(binary_mask, return_counts=True)
        counts_dict = dict(zip(unique, counts))

        # Print the count of 0 and 1
        #print(f"Counts in the binary mask for {filename}:")
        #print(f"Value 0: {counts_dict.get(0, 0)}")
        #print(f"Value 1: {counts_dict.get(1, 0)}")
        # Append the filename, raster data, and the binary mask to the output list
        rasterized_list.append((filename, raster_data, binary_mask))

    return rasterized_list

# Apply function
rasterized_list = rasterize_vector_to_raster_extent(directory, paired_files)

# Check rasterized data
plt.imshow(rasterized_list[0][2], cmap='grey')
plt.show()

#%%
def pad_array(array, tile_size):
    """
    Pad the array to ensure its dimensions are divisible by the tile_size.
    Handles both 2D and 3D arrays.

    Args:
        array (numpy array): The array to pad.
        tile_size (int): The size of the tile (assumes square tiles).

    Returns:
        numpy array: The padded array.
    """
    if array.ndim == 3:
        num_channels, num_rows, num_cols = array.shape
        pad_rows = (tile_size - (num_rows % tile_size)) % tile_size
        pad_cols = (tile_size - (num_cols % tile_size)) % tile_size
        padded_array = np.pad(array, ((0, 0), (0, pad_rows), (0, pad_cols)), mode='constant')
    elif array.ndim == 2:
        num_rows, num_cols = array.shape
        pad_rows = (tile_size - (num_rows % tile_size)) % tile_size
        pad_cols = (tile_size - (num_cols % tile_size)) % tile_size
        padded_array = np.pad(array, ((0, pad_rows), (0, pad_cols)), mode='constant')
    else:
        raise ValueError("Array must be 2D or 3D")

    return padded_array

def save_tiles_with_overlap(raster_data, mask_data, tile_size, output_dir, prefix, stride):
    """
    Save raster and mask data as overlapping tiles, including padding for non-divisible dimensions.

    Args:
        raster_data (numpy array): The raster data array.
        mask_data (numpy array): The binary mask array.
        tile_size (int): The size of each tile (assumes square tiles).
        output_dir (str): Directory to save the tiles.
        prefix (str): Prefix for filenames.
        stride (int): The number of pixels to shift for overlapping tiles.
    """
    # Pad arrays to ensure full coverage
    padded_raster_data = pad_array(raster_data, tile_size)
    padded_mask_data = pad_array(mask_data, tile_size)

    num_rows, num_cols = padded_raster_data.shape[1], padded_raster_data.shape[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for row_start in range(0, num_rows - tile_size + 1, stride):
        for col_start in range(0, num_cols - tile_size + 1, stride):
            row_end = row_start + tile_size
            col_end = col_start + tile_size

            # Crop the tiles
            raster_tile = padded_raster_data[:, row_start:row_end, col_start:col_end]
            mask_tile = padded_mask_data[row_start:row_end, col_start:col_end]

            # Save the tiles
            np.save(os.path.join(f'{output_dir}/raster', f'{prefix}_raster_tile_{row_start}_{col_start}.npy'), raster_tile)
            np.save(os.path.join(f'{output_dir}/mask', f'{prefix}_mask_tile_{row_start}_{col_start}.npy'), mask_tile)


def process_and_save_tiles(rasterized_list, tile_size, output_dir):
    """
    Process each item in the rasterized_list and save tiles.

    Args:
        rasterized_list (list): List of tuples (filename, raster_data, mask_data).
        tile_size (int): The size of each tile (assumes square tiles).
        output_dir (str): Directory to save the tiles.
    """
    for filename, raster_data, mask_data in rasterized_list:
        prefix = filename  # Use filename as prefix for tile files
        save_tiles_with_overlap(raster_data, mask_data, tile_size, output_dir, prefix, stride)

# Apply function
stride = 50
tile_size = 128
output_directory = '/Users/christinakrause/HIWI_Hannes/ParkingLotDetection/training_tiles'
process_and_save_tiles(rasterized_list, tile_size, output_directory)

array = rasterized_list[0][1]
padded_array = pad_array(array, tile_size)
print("Original shape:", array.shape)
print("Padded shape:", padded_array.shape)