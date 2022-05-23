# Data

## What is it?

The **Data** folder contain the data witch used in this project. Some data are imported in GitHub like datasets. Other
are just local.

By default, all scripts will save datas with the following **data organisation**. But you can also specify where you want 
saved outs.


### Data organisation

```
data
│
└───  README.md
│
└─── 1_decoupageEmpriseZip
│   └─── Year
│       └─── TILE
│           └─── Slices
│                   "S2A_date_tile_B2.tif"
│                           .
│                           .
│                   "S2A_date_tile_B12.tif"
│                   "S2A_date_tile_mask.tif"
│
│
└─── 2_applicationMasque
│   └─── Year
│       └─── TILE
│           └─── Slices
│                   "S2A_date_tile_B2.tif"
│                           .
│                           .
│                   "S2A_date_tile_B12.tif"
│
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
