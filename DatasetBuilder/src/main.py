import os  # Portable way of using operating system dependent functionality
from time import perf_counter  # to calculate the computation time
import logging  # a logger

# My imports
from DatasetBuilder.src.fonction import build_TileCubes_dict
from DatasetBuilder.src.fonction import building_and_save_dataset, merge_dataset

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


def dataset_builder(tile_folder: str, tfe_folder: str, dataset_path: str) -> None:
    """this is function build a dataset from Sentinel-2 images
    and the ground truth data
    """

    logger.info(
        f"""
    #===========================================#
    # The script to build a dataset has launch! #
    #===========================================#
        
        The tiles given are stored in:
            {tfe_folder}
        
        The ground truth given are on TFE files stored in:
            {tfe_folder}
            
        Dataset will stored as netCDF4 files in:
            {dataset_path}
            
    """
    )

    # build a dict of TileCube object
    logger.info(
        """
    Building a dict of TileCube object...
    -------------------------------------
    """
    )
    TileCube_dict = build_TileCubes_dict(tile_folder, tfe_folder)

    # build one dataset per TileCube
    logger.info(
        """
    Building one dataset per TileCube...
    ------------------------------------
    """
    )
    building_and_save_dataset(TileCube_dict, dataset_path)

    # merge all datasets in "dataset.nc" stored in the dataset folder given
    logger.info(
        """
    Merging all dataset...
    ----------------------
    """
    )
    merge_dataset(dataset_path)


def get_tile_folder() -> str:
    """ask the use to choose the folder where tiles datas are stored"""

    tile_folder = input(
        """
    Enter the path to the tiles folder:
    (if nothing is specified, by default in "../data/applicationMasque/sortie")
    --> """
    )

    if tile_folder == "":
        tile_folder = "../data/applicationMasque/sortie"

    return tile_folder


def get_tfe_folder() -> str:
    """ask the use to choose the folder where tfe datas are stored"""

    tfe_folder = input(
        """
    Enter the path to the TFE folder:
    (if nothing is specified, by default in "../data/TFE")
    --> """
    )

    if tfe_folder == "":
        tfe_folder = "../data/TFE"

    return tfe_folder


# TODO: standardize the output data. you only need to enter the "data" folder
def get_dataset_folder() -> str:
    """ask the use to choose the folder where dataset datas will save"""

    dataset_folder = input(
        """
    Enter the path where datasets will saved:
    (if nothing is specified, by default in "../data/dataset/raw_dataset")
    --> """
    )

    if dataset_folder == "":
        dataset_folder = "../data/dataset/raw_dataset"

    return dataset_folder


def set_folder() -> tuple:
    """defined where tiles data and TFE are, and where the datasets will save"""

    # set where tile are stored
    tile_path = get_tile_folder()
    while not os.path.exists(tile_path):
        logger.warning(f"'{tile_path}' is not a path. Please enter a valid path.")
        tile_path = get_tile_folder()

    # set where TFE are stored
    tfe_path = get_tfe_folder()
    while not os.path.exists(tfe_path):
        logger.warning(f"'{tfe_path}' is not a path. Please enter a valid path.")
        tfe_path = get_tfe_folder()

    # set the dataset folder
    dataset_path = get_dataset_folder()
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    return tile_path, tfe_path, dataset_path


def main() -> None:
    """main function of the DatasetBuilder"""

    time_start = perf_counter()
    # set paths
    tile_path, tfe_path, dataset_path = set_folder()
    # run the dataset_builder
    dataset_builder(tile_path, tfe_path, dataset_path)

    time_end = perf_counter()

    # Compute the process time
    delta = time_end - time_start
    h = delta // 3600
    m = (delta - h * 3600) // 60
    s = int(delta - h * 3600 - m * 60)

    # display process time
    logger.info(
        f"""
The script had successfully run!
--------------------------------

{os.path.split(__file__)[1]} was executed in {h} hours {m} minutes and {s} seconds
        """
    )
