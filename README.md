
<div align="center">
  <img src=img/background.jpeg><br>
</div>


# AlpageSentinelles

This is my end of study project in the context of [AlpageSentinelles](https://www.alpages-sentinelles.fr/) action and 
realized with [Pacte](https://www.pacte-grenoble.fr/) laboratory  based in France, Grenoble. This project is about a 
classification of mountain pasture characteristics from Sentinel-2 spectral images. 

**Goals**: Show how remote sensing can help to:

  - Maps mountain pastures
  - Better understanding impact of climate change
  - Improve sheep management


***


## Outline

  1. [`DatasetBuilder`](DatasetBuilder): Build a dataset based on the ground truth establish by 
[AlpageSentinelles](https://www.alpages-sentinelles.fr/). The associate executable script is `bin/dataset_builder.py`.
  2. 


### Structure of the project

  - `data`: Contain the main dataset, you can also put all your local data like TFE.
  - `doc`: reports and other project related documents
  - `environement.yaml`: the developing environment
  

### Executables

Executable are sored in bin/

  - [`dataset_builder.py`](bin) is the script to build the dataset based on the ground truth


## Glossary 
  - `Tile` or `Tile Cube`: All data about the 100km by 100km area (bands, time series, mask).
  - `Slice`: A spectral images at one a given date.
  - `Layer`: A band or a mask of spectral image.
  - `Bands`: One or several bands corresponding to a spectral image at one date.
  - `Mask`: Sentinel2 mask used to remove clouds and snow.

## Links

  - [Bibliographies]()
  - [My AlpageSentinelles' drive]()



| Name           | Email                           |
|----------------|---------------------------------|
| Charles Dupret | charles.dupret@grenoble-inp.org | 

