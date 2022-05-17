import os
import numpy as np
import rasterio

# TODO
def apply_mask_on_all_tiles(cut_data_path: str, out_path: str):
    pass


# TODO
def apply_masks_on_tile(tile_path: str, out_path: str):
    pass


def _apply_masks_on_slice(slice_path: str, saving_folder: str) -> None:
    """apply a mask on a slice and save it into the out_path

    Parameters
    ----------
    slice_path: path to the slice folder
    saving_folder: where the masked slice will be saved
    """

    # split bands and mask
    layer = os.listdir(slice_path)
    bands_dict = {b[20:]: b for b in layer if b[20] == "B"}
    mask_dict = {b[20:]: b for b in layer if b[20] != "B"}

    # make out folder
    os.makedirs(saving_folder, exist_ok=True)

    # import all masks array
    master_mask = []
    for mask_name, mask in mask_dict.items():
        mask_path = os.path.join(slice_path, mask)

        # get mask values
        with rasterio.open(mask_path, "r") as m:
            master_mask.append(m.read(1))

    # combine all masks in one
    master_mask = np.nansum(master_mask, axis=0)

    # loop through all bands
    for band in bands_dict.values():
        # get band values and profile
        band_path = os.path.join(slice_path, band)
        with rasterio.open(band_path, "r") as m:
            band_val = m.read(1)
            profile = m.profile

        # update profile
        profile.update(dtype=rasterio.float64, count=1, compress="lzw", nodata=np.nan)

        # band filtering
        filtered_band = band_val.astype(np.float64)
        filtered_band /= 10000
        filtered_band = np.where(master_mask == 0, np.nan, band_val)

        # write the masked band
        out_path = os.path.join(saving_folder, band)
        with rasterio.open(out_path, "w", **profile) as out:
            out.write(filtered_band)
