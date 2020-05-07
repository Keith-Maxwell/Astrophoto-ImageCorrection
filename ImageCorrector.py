from astropy.io import fits
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from tqdm import trange  # small module that allows to display progress bars https://github.com/tqdm/tqdm


# C = ((Raw - Dark - Offset) * mean) / (Flat - Dark - Offset)


def generate_master(img_list):
    master = np.zeros((SIZE, SIZE))
    for i in trange(SIZE):
        for j in range(SIZE):
            L = [array[i, j] for array in img_list]
            master[i, j] = np.median(L)
    return master


# Liste des images à étudier
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
# show an "Open" dialog box and return the path to the selected files
raw_list = askopenfilenames(title='select RAW files')
flat_list = askopenfilenames(title='select FLAT files')
offset_list = askopenfilenames(title='select OFFSET files')

# Extraire la taille des images
hdul = fits.open(raw_list[0])
SIZE = hdul[0].header['NAXIS1']

# Concatenation des données de chacune des images
raw_concat = [fits.getdata(image) for image in raw_list]
flat_concat = [fits.getdata(image) for image in flat_list]
offset_concat = [fits.getdata(image) for image in offset_list]

# Générer les master images
master_flat = generate_master(flat_concat)
master_offset = generate_master(offset_concat)

# Générer les images corrigées
final_raw_list = [(raw - master_offset) * np.mean(master_flat) / (master_flat - master_offset) for raw in raw_concat]

# Sauvegarder les images corrigées
for i in range(len(final_raw_list)):
    hdu = fits.PrimaryHDU(final_raw_list[i])
    hdu.writeto(raw_list[i].replace('.fit', '-corrected.fit'))
