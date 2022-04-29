import DataBuilder

'''
def pip_install():
    """Automatically install requirements"""

    with cd(env.path):
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')

'''

# folder where tiles, TFE and dataset are stored
tile_folder = "../data/applicationMasque/sortie"
tfe_folder = "../data/TFE"
dataset_path = "../data/dataset"

DataBuilder.main(tile_folder, tfe_folder, dataset_path)
