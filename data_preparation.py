#This script prepares our input data for our deep learning models.
#It analyzes and filteres out tiles that dont't contain parking lot pixels.
# Additionally, it saves that those tiles, where the pixel sum for the parking lots is greater than the median for further analysis. 

# load libaries
import os
import shutil
import glob
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# Set the path to the folder containing the mask and raster files
mask_folder = '/Users/marle/Downloads/masks_all/mask'
raster_folder = '/Users/marle/Downloads/raster_all/raster'

# Get all files
mask_files = sorted(glob.glob(mask_folder + '/*.npy'))
print(f"Total number of masks: {len(mask_files)}")
raster_files = sorted(glob.glob(raster_folder + '/*.npy'))
print(f"Total number of rasters: {len(raster_files)}")

# calculate the sum and percentage of 1's in each mask
# initialize dictionary
px_dict = {}

# Loop over all mask files
for mask_file in mask_files:
    mask = np.load(mask_file, mmap_mode='r')  # Load mask using memory mapping for efficiency
    sum_mask = np.sum(mask) # Calculate the sum of 1's in the mask
    px_dict[mask_file ] = [sum_mask, sum_mask/mask.size] # Store the sum and percentage of 1's
    
# Check if the dictionary was filled correctly
print(f"Dictionary size: {len(px_dict)}")
print(f"Example entry: {list(px_dict.items())[0]}")


# only keep masks that have pixel sum of 1s > 0
masks_above_zero = [k for k, v in px_dict.items() if v[0] > 0]
print(len(masks_above_zero))

#calculate the median of pixel sums for masks above zero for further analysis
# get the pixel values for masks above zero
px_values_above_zero = [value[0] for value in px_dict.values() if value[0] > 0]
#calculate median
median = np.median(px_values_above_zero)
print(median)

# find the matching rasters for the masks above zero
# Extract the relevant parts of filenames for matching masks and rasters
def extract_common_part(filename):
    basename = os.path.basename(filename)
    parts = basename.split('_')
    if len(parts) >= 6:
        first_part = parts[0] + '_' + parts[1]  # "32562_5513"
        tile_part = parts[-2] + '_' + parts[-1].replace('.npy', '')  # "1000_1200"
        return first_part, tile_part
    return None, None
  
# Apply the function to extract common parts from both rasters and masks
raster_common_parts = set(extract_common_part(f) for f in raster_files)
mask_common_parts = set(extract_common_part(f) for f in masks_above_zero)


# Find the common parts that are present in both raster and mask files
matching_mask_files = [f for f in masks_above_zero if extract_common_part(f) in raster_common_parts]

print(f"Number of matching masks: {len(matching_mask_files)}")


matching_raster_files = [f for f in raster_files
                         if extract_common_part(f) in mask_common_parts]

print(f"Number of matching rasters: {len(matching_raster_files)}")


# export matching masks
filtered_masks_folder = '/Users/marle/Downloads/maks_filtered'

if not os.path.exists(filtered_masks_folder):
    os.makedirs(filtered_masks_folder)

# Copy matching raster files to the new folder
for mask_file in matching_mask_files:
    # Extract the filename from the full path
    filename = os.path.basename(mask_file)
    
    # Construct the destination path
    destination_path = os.path.join(filtered_masks_folder, filename)
    
    # Copy the raster file to the 'filtered' folder
    shutil.copy(mask_file, destination_path)

print(f"Copied {len(matching_mask_files)} masks files to the 'filtered_masks' folder.")


# export matching rasters
filtered_rasters_folder = '/Users/marle/Downloads/rasters_filtered'

if not os.path.exists(filtered_rasters_folder):
    os.makedirs(filtered_rasters_folder)

# Copy matching raster files to the new folder
for raster_file in matching_raster_files:
    # Extract the filename from the full path
    filename = os.path.basename(raster_file)
    
    # Construct the destination path
    destination_path = os.path.join(filtered_rasters_folder, filename)
    
    # Copy the raster file to the 'filtered' folder
    shutil.copy(raster_file, destination_path)

print(f"Copied {len(matching_raster_files)} raster files to the 'filtered_rasters' folder.")




# Additonally, filter all masks that have a pixel sum of 1s > median 

# only keep masks that have pixel sum of 1s > 0
masks_above_median = [k for k, v in px_dict.items() if v[0] > median]
print(len(masks_above_median))

# find the matching rasters for the masks above median
# Find the common parts that are present in both raster and mask files
raster_common_parts_median = set(extract_common_part(f) for f in raster_files)
mask_common_parts_median = set(extract_common_part(f) for f in masks_above_median)

# extract matching masks
matching_mask_files_median = [f for f in masks_above_median if extract_common_part(f) in mask_common_parts_median]
print(f"Number of matching masks: {len(matching_mask_files_median)}")

# extract matching rasters
matching_raster_files_median = [f for f in raster_files
                         if extract_common_part(f) in mask_common_parts_median]
print(f"Number of matching rasters: {len(matching_raster_files_median)}")

# export matching median masks
filtered_masks_median_folder = '/content/drive/MyDrive/masks_above_median'

if not os.path.exists(filtered_masks_median_folder):
    os.makedirs(filtered_masks_median_folder)

# Copy matching raster files to the new folder
for mask_file in matching_mask_files_median:
    # Extract the filename from the full path
    filename = os.path.basename(mask_file)
    
    # Construct the destination path
    destination_path = os.path.join(filtered_masks_median_folder, filename)
    
    # Copy the raster file to the 'filtered' folder
    shutil.copy(mask_file, destination_path)

print(f"Copied {len(matching_mask_files_median)} masks files to the 'filtered_masks' folder.")


# export matching median rasters
# export matching rasters
filtered_rasters_median_folder = '/content/drive/MyDrive/rasters_above_median'

if not os.path.exists(filtered_rasters_median_folder):
    os.makedirs(filtered_rasters_median_folder)

# Copy matching raster files to the new folder
for raster_file in matching_raster_files_median:
    # Extract the filename from the full path
    filename = os.path.basename(raster_file)
    
    # Construct the destination path
    destination_path = os.path.join(filtered_rasters_median_folder, filename)
    
    # Copy the raster file to the 'filtered' folder
    shutil.copy(raster_file, destination_path)

print(f"Copied {len(matching_raster_files_median)} raster files to the 'filtered_rasters' folder.")
