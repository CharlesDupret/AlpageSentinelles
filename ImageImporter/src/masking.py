import os
from osgeo import gdal
import numpy
import numpy as np
import rasterio

# drivers

gdal.AllRegister()

# se placer dans le répertoire "applicationMasque"

# traitements des images(par bande) par tuile

####################
####################
### Tuile 31TFJ ####
####################
####################


# Ouverture fichiers


repDonnees = r"../1_decoupageEmpriseZip/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"

# creation liste des sous-répertoires (les différentes dates de la tuile)

listeRep = os.listdir(repDonnees)

for i in range(len(listeRep)):
    repCourant = os.path.join(
        repDonnees, listeRep[i]
    )  # se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(
        repCourant
    )  # lister les fichiers à savoir les différentes bandes

    B2 = [f for f in fichiersRep if "B2" in f]
    B3 = [f for f in fichiersRep if "B3" in f]
    B4 = [f for f in fichiersRep if "B4" in f]
    B5 = [f for f in fichiersRep if "B5" in f]
    B6 = [f for f in fichiersRep if "B6" in f]
    B7 = [f for f in fichiersRep if "B7" in f]
    B8 = [f for f in fichiersRep if "B8" in f]
    B8.sort()
    del B8[1]
    B8A = [f for f in fichiersRep if "B8A" in f]
    B11 = [f for f in fichiersRep if "B11" in f]
    B12 = [f for f in fichiersRep if "B12" in f]
    masqueCLM = [f for f in fichiersRep if "CLM" in f]

    listeBandes = B2 + B3 + B4 + B5 + B6 + B7 + B8 + B8A + B11 + B12

    for j in range(len(listeBandes)):
        nomPartiesImage = os.path.basename(listeBandes[j]).split(
            "_"
        )  # séparer les parties du fichier en cours de traitement pour les réutiliser pour la sortie
        sat = nomPartiesImage[0]
        date = nomPartiesImage[1]
        tuile = nomPartiesImage[2]
        bande = nomPartiesImage[3]

        # définir les répertoires en sortie
        rep = f"{sat}_{date}_{tuile}"
        repSortieDate = os.path.join(repSortie, rep)
        os.makedirs(repSortieDate, exist_ok=True)  # création du dossier sur le disque

        # convertir le masque pour l'appliquer
        nomMasque1 = "masqueConverti"
        masque1Sortie = os.path.join(repSortieDate, nomMasque1 + ".tiff")

        with rasterio.open(repCourant + "/" + masqueCLM[0], "r") as src:
            masque1Array = src.read(1)  # creation array
            masque1Final = np.where(masque1Array == 0, 1, np.nan)
            with rasterio.open(masque1Sortie, "w", **src.profile) as dest:
                dest.write(masque1Final.astype(rasterio.uint8), 1)

        # application du masque
        with rasterio.open(masque1Sortie, "r") as src:
            masque1 = src.read(1)
            profile = src.profile
            profile.update(
                dtype=rasterio.float64, count=1, compress="lzw", nodata=np.nan
            )
            nomImageMasque = f"{sat}_{date}_{tuile}_{bande}"
            if not os.path.exists(
                os.path.join(repSortieDate, nomImageMasque + "_masque_scaling.tiff")
            ):
                img = repCourant + "/" + listeBandes[j]

            with rasterio.open(img, "r") as src:
                band = src.read(1)
                band = band.astype(np.float64)
                band /= 10000  # band = band / 10000
                # band[band == 0] = np.nan
                profile = src.profile
                profile.update(
                    dtype=rasterio.float64, count=1, compress="lzw", nodata=np.nan
                )
                imageMasque = np.multiply(masque1, band)
                imageMasque[imageMasque == 0] = np.nan

            with rasterio.open(
                os.path.join(repSortieDate, nomImageMasque + "_masque_scaling.tiff"),
                "w",
                **profile,
            ) as dst:
                dst.write(imageMasque.astype(rasterio.float64), 1)
