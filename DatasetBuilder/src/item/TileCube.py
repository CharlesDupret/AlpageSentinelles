import xarray as xr  # labelled multi-dimensional arrays manipulation
import pandas as pd  # Data analysis and manipulation tool
import os  # Portable way of using operating system dependent functionality

from .GroundTruth import GroundTruth
from .TileSlice import TileSlice


class TileCube:
    """That is a Sentinel-2 dataCube tile for a while"""

    __name: str  # name of the tile dataCube
    __tile_cube_path: str  # the place where all self.tile data is stored
    __tfe_path: str  # the place where the TFE file is stored
    slices: dict  # (time: TileSlice) dict of TileSlice
    gt: GroundTruth  # class that contains the ground truth as a dataset

    def __init__(self, tile_cube_path, tfe_path):
        self.__name = os.path.split(tile_cube_path)[1]
        self.__tfe_path = tfe_path
        self.__tile_cube_path = tile_cube_path
        self.slices = {}

        # build the GroundTruth object
        self.gt = GroundTruth(self.__tfe_path)

        # build the TileSlice object list
        list_dir = os.listdir(tile_cube_path)

        for d in list_dir:
            slice_date = pd.Timestamp(d[4:12])
            slice_path = os.path.join(tile_cube_path, d)

            self.slices[slice_date] = TileSlice(slice_path)

    def __repr__(self) -> str:
        return f"TileCube {self.__name} composed by {len(self.slices)} slices,\
 and the ground truth {self.gt.__repr__()}"

    def _get_poi(self) -> dict:
        """get points of interest of the tile according to the ground truth

        Parameters
        ----------
            gt: a GroundTruth object corresponding to the tileCube

        Returns
        -------
            a dict {"name": (x, y)} of points of interest
        """

        return self.gt.dict_poi()

    def grab_all_poi_data(self) -> dict:
        """collects all the poi data from the TileCube

        Returns
        -------
            {band_name: pd.DataFrame( {poi_name: val}, index=time )}
        """

        # initialization
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

        poi = self._get_poi()
        time_list = []
        bands_dict = {name: None for name in bands_names}

        for band_name in bands_dict.keys():
            bands_dict[band_name] = {poi_name: [] for poi_name in poi.keys()}

        # loop through each tile slices
        for time, s in self.slices.items():
            time_list.append(time)

            # loop through each variable
            for poi_name, bands in s.get_poi_slice(poi).items():
                for i, b in enumerate(bands_names):
                    bands_dict[b][poi_name].append(bands[i])

        # make a dict dataframe for each bands
        dict_dataframe = {}
        for b in bands_names:
            df = pd.DataFrame(bands_dict[b], index=time_list)
            df.index.name = "time"
            df.columns.name = "Id_sitesAS"
            dict_dataframe[b] = df

        return dict_dataframe

    def fill_dataset(self, dict_dataframe: dict) -> xr.Dataset:
        """add the data of the TileCube to a Xarray dataset

        Parameters
        ----------
            dict_dataframe: {band_name: pd.DataFrame( {poi_name: val}, index=time )}

        Returns
        -------
            the Xarray completed by the tileCube data
        """

        dataset = xr.Dataset()

        # fill with 1D data all_cara(poi)
        tfe = self.gt.get_tfe()
        for var in tfe:
            if var != "geometry":
                dataset = dataset.assign({var: tfe[var]})

        # fill the dataset with 2D data all_(poi)
        for name, df in dict_dataframe.items():
            dataset = dataset.assign({name: df})

        return dataset

    def quick_fill_dataset(self) -> xr.Dataset:
        """a faster way to apply grab_all_poi_data and fill_dataset

        Returns
        -------
            the Xarray completed by the tileCube data
        """

        return self.fill_dataset(self.grab_all_poi_data())
