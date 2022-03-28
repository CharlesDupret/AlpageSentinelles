import os.path

import xarray as xr  # labelled multi-dimensional arrays manipulation

dataset_path = "/home/sirote/Bureau/dataset"

with xr.open_dataset(os.path.join(dataset_path, "dataset.nc")) as f:
    data = f

print(data.B04.sel(Id_sitesAS="UBABAS01"))
print(data.B04.sel(Id_sitesAS="UBABAS01"))
