# Dataset-Builder

***

## What is it?
**DataBuilder** is a script to create a Xarray Dataset of point of interest 
based on Sentinel2 images .tiff and a .sch file as ground truth.


## How To Use


  - make sure that you have all dependence
  - run `bin/dataset_builder.py`

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