import matplotlib.pyplot as plt  # Provides an implicit way of plotting
import pandas as pd  # Data analysis and manipulation tool
import gdal  # GDAL for manipulating geospatial raster data
import numpy as np  # The fundamental package for scientific computing
import os  # Portable way of using operating system dependent functionality

from .Layer import Layer


class TileSlice:
    """tile at one date from Sentinel-2 composed by spacial bands"""

    __name: str  # name of the tile
    __date: pd.Timestamp  # pandas date class
    bands: dict  # dict of {"band_name": gdal.Dataset}
    mask: gdal.Band  # mask corresponding at self.__date

    def __init__(self, path):
        # find all file in the path
        list_dir = np.sort(np.array(os.listdir(path)))
        bands_names = [
            "B02",
            "B03",
            "B04",
            "B05",
            "B06",
            "B07",
            "B08A",
            "B08",
            "B11",
            "B12",
        ]

        # sort bands the list
        list_dir = np.roll(list_dir, -2)

        # initialize the attributes of the tile
        self.__name = os.path.split(path)[1]
        self.__date = pd.Timestamp(self.__name[4:12])
        self.bands = {
            name: Layer(os.path.join(path, d)) for d, name in zip(list_dir, bands_names)
        }

    def __repr__(self) -> str:
        return f"Tile {self.__name} on {self.__date}"

    def get_date(self) -> pd.Timestamp:
        """return the acquisition date of the tile as pandas timestamp"""
        return self.__date

    def get_poi_slice(self, poi: dict) -> dict:
        """get the spectral values of points of interest at one time

        Parameters
        ----------

            poi: dict {"poi_name": (x, y)} of points of interest

        Returns
        -------

            tuple (Timestamp, {poi_name: [B1, B2, ]})
        """

        poi_slice = {}

        # loop through all bands
        for _, b in self.bands.items():

            # loop through all poi
            for poi_name, val in b.get_poi_layer(poi).items():

                # add the value of the band in the dict
                if poi_name in poi_slice:
                    poi_slice[poi_name].append(val)
                else:
                    poi_slice[poi_name] = [val]

        return poi_slice

    def show_slice(self, cmap="gray"):
        """display all bands of the tile"""

        plt.figure()

        for (i, b_name), b in enumerate(self.bands):
            plt.subplot(len(self.bands), 1, i)
            plt.imshow(b, cmap=cmap)
            plt.tile(f"Band {b_name}")

        plt.show()
