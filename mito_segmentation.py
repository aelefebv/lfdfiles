import tifffile
import skimage.filters as skf


def run_segmentation(path, file):
    im = tifffile.imread(path+'/'+file)
    threshold = skf.threshold_otsu(im[0, :, :])
    mito_mask = im[0, :, :] > threshold
    return mito_mask
