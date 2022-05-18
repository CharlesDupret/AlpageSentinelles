import os  # Portable way of using operating system dependent functionality
from time import perf_counter  # to calculate the computation time
import logging  # a logger


# My imports
from ImageImporter.src.tiles_cutting import tiles_cutting
from ImageImporter.src.tiles_masking import tiles_masking


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


def get_zip_folder() -> str:
    """ask the use to choose the folder where decoupageZIP datas are stored"""

    zip_folder = input(
        """
    Enter the path where datasets will saved:
    (if nothing is specified, by default in "data/decoupageZip")
    --> """
    )

    if zip_folder == "":
        zip_folder = "data/decoupageZip"

    return zip_folder


def get_cut_data_folder() -> str:
    """ask the use to choose the folder where decoupageZIP datas are stored"""

    cut_data_folder = input(
        """
    Enter the path where datasets will saved:
    (if nothing is specified, by default in "data/decoupageZip")
    --> """
    )

    if cut_data_folder == "":
        cut_data_folder = "data/decoupageZip"

    return cut_data_folder


def get_data_folder() -> str:
    """ask the use to choose the folder where decoupageZIP datas are stored"""

    data_folder = input(
        """
    Enter the path where datasets will saved:
    (if nothing is specified, by default in "data")
    --> """
    )

    if data_folder == "":
        data_folder = "data"

    return data_folder


def set_folder() -> tuple:
    """defined where tiles data and TFE are, and where the datasets will save"""

    # set where tile are stored
    zip_folder = get_zip_folder()
    while not os.path.exists(zip_folder):
        logger.warning(f"'{zip_folder}' is not a path. Please enter a valid path.")
        zip_folder = get_zip_folder()

    # set where TFE are stored
    cut_data_folder = get_cut_data_folder()
    while not os.path.exists(cut_data_folder):
        logger.warning(f"'{cut_data_folder}' is not a path. Please enter a valid path.")
        cut_data_folder = get_cut_data_folder()

    # set the dataset folder
    data_folder = get_data_folder()
    if not os.path.exists(zip_folder):
        os.makedirs(data_folder)

    return zip_folder, cut_data_folder, data_folder


def image_importer(zip_folder: str, cut_data_folder: str, data_folder: str) -> None:
    """run both tiles_cutting and tiles_masking

    Parameters
    ----------
    zip_folder:
    cut_data_folder:
    data_folder:
    """

    logger.info(
        f"""
            #=======================================================#
            # The script to cut and mask raw img has been launched! #
            #=======================================================#

                The ZIP data given are stored in:
                    {zip_folder}

                The cut layer given are on TFE files stored in:
                    {cut_data_folder}

                Dataset will stored as netCDF4 files in:
                    {data_folder}

            """
    )

    logger.info(
        """
    Cutting raw_images and mask...
    ------------------------------
    """
    )

    # cut and save Sentinel2 tiles
    tiles_cutting(zip_folder, data_folder)

    logger.info(
        """
    Applying masks on cut images...
    -------------------------------------
    """
    )

    # apply cloud and snow mask on cut tiles
    tiles_masking(cut_data_folder, data_folder)


def main() -> None:
    """main function of the DatasetBuilder"""

    time_start = perf_counter()

    # set folder
    zip_folder, cut_data_folder, data_folder = set_folder()

    # cut and apply masks on raw images
    image_importer(zip_folder, cut_data_folder, data_folder)

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
