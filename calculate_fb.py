import tifffile
import numpy as np

import exporting
import importing


# Function to create a median stack of images in the specified path
def get_median_stack(path_to_combo_ims):
    # Get the list of files and number of samples
    combo_files = importing.get_filename_list(path_to_combo_ims, '*.tif')
    num_samples = importing.get_num_samples(combo_files, "CC0S_", 3)
    # Initialize variables
    sample_ims = []
    frame_num = 0
    sample_num = 0
    for file in combo_files:
        # Get the frame number and sample name for each file
        frame_num_current, sample_name = importing.get_frame_number(file, "_$CC0S_", 3)
        if not frame_num_current:
            print(f"[INFO] getting median fb image {sample_num + 1} of {num_samples}")
            sample_num += 1
        if frame_num_current < frame_num:
            # Calculate the median image
            med_im = np.nanmedian(np.array(sample_ims), axis=0)
            print(np.shape(med_im))
            # Save the median image
            exporting.save_im(path_to_combo_ims, file, np.array(med_im).astype('uint16'), '/median')
            sample_ims = []
            frame_num = 0
        else:
            # Read the image and append it to the sample images
            combo_im = tifffile.imread(path_to_combo_ims + '/' + file)
            sample_ims.append(combo_im)
            frame_num += 1


# Function to calculate the median fraction bound values
def get_median_fb(path_to_fb_ims):
    # Get the list of files and number of samples
    fb_files = importing.get_filename_list(path_to_fb_ims, '*.tif')
    num_samples = importing.get_num_samples(fb_files, "CC0S_", 3)
    # Initialize variables
    all_median_vals = []
    sample_median_vals = []
    frame_num = 0
    sample_num = 0
    all_sample_names = []
    for file in fb_files:
        # Get the frame number and sample name for each file
        frame_num_current, sample_name = importing.get_frame_number(file, "_$CC0S_", 3)
        if not frame_num_current:
            all_sample_names.append(sample_name)
            print(f"[INFO] getting median fb sample {sample_num + 1} of {num_samples}")
            sample_num += 1
        if frame_num_current < frame_num:
            # Calculate the mean median value and append it to the list
            all_median_vals.append(np.nanmean(sample_median_vals))
            # Reset the sample median values and frame number
            sample_median_vals = []
            frame_num = 0
        else:
            # Read the image and calculate its median value
            fb_im = tifffile.imread(path_to_fb_ims+'/'+file)
            sample_median_vals.append(np.nanmedian(fb_im))
            frame_num += 1

    return all_median_vals, all_sample_names


# Function to extract bound and free values of an image given a path and file
def run(path, file):
    # Constants, 80MHz pulse and 3.4ns and 0.4ns for bound and free lifetimes of NADH, respectively
    FREQUENCY = 80000000
    FREE_TAU = 0.4E-09
    BOUND_TAU = 3.4E-09

    # Calculate omega and the G and S values for free and bound states
    omega = 2*np.pi*FREQUENCY
    g_free = 1/(1+(omega*FREE_TAU)**2)
    s_free = (omega*FREE_TAU)/(1+(omega*FREE_TAU)**2)
    g_bound = 1/(1+(omega*BOUND_TAU)**2)
    s_bound = (omega*BOUND_TAU)/(1+(omega*BOUND_TAU)**2)

    # Read the G and S image data
    gs_im = tifffile.imread(path+'/'+file)
    g_vals = gs_im[0, :, :].flatten()
    s_vals = gs_im[1, :, :].flatten()

    # Initialize the solution matrix
    a = np.array([[g_free, g_bound, 0],
                  [s_free, s_bound, 0],
                  [1, 1, 1]])

    x = None
    for pixel in range(np.size(g_vals)):

        # Create the y vector for each pixel
        y = np.array([g_vals[pixel], s_vals[pixel], 1])
        if x is None:
            if g_vals[pixel]:
                x = np.array([np.linalg.solve(a, y)])
            else:
                x = np.array([[np.nan, np.nan, np.nan]])
        else:
            if g_vals[pixel]:
                x = np.append(x, [np.linalg.solve(a, y)], axis=0)
            else:
                x = np.append(x, np.array([[np.nan, np.nan, np.nan]]), axis=0)

    # Calculate the fractional bound values and reshape the resulting image
    fb = x[:, 1] / (x[:, 1] + x[:, 0])
    fb_im = np.array(fb).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))

    # fb_im = np.empty([3, np.shape(gs_im)[1], np.shape(gs_im)[2]])
    # fb_im[0, :, :] = np.array(x[:, 0]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))
    # fb_im[1, :, :] = np.array(x[:, 1]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))
    # fb_im[2, :, :] = np.array(x[:, 2]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))

    return fb_im

# Function to combine mitochondrial and cytosolic images
def combine_ims(path_to_fb_ims, filename):
    mito_fb = tifffile.imread(path_to_fb_ims+'/mito/'+filename)
    cyto_fb = tifffile.imread(path_to_fb_ims+'/cyto/'+filename)
    combo = np.nan_to_num(mito_fb) + np.nan_to_num(cyto_fb)
    return np.array(combo*65536).astype('uint16')
