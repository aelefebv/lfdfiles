import importing
import exporting
import mito_segmentation
import apply_mask
import calculate_gs
import calculate_fb
import export_gs_coords
import csv
from datetime import datetime


def run_conversion(path):
    all_files = importing.get_filename_list(path, '*.R64')
    file_num = 0
    for file in all_files:
        print(f"[INFO] exporting file {file_num + 1} of {len(all_files)}")
        exporting.convert_r64_to_tiff(path, file)
        file_num += 1


def run_segmentation(path):
    all_files = importing.get_filename_list(path, '*ch2*.tif')
    file_num = 0
    for file in all_files:  # 0:5 for testing
        print(f"[INFO] segmenting file {file_num+1} of {len(all_files)}")
        mito_mask, cyto_mask = mito_segmentation.run_segmentation(path, file)
        exporting.save_im(path, file, mito_mask, '/segmented/mito')
        exporting.save_im(path, file, cyto_mask, '/segmented/cyto')
        file_num += 1


def run_masking(path):
    MED_FILTER_SIZE = 0

    mask_path = path + '/segmented'
    ch1_files = importing.get_filename_list(path, '*ch1*.tif')
    mito_mask_files = importing.get_filename_list(mask_path+'/mito', '*ch2*.tif')
    cyto_mask_files = importing.get_filename_list(mask_path+'/cyto', '*ch2*.tif')
    for file_num in range(len(ch1_files)):
        print(f"[INFO] masking file {file_num+1} of {len(ch1_files)}")
        mito_masked_phase_and_mod = apply_mask.mask_ch1(path, mask_path+'/mito',
                                                        ch1_files[file_num], mito_mask_files[file_num],
                                                        MED_FILTER_SIZE)
        cyto_masked_phase_and_mod = apply_mask.mask_ch1(path, mask_path+'/cyto', ch1_files[file_num],
                                                        cyto_mask_files[file_num],
                                                        MED_FILTER_SIZE)
        exporting.save_im(path, ch1_files[file_num], mito_masked_phase_and_mod, '/masked/mito')
        exporting.save_im(path, ch1_files[file_num], cyto_masked_phase_and_mod, '/masked/cyto')


def run_gs_calculation(path):
    mask_path = path + '/masked'
    mito_mask_files = importing.get_filename_list(mask_path+'/mito', '*.tif')
    cyto_mask_files = importing.get_filename_list(mask_path+'/cyto', '*.tif')
    file_num = 0
    for file in mito_mask_files:
        print(f"[INFO] calculating gs file {file_num+1} of {len(mito_mask_files)}")
        mito_gs_im = calculate_gs.run(mask_path+'/mito', file)
        cyto_gs_im = calculate_gs.run(mask_path+'/cyto', file)
        exporting.save_im(path, file, mito_gs_im, '/gs/mito')
        exporting.save_im(path, file, cyto_gs_im, '/gs/cyto')
        file_num += 1


def run_fb_calculation(path):
    gs_path = path + '/gs'
    mito_gs_files = importing.get_filename_list(gs_path+'/mito', '*.tif')
    cyto_gs_files = importing.get_filename_list(gs_path+'/cyto', '*.tif')
    file_num = 0
    for file in mito_gs_files:
        print(f"[INFO] calculating fb file {file_num+1} of {len(mito_gs_files)}")
        mito_fb_im = calculate_fb.run(gs_path+'/mito', file)
        cyto_fb_im = calculate_fb.run(gs_path+'/cyto', file)
        exporting.save_im(path, file, mito_fb_im, '/fb/mito')
        exporting.save_im(path, file, cyto_fb_im, '/fb/cyto')
        file_num += 1


def get_mean_fb(path):
    path_to_fb_ims = path + '/fb'
    mito_mean_fb, mito_sample_names = calculate_fb.get_median_fb(path_to_fb_ims+'/mito')
    cyto_mean_fb, cyto_sample_names = calculate_fb.get_median_fb(path_to_fb_ims+'/cyto')
    print("[INFO] exporting bound fraction to csv...")
    rn = datetime.today().strftime('%Y%m%d%H%M%S')
    with open(path_to_fb_ims + '/' + rn + '_mito_mean_fb.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(mito_sample_names, mito_mean_fb))
    with open(path_to_fb_ims + '/' + rn + '_cyto_mean_fb.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(cyto_sample_names, cyto_mean_fb))
    print(f"[INFO] csv of bound fraction saved to {path_to_fb_ims}/.")


def export_gs(path):
    path_to_gs_ims = path + '/gs'
    g_coords_c, s_coords_c, sample_names_c = export_gs_coords.get_median_gs(path_to_gs_ims+'/cyto')
    g_coords_m, s_coords_m, sample_names_m = export_gs_coords.get_median_gs(path_to_gs_ims+'/mito')
    print("[INFO] export gs coordinates to csv...")
    rn = datetime.today().strftime('%Y%m%d%H%M%S')
    with open(path_to_gs_ims + '/' + rn + '_cyto_gs_coords.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(sample_names_c, g_coords_c, s_coords_c))
    with open(path_to_gs_ims + '/' + rn + '_mito_gs_coords.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(sample_names_m, g_coords_m, s_coords_m))
    print(f"[INFO] csv of gs coords saved to {path_to_gs_ims}/.")


def create_colormap_images(path):
    fb_path = path+'/fb'
    files = importing.get_filename_list(fb_path+'/mito', '*.tif')
    num_files = 0
    for file in files:
        print(f"[INFO] creating colormap file {num_files+1} of {len(files)}")
        combo = calculate_fb.combine_ims(fb_path, file)
        print(combo.shape)
        exporting.save_im(path, file, combo, '/combo')
        num_files += 1


def run():
    RUN_CONVERSION = False
    RUN_MITO_SEGMENTATION = False
    MASK_PHASE_MOD = False
    GET_GS_IMAGE = False
    CALCULATE_FRACTION_BOUND = False
    GET_MEAN_FB = False
    CREATE_FULL_COLORMAP = False
    EXPORT_GS_COORDS = True

    path = '/Users/austin/Documents/Collaborations/Franco/Austin_Kevin_Tharp'

    if RUN_CONVERSION:
        run_conversion(path + '/R64')

    path_to_tifs = path + '/tif'
    if RUN_MITO_SEGMENTATION:
        run_segmentation(path_to_tifs)

    if MASK_PHASE_MOD:
        run_masking(path_to_tifs)

    if GET_GS_IMAGE:
        run_gs_calculation(path_to_tifs)

    if CALCULATE_FRACTION_BOUND:
        run_fb_calculation(path_to_tifs)

    if GET_MEAN_FB:
        get_mean_fb(path_to_tifs)

    if CREATE_FULL_COLORMAP:
        # create_colormap_images(path_to_tifs)
        calculate_fb.get_median_stack(path_to_tifs+'/combo')

    if EXPORT_GS_COORDS:
        export_gs(path_to_tifs)


if __name__ == '__main__':
    run()
