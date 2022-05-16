import os  # Portable way of using operating system dependent functionality
from time import perf_counter  # to calculate the computation time
import logging  # a logger


# My imports
from ImageImporter.src import cut_all_tile


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


def main() -> None:
    """main function of the DatasetBuilder"""

    time_start = perf_counter()

    # set folder
    outline_folder = "emprise"  # folder of outline of the areas of interest
    zip_tile_folder = "archive_zip"  # # folder containing the .zip images of Sentinel2
    out_folder = "sortie"  # save path

    # cut and save Sentinel2 tiles
    cut_all_tile(zip_tile_folder, outline_folder, out_folder)

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
