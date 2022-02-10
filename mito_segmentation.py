import tifffile
import skimage.filters as skf
import numpy as np


def run_segmentation(path, file):
    im = tifffile.imread(path+'/'+file)
    intensity_im = im[0, :, :]
    mito_threshold = skf.threshold_otsu(intensity_im)
    mito_mask = intensity_im > mito_threshold
    non_mito_im = intensity_im[intensity_im <= mito_threshold]
    cyto_threshold = skf.threshold_otsu(non_mito_im)
    cyto_mask = np.logical_and((intensity_im < mito_threshold),(intensity_im >= cyto_threshold))
    return mito_mask, cyto_mask
