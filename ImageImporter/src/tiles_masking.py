import os
import numpy as np
import rasterio


def tiles_masking(zip_folder: str, data_folder: str) -> None:
    """apply the cut_all_tile on all years

    Parameters
    ----------
    zip_folder: folder where raw sentinel2 images are stored (decoupageZIP)
    data_folder: where cut layer will be stored
    """

    year_list = os.listdir(zip_folder)

    # loop through all years
    for year in year_list:

        # defined paths
        cut_data_path = os.path.join(zip_folder, f"{year}/1_decoupageEmpriseZip/sortie")
        save_folder = os.path.join(data_folder, year)

        # cut and save Sentinel2 tiles by year
        _tiles_masking_by_year(cut_data_path, save_folder)



def _tiles_masking_by_year(cut_data_path: str, save_folder: str):
    """apply masks on all tiles of a year

    Parameters
    ----------
    cut_data_path: path to the import cut data
    save_folder: path to the folder where tiles will be saved
    """

    tile_list = os.listdir(cut_data_path)

    for tile in tile_list:
        tile_path = os.path.join(cut_data_path, tile)
        saving_tile_folder = os.path.join(save_folder, tile)
        _apply_masks_on_tile(tile_path, saving_tile_folder)


def _apply_masks_on_tile(tile_path: str, saving_tile_folder: str) -> None:
    """apply masks on all slices of a tile in a year

    Parameters
    ----------
    tile_path: tile path
    saving_tile_folder: path to the folder where slices will be saved
    """

    slice_list = os.listdir(tile_path)

    for tile_slice in slice_list:
        slice_path = os.path.join(tile_path, tile_slice)
        saving_folder = os.path.join(saving_tile_folder, tile_slice)
        _apply_masks_on_slice(slice_path, saving_folder)


def _apply_masks_on_slice(slice_path: str, saving_slice_folder: str) -> None:
    """apply a mask on a slice and save it into the out_path

    Parameters
    ----------
    slice_path: path to the slice folder
    saving_slice_folder: where the masked slice will be saved
    """

    # split bands and mask
    layer = os.listdir(slice_path)
    bands_dict = {b[20:]: b for b in layer if b[20] == "B"}
    mask_dict = {b[20:]: b for b in layer if b[20] != "B"}

    # make out folder
    os.makedirs(saving_slice_folder, exist_ok=True)

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
        out_path = os.path.join(saving_slice_folder, band)
        with rasterio.open(out_path, "w", **profile) as out:
            out.write(filtered_band, 1)
