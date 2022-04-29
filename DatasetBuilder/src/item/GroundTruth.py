import geopandas as gpd  # Make working with geospatial data in python
import os  # Portable way of using operating system dependent functionality
import numpy as np  # The fundamental package for scientific computing


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
        self._update_typo_veg()

    def __repr__(self) -> str:
        return f"Ground truth points {self.__name} from {self.__path}"

    def _update_typo_veg(self):
        """fusion the columns 'typo_veg' and 'MILIEU' in typo_veg"""

        # get column values
        typo = np.array(self.tfe["typo_veg"])
        milieu = np.array(self.tfe["MILIEU"])

        # fill gaps
        for i, val in enumerate(milieu):
            if typo[i] is None:
                typo[i] = val

        # overwrite old colum 'typo_veg'
        self.tfe["typo_veg"] = typo

        # del column 'MILIEU'
        self.tfe.drop(labels="MILIEU", axis=1)

    def get_tfe(self) -> gpd.GeoDataFrame:
        """get tfe as GeoDataFrame"""
        return self.tfe

    def dict_poi(self) -> dict:
        """get a dict {"poi_name": (x, y)}"""

        return self.tfe["geometry"].to_dict()
