import geopandas as gpd  # Make working with geospatial data in python
import os  # Portable way of using operating system dependent functionality


class GroundTruth:
    """class that is used to describe the ground truth points in a tile"""

    __name: str  # use the name of the tile
    __path: str  # path to the .shp file where points are stored
    tfe: gpd.GeoDataFrame  # geopandas dataframe

    def __init__(self, path):
        df = gpd.read_file(path)
        df = df.drop_duplicates(["geometry"])

        self.__name = os.path.split(path)[1]
        self.__path = path
        self.tfe = df.set_index("Id_sitesAS")  # using the unique index

    def __repr__(self) -> str:
        return f"Ground truth points {self.__name} from {self.__path}"

    def get_tfe(self) -> gpd.GeoDataFrame:
        """get tfe as GeoDataFrame"""
        return self.tfe

    def dict_poi(self) -> dict:
        """get a dict {"poi_name": (x, y)}"""

        return self.tfe["geometry"].to_dict()
