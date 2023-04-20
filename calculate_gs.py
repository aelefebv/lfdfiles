import tifffile
import numpy as np


def run(path, file):
    # Read the image file
    mask_im = tifffile.imread(path+'/'+file)
    # Crop the image to remove border artifacts
    mask_im = mask_im[:, 1:-2, 1:-2]
    # Create a copy of the image for calculations
    gs = mask_im.copy()
    phase_im = mask_im[0, :, :]
    mod_im = mask_im[1, :, :]

    # Calculate the real or g (cosine) and imaginary or s (sine) components of the image
    gs[0, :, :] = mod_im * np.cos(np.deg2rad(phase_im))
    gs[1, :, :] = mod_im * np.sin(np.deg2rad(phase_im))

    return gs
