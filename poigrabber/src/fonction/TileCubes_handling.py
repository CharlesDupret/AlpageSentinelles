import logging  # Flexible event logging system
import os  # Portable way of using operating system dependent functionality
from tqdm import tqdm  # A progress bar
from poigrabber.src.item.TileCube import TileCube


# logger configuration
LOG_FILE = f"{__name__}.log"

# clean previous log file
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# define formats
file_formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
stream_formatter = logging.Formatter("%(message)s")

# log file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# stream log
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def build_TileCubes_dict(tile_folder: str, tfe_folder: str) -> dict:
    """build a dict of TileCubes.

    Parameters
    ----------

        tile_folder: the path to the file where datas are stored

        tfe_folder: the path to the file where TFE are stored

    Return
    ------

        dict of TileCube where keys are the names of the tiles
    """

    # initialization
    tileCube_dict = {}
    tile_list = os.listdir(tile_folder)
    tfe_list = [f for f in os.listdir(tfe_folder) if f.endswith(".shp")]

    # import through all directories
    for tile in tqdm(tile_list):
        tile_path = os.path.join(tile_folder, tile)

        # find the right TFE
        tile_name = tile[6:]
        tfe_name = [tfe_path for tfe_path in tfe_list if tile_name in tfe_path][0]
        tfe_path = os.path.join(tfe_folder, tfe_name)

        # build the TileCube
        cube = TileCube(tile_path, tfe_path)

        # storing in dict
        logger.info(f"add {cube} into the TileCube_dict")
        tileCube_dict[tile_name] = cube

    logger.info("The TileCube dictionary has been created")

    return tileCube_dict
