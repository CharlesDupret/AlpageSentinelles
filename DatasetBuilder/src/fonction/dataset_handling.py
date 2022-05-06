import logging  # Flexible event logging system
import os  # Portable way of using operating system dependent functionality
import xarray as xr  # labelled multi-dimensional arrays manipulation
from tqdm import tqdm  # A progress bar

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


def building_and_save_dataset(
    TileCube_dict: dict, dataset_path="data/dataset/raw_dataset"
) -> list:
    """
    Parameters
    ----------
        TileCube_dict: dict of TileCube generated by the build_TileCubes_dict function
        dataset_path: path to the dataset folder
    """
    # create a directory in the dataset_path if it does not exist
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # build and save one dataset per TileCube
    for cube_name, cube in tqdm(TileCube_dict.items(), initial=1):
        # create a xr.dataset with the poi of the TileCube
        da = cube.quick_fill_dataset()

        # save the dataset in to the folder given
        save_path = os.path.join(dataset_path, f"raw_dataset_{cube_name}.nc")
        da.to_netcdf(save_path)

        logger.info(
            f" --> {cube_name} is successfully saved in {dataset_path} as 'raw_dataset_{cube_name}.nc'"
        )


def merge_dataset(dataset_path: str):
    """merge all dataset from all tiles in one dataset
    and save it as dataset.nc in to the folder given
    """

    dataset_list = []
    merged_dataset = []

    # read all datasets
    for da_name in os.listdir(dataset_path):
        if "raw_dataset_" in da_name:
            merged_dataset.append(da_name)

            with xr.open_dataset(os.path.join(dataset_path, da_name)) as da:
                dataset_list.append(da)

    # merge all datasets in a main dataset
    dataset = xr.merge(dataset_list)

    # save the main dataset as "dataset.nc"
    save_path = os.path.join(dataset_path, "raw_dataset.nc")
    dataset.to_netcdf(save_path)
    logger.info(f"{merged_dataset} are all successfully merged in 'raw_dataset.nc'")
