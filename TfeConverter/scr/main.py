import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
from tqdm import tqdm


def get_pts_inside_polygon(polygon_name: str, polygon: Polygon, *, resolution=10) -> dict:
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
    X, Y = np.meshgrid(np.arange(latmin, latmax, resolution), np.arange(lonmin, lonmax, resolution))
    point_list = [Point(x, y) for x, y in zip(X.flatten(), Y.flatten())]

    # get only points inside the polygon
    point_dict = {f"{polygon_name}_{i}": p for i, p in enumerate(point_list) if polygon.contains(p)}

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

            df = pd.DataFrame({"TYPO_VEGET": typo_list}, index=name_list)
            gdf = gpd.GeoDataFrame(df, geometry=pts_list, crs=tfe_polygon.crs)
            tfe_point = tfe_point.append(gdf)

        else:
            print(f"WARNING: a polygon has the name 'None', so it cannot be computed")

    return tfe_point


def build_point_tfe(path_to_polygon_tfe: str, save_path: str) -> None:
    tfe_polygon_list = [t for t in os.listdir(path_to_polygon_tfe) if (".shp" in t) and (".xml" not in t)]

    for tfe_polygon_name in tqdm(tfe_polygon_list, desc="Convert polygon TFE: "):
        tfe_path = f"{path_to_polygon_tfe}/{tfe_polygon_name}"
        tfe_polygon = gpd.read_file(tfe_path)

        # get the converted point tfe
        tfe_point = convert_tfe_polygon_to_pts(tfe_polygon)

        # save the point tfe
        os.makedirs(save_path, exist_ok=True)
        save_name = f"{save_path}/point_from_{tfe_polygon_name}.json"
        tfe_point.to_file(save_name, driver="GeoJSON")


def main() -> None:
    path_to_polygon_tfe = "TFE/TFE_2/polygon_TFE"
    save_path = "TFE/TFE_2/point_TFE"

    build_point_tfe(path_to_polygon_tfe, save_path)
