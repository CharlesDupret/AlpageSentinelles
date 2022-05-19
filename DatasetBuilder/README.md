# Dataset-Builder

## What is it?

**DataBuilder** is a script to create a Xarray Dataset of point of interest 
based on Sentinel2 images .tiff and a .sch file as ground truth.


## How To Use

  - make sure that you have all **dependence**
  - run in you terminal:

```Language
~/AlpageSentinelle python3 -m DatasetBuilder
```

  - give the path to the sentinel images and the TFE (by default in data/)

  - logs of your run will be generated in [log/](log)

  - datasets will be saved by default un [data/dataset/raw_dataset](../data/dataset/raw_dataset)


## Dependencies

  - numpy
  - geopandas
  - pandas
  - xarray
  - GDAL
  - scipy

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


