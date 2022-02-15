import importing
import tifffile
import numpy as np


def get_median_gs(path_to_gs_ims):
    gs_files = importing.get_filename_list(path_to_gs_ims, '*.tif')
    num_samples = importing.get_num_samples(gs_files, "CC0S_", 3)
    all_g_median_vals = []
    all_s_median_vals = []
    g_median_vals = []
    s_median_vals = []
    frame_num = 0
    sample_num = 0
    all_sample_names = []
    for file in gs_files:
        frame_num_current, sample_name = importing.get_frame_number(file, "_$CC0S_", 3)
        if not frame_num_current:
            all_sample_names.append(sample_name)
            print(f"[INFO] getting median gs of sample {sample_num + 1} of {num_samples}")
            sample_num += 1
        if frame_num_current < frame_num:
            all_g_median_vals.append(np.nanmean(g_median_vals))
            all_s_median_vals.append(np.nanmean(s_median_vals))
            g_median_vals = []
            s_median_vals = []
            frame_num = 0
        else:
            gs_im = tifffile.imread(path_to_gs_ims+'/'+file)
            g_im = gs_im[0, :, :]
            s_im = gs_im[1, :, :]
            g_non0 = g_im[g_im != 0]
            s_non0 = s_im[s_im != 0]
            g_median_vals.append(np.nanmedian(g_non0))
            s_median_vals.append(np.nanmedian(s_non0))
            frame_num += 1

    return all_g_median_vals, all_s_median_vals, all_sample_names
