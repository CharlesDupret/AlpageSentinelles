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
stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)


# TODO: finish this function
def _get_snow_mask_path(slice_name: str, snow_mask_list: list) -> str:
    """get the path to the snow mask associated to the slice

    Parameters
    ----------
        slice_name: the slice name
        snow_mask_list: the list of all snow mask of slices of the year

    Returns
    -------
        snow_mask_path: the path to the right snow mask
    """

    snow_mask_path = None

    return snow_mask_path


def tiles_cutting(raw_folder: str, data_folder: str) -> None:
    """apply the cut_all_tile on all years

    Parameters
    ----------
        raw_folder: where raw datas, stencils and masks are stored
        data_folder: where cut layer will be stored
    """

    year_list = [y for y in os.listdir(raw_folder) if y[:2] == "20"]

    # loop through all years
    for year in tqdm(year_list, desc="Cut through year processing", initial=1):
        # defined paths
        stencil_folder = f"{raw_folder}/{year}/emprise"
        zip_tile_folder = f"{raw_folder}/{year}/archive_zip"
        snow_mask_folder = f"{raw_folder}/{year}/archive_zip_snow"

        year_out_folder = f"{data_folder}/1_decoupageEmpriseZip/{year}"

        # cut and save Sentinel2 tiles by year
        _tiles_cutting_by_year(zip_tile_folder, stencil_folder, snow_mask_folder, year_out_folder)


def _tiles_cutting_by_year(
        zip_tile_folder: str, stencil_folder: str, snow_mask_folder: str, year_out_folder: str
) -> None:
    """cut and save all tile in a same year in the out_folder

    Parameters
    ----------
        zip_tile_folder: folder containing all tile of a year in a .zip format
        stencil_folder: folder containing stencil of interest in .gpkg format
        snow_mask_folder: folder containing snow masks
        year_out_folder: folder where cut tiles will be saved
    """

    # list images
    stencil_list = os.listdir(stencil_folder)
    tiles_list = os.listdir(zip_tile_folder)

    # loop through all tiles in a same year
    for tile, stencil in zip(tiles_list, stencil_list):
        tile_path = os.path.join(zip_tile_folder, tile)
        stencil_path = os.path.join(stencil_folder, stencil)

        # make the list of all image taken in the year
        slice_list = [s for s in os.listdir(tile_path)]

        # snow masks of the tile
        snow_mask_list = os.listdir(f"snow_mask_folder/{tile}")

        # cut and save all slices of the tile through all dates
        for slice_name in slice_list:

            # defined the path associated to the slice
            slice_path = os.path.join(tile_path, slice_name)
            snow_mask_path = _get_snow_mask_path(slice_name, snow_mask_list)

            # cut and save the slice
            _cut_save_zip_slice(slice_path, snow_mask_path, stencil_path, year_out_folder)
            logger.info(f"Slice {slice_name} cut and save")


def _cut_save_zip_slice(slice_path: str, snow_mask_path: str, stencil_path: str, year_out_folder: str) -> None:
    """cut and save all bands and mask of a tile ate one date

    Parameters
    ----------
        slice_path: path to the .zip containing the bands
        stencil_path: path to the associated outline of interest in .gpkg format
        year_out_folder: folder where cut tiles will be saved
    """

    # set name of the cut slice
    split_path = os.path.basename(slice_path).split("_")
    sat = split_path[0].replace("SENTINEL", "S")
    date = split_path[1].split("-")[0]
    tile_name = split_path[3]

    # makedir to save the slice
    dir_slice_name = f"{sat}_{date}_{split_path[3]}"
    slice_out_folder = f"{year_out_folder}/{tile_name}/{dir_slice_name})"
    os.makedirs(slice_out_folder, exist_ok=True)

    # read what files are in the .zip
    with ZipFile(slice_path, "r") as z:
        zip_list = z.namelist()

    # make a dict of files to keep
    band_list = [f for f in zip_list if "FRE" in f]
    cloud_mask = [f for f in zip_list if "CLM" in f and "R1" in f]

    layer_dict = {"bands": band_list, "cloud_mask": cloud_mask}

    # add snow mask in layer dict
    with ZipFile(snow_mask_path, "r") as z:
        layer_dict["snow_mask"] = [f for f in z.namelist() if ("SNW" in f) and ".tif" in f]

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
                    layer_name = "SNW_R2"
                    no_data = 0

                else:
                    layer_name = "CLM_R1"
                    no_data = 0

                layer_out_path = os.path.join(slice_out_folder, f"{dir_slice_name}_{layer_name}")

                # cutting .zip layer
                sortieTif = gdal.Warp(
                    layer_out_path,
                    f"/vsizip/{slice_path}/{layer}",  # we use the vsizip protocol
                    creationOptions=[
                        "COMPRESS=LZW",
                        "PREDICTOR=2",
                    ],
                    cutlineDSName=stencil_path,  # stencil
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
            logger.info(f"They is no {name} in {slice_path}")
