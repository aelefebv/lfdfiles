import tifffile
import skimage.filters as skf
import numpy as np


# Function to perform segmentation on an image
def run_segmentation(path, file):
    # Read the image file
    im = tifffile.imread(path+'/'+file)
    # Extract the intensity image
    intensity_im = im[0, :, :]
    # Apply Otsu's thresholding to separate mitochondria from the background
    mito_threshold = skf.threshold_otsu(intensity_im)
    mito_mask = intensity_im > mito_threshold
    # Apply Otsu's thresholding to separate cytoplasm from the background
    non_mito_im = intensity_im[intensity_im <= mito_threshold]
    cyto_threshold = skf.threshold_otsu(non_mito_im)
    cyto_mask = np.logical_and((intensity_im < mito_threshold),(intensity_im >= cyto_threshold))
    return mito_mask, cyto_mask
