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


def get_raw_folder() -> str:
    """ask to choose where raw datas, stencils and masks are stored"""

    raw_folder = input(
        """
    Enter the path where raw datas, stencils and masks are stored:
    (if nothing is specified, by default in "E:/")
    --> """
    )

    if raw_folder == "":
        raw_folder = "E:/"

    return raw_folder


def get_data_folder() -> str:
    """ask to choose the folder where decoupageZIP datas are stored"""

    data_folder = input(
        """
    Enter the path where out datas will be saved:
    (if nothing is specified, by default in "~/AlpageSentinelles/data")
    --> """
    )

    if data_folder == "":
        data_folder = "data"

    return data_folder


def set_folder() -> tuple:
    """defined where tiles data and TFE are, and where the datasets will save"""

    # set where raw datas, stencils and masks are stored
    raw_folder = get_raw_folder()
    while not os.path.exists(raw_folder):
        logger.warning(f"'{raw_folder}' is not a path. Please enter a valid path.")
        raw_folder = get_raw_folder()

    # set the out folder
    data_folder = get_data_folder()
    if not os.path.exists(raw_folder):
        os.makedirs(data_folder)

    return raw_folder, data_folder


def image_importer(raw_folder: str, data_folder: str) -> None:
    """run both tiles_cutting and tiles_masking

    Parameters
    ----------
    raw_folder: where raw datas, stencils and masks are stored
    data_folder: out folder
    """

    logger.info(
        f"""
            #=======================================================#
            # The script to cut and mask raw img has been launched! #
            #=======================================================#

                The raw datas, stencils and masks folder given is:
                    {raw_folder}

                Out datas will be stored in:
                    {data_folder}

            """
    )

    cutting = input("--> Cut and save Sentinel2 tiles (Y/n)")
    masking = input("--> apply cloud and snow mask on cut tiles (Y/n)")

    if cutting == 'Y':

        logger.info(
            """
        Cutting raw_images and mask...
        ------------------------------
        """
        )

        # cut and save Sentinel2 tiles
        tiles_cutting(raw_folder, data_folder)

    else:
        logger.info("/!\ The cutting has been skipped")

    if masking == 'Y':

        logger.info(
            """
        Applying masks on cut images...
        -------------------------------------
        """
        )
        # apply cloud and snow mask on cut tiles
        tiles_masking(data_folder)

    else:
        logger.info("/!\ The masking has been skipped")


def main() -> None:
    """main function of the DatasetBuilder"""

    time_start = perf_counter()

    # set folder
    raw_folder, data_folder = set_folder()

    # cut and apply masks on raw images
    image_importer(raw_folder, data_folder)

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
