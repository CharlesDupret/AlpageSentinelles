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


def building_and_save_dataset(year_dict: dict, dataset_folder) -> None:
    """
    Parameters
    ----------
        year_dict: dict of TileCube generated by the build_TileCubes_dict function
        dataset_folder: path to the dataset folder
    """

    # loop over all years
    for year, TileCube_dict in year_dict.items():
        year_dataset_folder = f"{dataset_folder}/{year}"
        _building_and_save_dataset_by_year(TileCube_dict, year_dataset_folder, year)


def _building_and_save_dataset_by_year(TileCube_dict: dict, year_dataset_folder: str, year: str) -> None:
    """
    Parameters
    ----------
        TileCube_dict: dict of TileCube generated by the build_TileCubes_dict function
        year_dataset_folder: path to the dataset folder of the year
    """

    # create a directory in the year_dataset_folder if it does not exist
    os.makedirs(year_dataset_folder, exist_ok=True)

    # build and save one dataset per TileCube
    for cube_name, cube in tqdm(TileCube_dict.items(), initial=1):

        # create a xr.dataset with the poi of the TileCube
        da = cube.quick_fill_dataset()

        # save the dataset in to the folder given
        dataset_name = f"raw_dataset_{year}_{cube_name}.nc"
        save_path = f"{year_dataset_folder}/{dataset_name}"
        da.to_netcdf(save_path)

        logger.info(
            f" --> {year} {cube_name} is successfully saved in {year_dataset_folder} as '{dataset_name}'"
        )


def merge_dataset(dataset_folder: str) -> None:
    """merge all dataset from all tiles in one dataset
    and save it as dataset.nc in to the folder given

    Parameters
    ----------
        dataset_folder: the folder of raw_dataset
    """

    merged_dataset_path = []
    year_list = os.listdir(dataset_folder)

    # loop over all years
    for year in year_list:

        # build the dataset of the year
        year_dataset_path = f"{dataset_folder}/{year}"
        merged_dataset_path.append(_merge_dataset_by_year(year_dataset_path, year))

    # build the main dataset over all year
    _merge_main_dataset(dataset_folder, merged_dataset_path)


def _merge_dataset_by_year(year_dataset_path: str, year: str) -> str:
    """merge all dataset from all tiles in one dataset
    and save it as dataset.nc in to the folder given

    Parameters
    ----------
        year_dataset_path: the folder of one year raw_dataset
        year: the year corresponding of dataset
    """

    dataset_list = []
    merged_dataset = []

    # read all datasets
    for da_name in os.listdir(year_dataset_path):
        if "raw_dataset_" in da_name:
            da_path = f"{year_dataset_path}/{da_name}"
            merged_dataset.append(da_name)

            with xr.open_dataset(da_path) as da:
                dataset_list.append(da)

    # merge all datasets in a main dataset
    dataset = xr.merge(dataset_list)

    # save the dataset as "year_dataset.nc"
    save_path = f"{year_dataset_path}/{year}_raw_dataset.nc"
    dataset.to_netcdf(save_path)
    logger.info(f"{merged_dataset} successfully merged in '{year}_raw_dataset.nc'")

    return save_path


def _merge_main_dataset(dataset_folder: str, merged_dataset_path: list) -> None:
    """merge all dataset in a main dataset over years and save it as raw_dataset.nc in to the folder given

    Parameters
    ----------
        dataset_folder: the dataset folder
    """

    dataset_list = []
    merged_dataset = []

    # read all datasets
    for da_path in merged_dataset_path:
        with xr.open_dataset(da_path) as da:
            dataset_list.append(da)

    # merge all datasets in a main dataset
    dataset = xr.merge(dataset_list)

    # save the main dataset as "dataset.nc"
    save_path = f"{dataset_folder}/raw_dataset.nc"
    dataset.to_netcdf(save_path)
    logger.info(f"All successfully merged in 'raw_dataset.nc'")
