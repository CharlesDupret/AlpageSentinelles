import logging  # Flexible event logging system
import os  # Portable way of using operating system dependent functionality
from tqdm import tqdm  # A progress bar
from DatasetBuilder.src.item.TileCube import TileCube


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
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def build_TileCubes_dict(
    main_folder: str, tfe_folder: str, selected_years: list
) -> dict:
    """build a dict of TileCubes.

    Parameters
    ----------
        main_folder: the path to the folder where all years are stored
        tfe_folder: the path to the folder where TFE are stored
        selected_years: the list of selected years to building dataset

    Return
    ------
        dict of dict TileCube where keys are the years and values dict
    """

    year_dict = {}

    # loop over all selected years
    for year in tqdm(selected_years, initial=1):
        logger.info(f"{year} in processing")

        # defined paths
        year_folder = f"{main_folder}/{year}"

        # sorting the year dict
        year_dict[year] = _build_TileCubes_dict_by_year(year_folder, tfe_folder)
        logger.info(f"The TileCube dictionary of {year} has been created")

    return year_dict


def _build_TileCubes_dict_by_year(year_folder: str, tfe_folder: str) -> dict:
    """build a dict of TileCubes.

    Parameters
    ----------
        year_folder: the path to the folder where datas of the year are stored
        tfe_folder: the path to the folder where TFE are stored

    Return
    ------
        dict of TileCube where keys are the names of the tiles
    """

    # initialization
    tileCube_dict = {}
    tile_list = os.listdir(year_folder)
    tfe_list = [f for f in os.listdir(tfe_folder) if f.endswith(".shp")]

    # import over all tiles
    for tile in tqdm(tile_list, initial=1):
        tile_path = f"{year_folder}/{tile}"

        # find the right TFE
        tfe_name = [tfe_path for tfe_path in tfe_list if tile in tfe_path][0]
        tfe_path = f"{tfe_folder}/{tfe_name}"

        # build the TileCube
        cube = TileCube(tile_path, tfe_path)

        # storing the tile dict
        logger.info(f"add {cube} into the TileCube_dict")
        tileCube_dict[tile] = cube

    return tileCube_dict
