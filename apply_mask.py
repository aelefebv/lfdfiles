import tifffile
import skimage.filters as skf
import skimage.morphology as skm


def mask_ch1(path, mask_path, file, mask_file, med_filter_size):
    im = tifffile.imread(path+'/'+file)
    mask = tifffile.imread(mask_path+'/'+mask_file)
    im = im[1:3, :, :]
    for frame in range(0, 2):
        im[frame, :, :] = skf.median(im[frame, :, :], skm.disk(med_filter_size))
    masked_im = im*mask
    return masked_im
