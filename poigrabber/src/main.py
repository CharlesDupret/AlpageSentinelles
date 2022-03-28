import os  # Portable way of using operating system dependent functionality
from time import perf_counter
import logging

# My imports
from fonction.TileCubes_handling import build_TileCubes_dict
from fonction.dataset_handling import building_and_save_dataset, merge_dataset


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
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def main():
    """this is function build a dataset from Sentinel-2 images
    and the ground truth data
    """

    # folder where tiles, TFE and dataset are stored
    tile_folder = "/home/sirote/Bureau/2_applicationMasque/sortie"
    tfe_folder = "/home/sirote/Bureau/TFE"
    dataset_path = "/home/sirote/Bureau/dataset"

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


if __name__ == "__main__":
    # main script
    time_start = perf_counter()
    main()
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
