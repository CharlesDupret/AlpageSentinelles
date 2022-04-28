import logging  # Flexible event logging system
import os  # Portable way of using operating system dependent functionality
import xarray as xr  # labelled multi-dimensional arrays manipulation
from tqdm import tqdm  # A progress bar

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


def building_and_save_dataset(TileCube_dict: dict, dataset_path="dataset/") -> list:
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
        if "32" not in cube_name:
            # create a xr.dataset with the poi of the TileCube
            da = cube.quick_fill_dataset()

            # save the dataset in to the folder given
            save_path = os.path.join(dataset_path, f"dataset_{cube_name}.nc")
            da.to_netcdf(save_path)

            logger.info(
                f" --> {cube_name} is successfully saved in {dataset_path} as 'dataset_{cube_name}.nc'"
            )

        else:
            logger.info(f" --> {cube_name} is skied because it's a tile 32")


def merge_dataset(dataset_path: str):
    """merge all dataset from all tiles in one dataset
    and save it as dataset.nc in to the folder given
    """

    dataset_list = []
    merged_dataset = []

    # read all datasets
    for da_name in os.listdir(dataset_path):
        if da_name != "dataset.nc":
            merged_dataset.append(da_name)

            with xr.open_dataset(os.path.join(dataset_path, da_name)) as da:
                dataset_list.append(da)

    # merge all datasets in a main dataset
    dataset = xr.merge(dataset_list)

    # save the main dataset as "dataset.nc"
    save_path = os.path.join(dataset_path, "dataset.nc")
    dataset.to_netcdf(save_path)
    logger.info(f"{merged_dataset} are all successfully merge in 'dataset.nc'")
