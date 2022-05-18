import os  # Portable way of using operating system dependent functionality
from zipfile import ZipFile  # provides tools to handling ZIP file
import gdal  # GDAL for manipulating geospatial raster data
import logging  # a logger

import numpy as np
from tqdm import tqdm  # a progress bar

# logger configuration
DIR = "log/"
LOG_FILE = f"{__name__}.log"

LOG_PATH = os.path.join(DIR, LOG_FILE)

# clean previous log file
if os.path.exists(LOG_PATH):
    os.remove(LOG_PATH)

if not os.path.exists(DIR):
    os.makedirs(DIR)

# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# define formats
file_formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
stream_formatter = logging.Formatter("%(message)s")

# log file
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# stream log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def tiles_cutting(zip_folder: str, data_folder: str) -> None:
    """apply the cut_all_tile on all years

    Parameters
    ----------
    zip_folder: folder where raw sentinel2 images are stored (decoupageZIP)
    data_folder: where cut layer will be stored
    """

    year_list = os.listdir(zip_folder)

    # loop through all years
    for year in year_list:

        # defined paths
        outline_folder = os.path.join(zip_folder, f"{year}/1_decoupageEmpriseZip/emprise")
        zip_tile_folder = os.path.join(zip_folder, f"{year}/1_decoupageEmpriseZip/archive_zip")
        out_folder = os.path.join(data_folder, f"decoupageZip/{year}/1_decoupageEmpriseZip/sortie")

        # cut and save Sentinel2 tiles by year
        _tiles_cutting_by_year(zip_tile_folder, outline_folder, out_folder)


def _tiles_cutting_by_year(zip_tile_folder: str, outline_folder: str, out_folder: str) -> None:
    """cut and save all tile in a same year in the out_folder

    Parameters
    ----------
    zip_tile_folder: folder containing all tile of a year in a .zip format
    outline_folder: folder containing outline of interest in .gpkg format
    out_folder: folder where cut tiles will be saved
    """

    # list images
    outline_list = [outline for outline in os.listdir(outline_folder)]
    tiles_list = [name for name in os.listdir(zip_tile_folder)]

    # loop through all tiles in a same year
    for tile, outline in zip(tiles_list, outline_list):
        tile_path = os.path.join(zip_tile_folder, tile)
        outline_path = os.path.join(outline_folder, outline)

        # make the list of all image taken in the year
        slice_list = [s for s in os.listdir(tile_path)]

        # cut and save all images of the tile through all dates
        for slice_name in tqdm(slice_list, initial=1):
            slice_path = os.path.join(tile_path, slice_name)
            _cut_save_zip_slice(slice_path, outline_path, out_folder)
            logger.info(f"Slice {slice_name} cut and save")


def _cut_save_zip_slice(slice_path: str, outline_path: str, out_folder: str) -> None:
    """cut and save all bands and mask of a tile ate one date

    Parameters
    ----------
    slice_path: path to the .zip containing the bands
    outline_path: path to the associated outline of interest in .gpkg format
    out_folder: folder where cut tiles will be saved
    """

    # set name of the cut slice
    split_path = os.path.basename(slice_path).split("_")
    sat = split_path[0].replace("SENTINEL", "S")
    date = split_path[1].split("-")[0]

    # makedir to save the slice
    dir_slice_name = f"{sat}_{date}_{split_path[3]}"
    logger.info(split_path[3])
    out = os.path.join(f"sortie{split_path[3]}", dir_slice_name)
    out = os.path.join(out_folder, out)
    os.makedirs(out, exist_ok=True)

    # read what files are in the .zip
    with ZipFile(slice_path, "r") as z:
        zip_list = z.namelist()

    # make a dict of files to keep
    band_list = [f for f in zip_list if "FRE" in f]
    snow_mask = [f for f in zip_list if ("EXS" in f or "SNW" in f) and ".tif" in f]
    cloud_mask = [f for f in zip_list if "CLM" in f and "R1" in f]

    layer_dict = {"bands": band_list, "snow_mask": snow_mask, "cloud_mask": cloud_mask}

    # loop through bands and masks
    for name, layer_list in layer_dict.items():

        # ensure that bands or masks are found
        if layer_list:

            # loop through all bands
            for layer in layer_list:

                if name == "bands":
                    layer_name = layer.split("_")[-1].split(".")[0]
                    no_data = -1000

                elif name == "snow_mask":
                    layer_name = "SNW"
                    no_data = 0

                else:
                    layer_name = layer[-10:-4]
                    no_data = 0

                layer_path = os.path.join(out, f"{dir_slice_name}_{layer_name}")

                # cutting .zip layer
                sortieTif = gdal.Warp(
                    layer_path,
                    f"/vsizip/{slice_path}/{layer}",  # we use the vsizip protocol
                    creationOptions=[
                        "COMPRESS=LZW",
                        "PREDICTOR=2",
                    ],
                    cutlineDSName=outline_path,  # outline
                    dstNodata=no_data,  # nodata value -10000
                    xRes=10,  # x output resolution
                    yRes=-10,  # y output resolution
                    targetAlignedPixels=True,  # keep the same pixel location as the original image
                    cropToCutline=True,
                )

                if not sortieTif:
                    logger.error(f"Error in cutting {layer_name}")

        # write in the logger if a mask is missing
        else:
            logger.warning(f"They is no {name} in {slice_path}")
