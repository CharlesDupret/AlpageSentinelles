
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

  1. [`ImageImporter`](ImageImporter): Unzip and cut Sentinel2 Images and mask according area of interest around
     alpine pasture.

  2. [`DatasetBuilder`](DatasetBuilder): Build a dataset based on the ground truth establish by
     [AlpageSentinelles](https://www.alpages-sentinelles.fr/).
  
     
### Structure of the project

  - `data`: That folder contains datas used in this project. Some data are imported in GitHub like datasets. Other are
just local.

  - `doc`: Reports and other project related documents

  - `environement.yaml`: the setting of developing environment used

  - `log`: All running logs will be generated in a **log** folder (not imported in GitHub)


## About development

Scripts are working, but consider that they are not that robust. Specifically about passing and error exceptions.

If you want to continue or just helps in the development of this project please consider the `How to improve ?`
section in README of each package.

## Glossary 
  - `Tile` or `Tile Cube`: All data about a 100km by 100km (bands, time series, mask).
  - `Slice`: A spectral images at one given time.
  - `Layer`: One layer like a band or a mask of spectral image.
  - `Bands`: One or several layers corresponding to spectral bands.
  - `Mask`: Sentinel2 mask used to remove clouds and snow.

## Links

  - [Bibliographies]()
  - [My AlpageSentinelles' drive]()



| Name           | Email                           |
|----------------|---------------------------------|
| Charles Dupret | charles.dupret@grenoble-inp.org | 

