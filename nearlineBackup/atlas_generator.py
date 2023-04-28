from PIL import Image
import os
import math

# Set the directory where the UDIM maps are located
dir_path = "D:\\PROJECT_AND_ARGE\\trex_230327\\_REF\\norm\\\JPEG"

# Find all UDIM map files in the directory
udim_files = [f for f in os.listdir(dir_path) if f.endswith(".jpg")]

# Get the number of UDIM tiles
num_tiles = len(udim_files)

# Calculate the number of rows and columns based on the number of UDIM tiles
num_rows = math.ceil(math.sqrt(num_tiles))
num_cols = math.ceil(num_tiles / num_rows)

# Set the resolution of the atlas map
max_size = 4096
if num_rows >= num_cols:
    atlas_width = max_size
    atlas_height = int(max_size / num_rows * num_cols // 10 * 10)
else:
    atlas_height = max_size
    atlas_width = int(max_size / num_cols * num_rows // 10 * 10)
longest_side = max(atlas_width, atlas_height)

# Sort the UDIM map files in ascending order
udim_files.sort()

# Initialize an empty atlas image
atlas_img = Image.new("RGB", (atlas_width, atlas_height))

# Iterate through each UDIM map file
for i, udim_file in enumerate(udim_files):
    # Get the UDIM number from the file name
    udim_num = int(udim_file.split(".")[1])

    # Calculate the column and row indices of the UDIM tile
    col_idx = i % num_cols
    row_idx = i // num_cols

    # Load the UDIM map file
    udim_img = Image.open(os.path.join(dir_path, udim_file))

    # Resize the UDIM tile to fit in the atlas image
    tile_img = udim_img.resize((atlas_width // num_cols, atlas_height // num_rows), resample=Image.BILINEAR)

    # Calculate the coordinates of the UDIM tile in the atlas image
    x_min = col_idx * atlas_width // num_cols
    y_min = (num_rows - 1 - row_idx) * atlas_height // num_rows
    x_max = (col_idx + 1) * atlas_width // num_cols
    y_max = (num_rows - row_idx) * atlas_height // num_rows

    # Copy the tile into the atlas image
    resized_tile_img = tile_img.resize((x_max - x_min, y_max - y_min), resample=Image.BILINEAR).convert(atlas_img.mode)
    atlas_img.paste(resized_tile_img, (x_min, y_min, x_max, y_max))

# Save the atlas image
atlas_img.save(os.path.join(dir_path, "atlas_map.png"), format="PNG")

