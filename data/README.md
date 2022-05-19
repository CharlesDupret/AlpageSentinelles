# Data

## What is it?

The **Data** folder contain the data witch used in this project. Some data are imported in GitHub like datasets. Other
are just local.

By default, all scripts will save datas with the following **data organisation**. But you can also specify where you want 
saved outs.


### Data organisation

```
data
│   README.md
│
└─── decoupageZIP
│   └─── 2021
│       └─── 1_decoupageEmpriseZip
│          └─── sortie
│              └─── sortieTILE
│                 └─── TILES
│                     └─── Slices "S2A_date_tile"
│                         └─── Layers
│                            "S2A_date_tile_B2"
│                                     .
│                                     .
│                            "S2A_date_tile_B12"
│                            "S2A_date_tile_mask"
│
│
└─── applicationMasque
│   └─── 2021
│       └─── sortie
│           └─── sortieTILE
│               └─── TILES
│                   └─── Slices
│                       └─── Bands
│                           "S2A_date_tile_B2"
│                                    .
│                                    .
│                           "S2A_date_tile_B12" 
└─── dataset
    └─── raw_dataset
    │   raw_dataset.nc
    │
    └─── cleaned_dataset
    │   cleaned_dataset.nc
    │
    └─── filled_dataset
    │   filled_dataset.nc
    │
    └─── augmented_dataset
    │   augmented_dataset.nc

```
