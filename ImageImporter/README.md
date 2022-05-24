# Image Importer

## What is it?

**DataBuilder** is a script to create a Xarray Dataset of point of interest 
based on Sentinel2 images .tiff and a .sch file as ground truth.


## How To Use

  - make sure that you have all **dependence**

  - run in you terminal:

```Language
~/AlpageSentinelle python3 -m ImageImpoter
```

  - give the path to the sentinel2 raw_data and the TFE (by default in data/)

  - logs of your run will be generated in [log](log)

  - Slices will be saved by default in [data/applicationMasque](../data/applicationMasque). The data organisation is 
describe in [data](../data).


## Dependencies

  - numpy
  - GDAL
  - rasterio

To install dependencies run in you terminal:

```Language
pip install -r requiments.txt
```

If you have some troubles about installing GDAL, you can try this command line
below:

```Language
pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version
```


## How to improve ?

  - Add a year selection for the importation. That can allow to just import a new year.
  - Improve passing
  - Add exceptions and errors messages. For example if some masques are missing...
  - Improve logs to better know what is done or missing (like snow mask)
