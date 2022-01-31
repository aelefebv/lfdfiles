import tifffile
import numpy as np


def run(path, file):
    mask_im = tifffile.imread(path+'/'+file)
    mask_im = mask_im[:, 1:-2, 1:-2]
    gs = mask_im.copy()
    phase_im = mask_im[0, :, :]
    mod_im = mask_im[1, :, :]

    gs[0, :, :] = mod_im * np.cos(np.deg2rad(phase_im))
    gs[1, :, :] = mod_im * np.sin(np.deg2rad(phase_im))

    return gs
