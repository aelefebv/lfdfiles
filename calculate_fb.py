import tifffile
import numpy as np
import importing


def get_median_fb(path_to_fb_ims):
    fb_files = importing.get_filename_list(path_to_fb_ims, '*.tif')
    num_samples = importing.get_num_samples(fb_files, "CC0S_", 3)
    all_median_vals = []
    sample_median_vals = []
    frame_num = 0
    sample_num = 0
    all_sample_names = []
    for file in fb_files:
        frame_num_current, sample_name = importing.get_frame_number(file, "_$CC0S_", 3)
        if not frame_num_current:
            all_sample_names.append(sample_name)
            print(f"[INFO] getting median fb sample {sample_num + 1} of {num_samples}")
            sample_num += 1
        if frame_num_current < frame_num:
            all_median_vals.append(np.nanmean(sample_median_vals))
            sample_median_vals = []
            frame_num = 0
        else:
            fb_im = tifffile.imread(path_to_fb_ims+'/'+file)
            sample_median_vals.append(np.nanmedian(fb_im))
            frame_num += 1

    return all_median_vals, all_sample_names


def run(path, file):
    FREQUENCY = 80000000
    FREE_TAU = 0.4E-09
    BOUND_TAU = 3.4E-09

    omega = 2*np.pi*FREQUENCY
    g_free = 1/(1+(omega*FREE_TAU)**2)
    s_free = (omega*FREE_TAU)/(1+(omega*FREE_TAU)**2)
    g_bound = 1/(1+(omega*BOUND_TAU)**2)
    s_bound = (omega*BOUND_TAU)/(1+(omega*BOUND_TAU)**2)

    gs_im = tifffile.imread(path+'/'+file)
    g_vals = gs_im[0, :, :].flatten()
    s_vals = gs_im[1, :, :].flatten()

    a = np.array([[g_free, g_bound, 0],
                  [s_free, s_bound, 0],
                  [1, 1, 1]])

    x = None
    for pixel in range(np.size(g_vals)):

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

    fb = x[:, 1] / (x[:, 1] + x[:, 0])
    fb_im = np.array(fb).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))

    # fb_im = np.empty([3, np.shape(gs_im)[1], np.shape(gs_im)[2]])
    # fb_im[0, :, :] = np.array(x[:, 0]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))
    # fb_im[1, :, :] = np.array(x[:, 1]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))
    # fb_im[2, :, :] = np.array(x[:, 2]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))

    return fb_im
