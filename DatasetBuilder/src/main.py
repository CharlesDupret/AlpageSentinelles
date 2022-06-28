import os  # Portable way of using operating system dependent functionality
from time import perf_counter  # to calculate the computation time
import logging  # a logger

# My imports
import numpy as np

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


def get_main_folder() -> str:
    """ask the use to choose the folder where tiles datas are stored"""

    main_folder = input(
        """
    Enter the path to the tiles folder:
    (if nothing is specified, by default in "data/2_applicationMasque")
    --> """
    )

    if main_folder == "":
        main_folder = "data/2_applicationMasque"

    return main_folder


def get_tfe_folder() -> str:
    """ask the use to choose the folder where tfe datas are stored"""

    tfe_folder = input(
        """
    Enter the path to the TFE folder:
    (if nothing is specified, by default in "data/TFE/TFE_2/point_TFE")
    --> """
    )

    if tfe_folder == "":
        tfe_folder = "data/TFE/TFE_2/point_TFE"

    return tfe_folder


def get_dataset_folder() -> str:
    """ask the use to choose the folder where dataset datas will save"""

    dataset_folder = input(
        """
    Enter the path where datasets will saved:
    (if nothing is specified, by default in "data/dataset/raw_dataset")
    --> """
    )

    if dataset_folder == "":
        dataset_folder = "data/dataset/raw_dataset"

    return dataset_folder


def set_folder() -> tuple:
    """defined where tiles data and TFE are, and where the datasets will save"""

    # set where tile are stored
    tile_path = get_main_folder()
    while not os.path.exists(tile_path):
        logger.warning(f"'{tile_path}' is not a path. Please enter a valid path.")
        tile_path = get_main_folder()

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


def _input_years(tile_folder: str) -> list:
    """ask the user to input a years list

    Parameters
    ----------
        tile_folder:  folder where tiles datas are stored

    Returns
    -------
        selected_years: the list of selected years
    """

    selected_years = []
    years_list = os.listdir(tile_folder)

    logger.info(
        """
    Select years to import
    ---------------------
    """
    )

    logger.info(f"The data folder contain those years: {' '.join(years_list)}")

    logger.info(
        "Input all years that you want to import to the dataset. Tap 'ok' when you have finished:\n"
    )

    validate = False
    while not validate:
        input_year = input("(year/all/ok): ")

        if ("all" == input_year) or ("*" == input_year):
            return years_list

        elif input_year in years_list:
            selected_years.append(input_year)

        elif "ok" == input_year:
            if selected_years:
                validate = True
            else:
                logger.info(
                    f"You must select at least one year among [{' '.join(years_list)}]"
                )

        else:
            logger.info(f"Sorry '{input_year}' is not in [{' '.join(years_list)}]\n")

        if selected_years == years_list:
            validate = True

    # some processing
    selected_years = np.array(selected_years)
    selected_years = np.unique(selected_years)
    selected_years = np.sort(selected_years)

    return selected_years


def _get_years_selection(tile_folder) -> list:
    """validated years list selection

    Parameters
    ----------
        tile_folder:  folder where tiles datas are stored

    Returns
    -------
        selected_years: the validated list of selected years
    """

    selected_years = None
    validate = False

    while not validate:
        selected_years = _input_years(tile_folder)

        while (validate != "Y") and (validate != "n"):
            validate = input(
                f"\nConfirm that you want to build a dataset with [{' '.join(selected_years)}] (Y/n): "
            )

        if "Y" == validate:
            validate = True

        if "n" == validate:
            validate = False

        # juste for print design
        logger.info("\n")

    return selected_years


def dataset_builder(main_folder: str, tfe_folder: str, dataset_folder: str) -> None:
    """this is function build a dataset from Sentinel-2 images
    and the ground truth data
    """

    logger.info(
        f"""
    #===========================================#
    # The script to build a dataset has launch! #
    #===========================================#
        
        The tiles given are stored in:
            {main_folder}
        
        The ground truth given are on TFE files stored in:
            {tfe_folder}
            
        Dataset will stored as netCDF4 files in:
            {dataset_folder}
            
    """
    )

    # get the parsed selected years list
    selected_years = _get_years_selection(main_folder)

    # TODO: ask to merge the new imported dataset to 'raw_dataset.nc'

    # build a dict of TileCube object
    logger.info(
        """
    Building a dict of TileCube object...
    -------------------------------------
    """
    )
    year_dict = build_TileCubes_dict(main_folder, tfe_folder, selected_years)

    # build one dataset per TileCube
    logger.info(
        """
    Building one dataset per TileCube...
    ------------------------------------
    """
    )

    building_and_save_dataset(year_dict, dataset_folder)

    # merge all datasets in "dataset.nc" stored in the dataset folder given
    logger.info(
        """
    Merging all dataset...
    ----------------------
    """
    )

    merge_dataset(dataset_folder)


def main() -> None:
    """main function of the DatasetBuilder"""

    time_start = perf_counter()
    # set paths
    main_folder, tfe_folder, dataset_folder = set_folder()
    # run the dataset_builder
    dataset_builder(main_folder, tfe_folder, dataset_folder)

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

{__name__} was executed in {h} hours {m} minutes and {s} seconds
        """
    )
