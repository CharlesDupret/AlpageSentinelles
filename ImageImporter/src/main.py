from ImageImporter.src import cut_all_tile


# folder containing the outline of the areas of interest
outline_folder = "emprise"

# folder containing the .zip images of Sentinel2
zip_tile_folder = "archive_zip"

# save path
out_folder = "sortie"


cut_all_tile(zip_tile_folder, outline_folder, out_folder)
