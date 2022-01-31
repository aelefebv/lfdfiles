import tifffile


def mask_ch1(path, mask_path, file, mask_file):
    im = tifffile.imread(path+'/'+file)
    mask = tifffile.imread(mask_path+'/'+mask_file)
    im = im[1:3, :, :]
    masked_im = im*mask
    return masked_im
