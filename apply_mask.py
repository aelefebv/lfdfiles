import tifffile
import skimage.filters as skf
import skimage.morphology as skm


# Function to mask channel 1 of an image using a specified mask
def mask_ch1(path, mask_path, file, mask_file, med_filter_size):
    # Read the image and mask files
    im = tifffile.imread(path+'/'+file)
    mask = tifffile.imread(mask_path+'/'+mask_file)
    # Extract the desired channels from the image
    im = im[1:3, :, :]
    # Apply median filtering to the image for noise reduction
    for frame in range(0, 2):
        im[frame, :, :] = skf.median(im[frame, :, :], skm.disk(med_filter_size))
        # Apply the mask to the image
    masked_im = im*mask
    return masked_im
