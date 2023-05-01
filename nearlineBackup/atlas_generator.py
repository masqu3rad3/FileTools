from PIL import Image
import os
import math


def build_matrix(udims, num_columns=10):
    max_val = max(udims)
    min_val = min(udims)
    num_rows = ((max_val - min_val) // num_columns) + 1
    matrix = [[None for j in range(num_columns)] for i in range(num_rows)]
    for val in udims:
        x = (val - min_val) // num_columns
        y = (val - min_val) % num_columns
        matrix[x][y] = val
    return matrix

# Set the directory where the UDIM maps are located
dir_path = "D:\\PROJECT_AND_ARGE\\Brachur_230220\\_REF\\CrabMonster\\Textures\\dif\\JPEG"
# dir_path = "D:\\PROJECT_AND_ARGE\\trex_230327\\_REF\\test\\JPEG"

# Find all UDIM map files in the directory
udim_files = [f for f in os.listdir(dir_path) if f.endswith(".jpg")]

def find_path_from_udim(udim_files, val):
    if not val:
        return None
    for udim_file in udim_files:
        if val == int(udim_file.split(".")[1]):
            return os.path.join(dir_path, udim_file)

def atlas_from_udims(udim_files, max_size=4096):
    udim_files.sort()
    udims = [int(x.split(".")[1]) for x in udim_files]
    print(udims)
    udim_matrix = build_matrix(udims)
    num_rows = len(udim_matrix)
    num_columns = [len([val for val in row if val is not None]) for row in udim_matrix]
    # calculate the tile size based on the number of rows and columns
    tile_size = max_size // max(num_rows, max(num_columns))
    # map_size = tile_size * max(num_rows, max(num_columns))
    map_size_x = tile_size * max(num_columns)
    map_size_y = tile_size * num_rows
    print("Tile Size:", tile_size)
    print("Map Size X:", map_size_x)
    print("Map Size Y:", map_size_y)
    # Initialize the atlas image
    atlas = Image.new("RGB", (map_size_x, map_size_y))
    # Initialize an empty atlas image
    empty_img = Image.new("RGB", (tile_size, tile_size))
    #
    # Iterate through udim_matrix and paste each tile into the atlas
    for row_nmb, row in enumerate(udim_matrix):
        for col_nmb, udim in enumerate(row):
            if udim is None:
                # paste the empty image if there is no tile
                paste_x = col_nmb * tile_size
                paste_y = row_nmb * tile_size
                atlas.paste(empty_img, (paste_x, paste_y))
            else:
                # find the path corresponding to the UDIM number
                tile_path = find_path_from_udim(udim_files, udim)
                # open the tile image
                tile = Image.open(tile_path)
                # resize the tile to the tile size
                tile = tile.resize((tile_size, tile_size), resample=Image.BILINEAR)
                # paste the tile into the atlas
                paste_x = col_nmb * tile_size
                paste_y = row_nmb * tile_size
                atlas.paste(tile, (paste_x, paste_y))
    return atlas

atlas = atlas_from_udims(udim_files)
atlas.save('atlas.jpg')
