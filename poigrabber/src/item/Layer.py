import matplotlib.pyplot as plt  # Provides an implicit way of plotting
import gdal  # GDAL for manipulating geospatial raster data
import os  # Portable way of using operating system dependent functionality
import numpy as np  # The fundamental package for scientific computing


class Layer:
    """one layer of spectral an image"""

    __name: str  # name of the band ("B01", "B02"...)
    path: str  # path of the layer
    origin: tuple  # geographical reference
    pix_size: tuple  # spatial resolution

    def __init__(self, path):
        # get information about the layer
        data = gdal.Open(path)

        info = data.GetGeoTransform()
        x_origin = info[0]
        y_origin = info[3]
        pixel_width = info[1]
        pixel_height = -info[5]

        # initialize the attributes of the tile
        self.path = path
        self.__name = os.path.split(path)[1]
        self.origin = (x_origin, y_origin)
        self.pix_size = (pixel_width, pixel_height)

    def __repr__(self):
        print(f"Band {self.__name}, path: {self.path}")

    def _get_layer_as_array(self) -> np.array:
        """get the values of the layer"""

        data = gdal.Open(self.path)
        image = data.GetRasterBand(1)

        return np.array(image.ReadAsArray())

    def show_layer(self, cmap="gray"):
        """plot the layer"""

        plt.figure()
        plt.imshow(self._get_layer_as_array(), cmap=cmap)
        plt.title(f"Band {self.__name}")
        plt.show()

    def get_poi_layer(self, poi: dict) -> dict:
        """get the values of poi in the layer with the poi’s name as key

        Parameters
        ----------

            poi: dict {"poi_name": (x, y)} of points of interest

        Returns
        -------

            {"poi_name": val} value of pixel with the poi poi_name as key
        """

        dict_poi_layer = {}
        img = self._get_layer_as_array()

        for poi_name, point in poi.items():
            col = int((point.x - self.origin[0]) / self.pix_size[0])
            row = int((self.origin[1] - point.y) / self.pix_size[1])

            dict_poi_layer[poi_name] = img[row, col]

        return dict_poi_layer
