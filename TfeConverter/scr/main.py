import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
from tqdm import tqdm
import logging  # a logger
from time import perf_counter  # to calculate the computation time


# TODO: improve the log and some parsing

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


def get_pts_inside_polygon(
    polygon_name: str, polygon: Polygon, *, resolution=10
) -> dict:
    """get all point inside a Polygon with a given resolution

    Parameters
    ----------
        polygon_name: the polygon name to build points name
        polygon: the considered shapely.Polygon
        resolution: the resolution in meters sa kwarg set by default at 10

    Returns
    -------
        {"point_name": shapely.Point}: the point_name is the point_name + the pts number
    """

    # polygon max boundary values
    latmin, lonmin, latmax, lonmax = polygon.bounds

    # build grid which contain the polygon
    X, Y = np.meshgrid(
        np.arange(latmin, latmax, resolution), np.arange(lonmin, lonmax, resolution)
    )
    point_list = [Point(x, y) for x, y in zip(X.flatten(), Y.flatten())]

    # get only points inside the polygon
    point_dict = {
        f"{polygon_name}_{i}": p
        for i, p in enumerate(point_list)
        if polygon.contains(p)
    }

    return point_dict


def convert_tfe_polygon_to_pts(tfe_polygon: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """convert a tfe of polygon to a point tfe

    Parameters
    ----------
        tfe_polygon: a GeoDataFrame of polygons

    Returns
    -------
        tfe_point the GeoDataFrame of all point of polygons
    """
    tfe_point = gpd.GeoDataFrame()
    tfe_polygon = tfe_polygon.set_index("id_polygon")

    for index in tfe_polygon.index:

        # get a dict of point inside the polygon
        polygon = tfe_polygon.geometry[index]

        # make sur that no polygon has 'None' as ID
        if index:
            dict_point = get_pts_inside_polygon(index, polygon)

            # build the tfe_point GeoDataFrame
            name_list = list(dict_point.keys())
            pts_list = list(dict_point.values())
            typo_list = np.full(len(name_list), tfe_polygon.typo_AS[index])
            massif_list = np.full(len(name_list), tfe_polygon.MASSIF_AS[index])
            area_list = np.full(len(name_list), tfe_polygon.territoire[index])

            df = pd.DataFrame(
                {
                    "TYPO_VEGET": typo_list,
                    "MASSIF_AS": massif_list,
                    "TERRITOIRE": area_list,
                },
                index=name_list,
            )
            df.index.name = "ID_SITESAS"
            gdf = gpd.GeoDataFrame(df, geometry=pts_list, crs=tfe_polygon.crs)
            tfe_point = tfe_point.append(gdf)

        else:
            print(f"WARNING: a polygon has the name 'None', so it cannot be computed")

    return tfe_point


def build_point_tfe(path_to_polygon_tfe: str, save_path: str) -> None:
    tfe_polygon_list = [
        t
        for t in os.listdir(path_to_polygon_tfe)
        if (".shp" in t) and (".xml" not in t)
    ]

    for tfe_polygon_name in tqdm(tfe_polygon_list, desc="TFE_polygon conversion in progress:"):
        tfe_path = f"{path_to_polygon_tfe}/{tfe_polygon_name}"
        tfe_polygon = gpd.read_file(tfe_path)

        # get the converted point tfe
        tfe_point = convert_tfe_polygon_to_pts(tfe_polygon)

        # save the point tfe
        os.makedirs(save_path, exist_ok=True)
        save_name = f"{save_path}/point_from_{tfe_polygon_name}.json"
        tfe_point.to_file(save_name, driver="GeoJSON")


def get_polygon_tfe_folder() -> str:
    """ask the use to choose the folder where polygons tfe are stored"""

    polygon_tfe_folder = input(
        """
    Enter the path to the TFE folder:
    (if nothing is specified, by default in "data/TFE/TFE_2/polygon_TFE")
    --> """
    )

    if polygon_tfe_folder == "":
        polygon_tfe_folder = "data/TFE/TFE_2/polygon_TFE"

    return polygon_tfe_folder


def get_save_path() -> str:
    """ask the use to choose the folder where polygons tfe are stored"""

    save_path = input(
        """
    Enter the path to the TFE folder:
    (if nothing is specified, by default in "data/TFE/TFE_2/point_TFE")
    --> """
    )

    if save_path == "":
        save_path = "data/TFE/TFE_2/point_TFE"

    return save_path


def main() -> None:
    """main function of the TfeConverter"""

    # start time
    time_start = perf_counter()

    # get used paths
    polygon_tfe_folder = get_polygon_tfe_folder()
    save_path = get_save_path()

    logger.info(
        f"""
                #=====================================================================#
                # The script to convert polygons_TFE to points_TFE has been launched! #
                #=====================================================================#

                    The the folder which contain polygons_TFE given is:
                        {polygon_tfe_folder}

                    Out datas will be saved in:
                        {save_path}

                """
    )

    # apply conversion the function
    build_point_tfe(polygon_tfe_folder, save_path)

    # end time
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
