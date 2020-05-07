# Astrophoto-ImageCorrection

This simple code corrects RAW .fit images using FLAT and OFFSET images using the formula :

$C = \frac{(RAW - OFFSET)*m}{FLAT - OFFSET}$

## Dependencies

- **astropy** : data extraction from the .fit files
- **numpy** : data manipulation
- **tkinter** : dialog boxes
- **tqdm** : console progress bar