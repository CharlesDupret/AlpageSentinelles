import os  # Portable way of using operating system dependent functionality
from zipfile import ZipFile  # provides tools to handling ZIP file
from osgeo import gdal  # GDAL for manipulating geospatial raster data


def cut_all_tile(zip_tile_folder: str, outline_folder: str, out_folder: str) -> None:
    """cut and save all tile in a same year in the out_folder

    Parameters
    ----------
    zip_tile_folder: folder containing all tile of a year in a .zip format
    outline_folder: folder containing outline of interest in .gpkg format
    out_folder: folder where cut tiles will be saved
    """

    # list images
    outline_list = [outline for outline in os.listdir(sentinel2_folder_path)]
    tiles_list = [name[3:9] for name in os.listdir(sentinel2_folder_path)]

    # loop through all tiles in a same year
    for tile, outline in zip(tiles_list, outline_list):
        tile_path = os.path.join(zip_tile_folder, tile)
        outline_path = os.path.join(outline_folder, outline)

        # make the list of all image taken in the year
        slice_list = [s for s in os.listdir(tile_path)]

        # cut and save all images of the tile through all dates
        for slice_name in slice_list:
            slice_path = os.path.join(tile_path, slice_name)
            _cut_save_zip_slice(slice_path, outline_path, out_folder)


def _cut_save_zip_slice(slice_path: str, outline_path: str, out_folder: str) -> None:
    """cut and save all bands and mask of a tile ate one date

    Parameters
    ----------
    slice_path: path to the .zip containing the bands
    outline_path: path to the associated outline of interest in .gpkg format
    out_folder: folder where cut tiles will be saved
    """

    # set name of the cut slice
    split_path = os.path.basename(slice_path).split("_")
    sat = split_path[0].replace("SENTINEL", "S")
    date = split_path[1].split("-")[0]

    # makedir to save the slice
    dir_slice_name = f"{sat}_{date}_{nomParties[3]}"
    out = os.path.join(out_folder, rep)
    os.makedirs(out, exist_ok=True)

    # read what files are in the .zip
    with ZipFile(slice_path, "r") as zip:
        zip_list = zip.namelist()

    # make a dict of files to keep
    band_list = [f for f in zip_list if "FRE" in f]
    snow_mask = [f for f in zip_list if ("EXS" in f or "SNW" in f) and ".tif" in f]
    cloud_mask = [f for f in zip_list if "CLM" in f and "R1" in f]

    layer_dict = {"bands": band_list, "snow_mask": snow_mask, "cloud_mask": cloud_mask}

    # loop through bands and masks
    for name, layer_list in layer_dict:

        # ensure that bands or masks are found
        if layer_list:

            # loop through all bands
            for layer in layer_list:

                if name == "bands":
                    layer_name = layer[-6:-4]

                else:
                    layer_name = layer[-10:-4]

                layer_path = os.path.join(out, f"{dir_slice_name}_{layer_name}")

                # cutting .zip layer
                sortieTif = gdal.Warp(
                    layer_path,
                    f"/vsizip/{dossierZip}/{img}",  # we use the vsizip protocol
                    creationOptions=[
                        "COMPRESS=LZW",
                        "PREDICTOR=2",
                    ],
                    cutlineDSName=outline_path,  # outline
                    dstNodata=-10000,  # nodata value -10000
                    xRes=10,  # x output resolution
                    yRes=-10,  # y output resolution
                    targetAlignedPixels=True,  # keep the same pixel location as the original image
                    cropToCutline=True,
                )

                if not sortieTif:
                    print(f"Error in cutting: {fichierExtrait}")

        # write in the logger if a mask is missing
        else:
            print(f"They is no {name} in {slice_path}")
