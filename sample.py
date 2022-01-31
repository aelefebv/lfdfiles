import importing
import exporting
import mito_segmentation
import apply_mask
import calculate_gs


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
        mito_mask = mito_segmentation.run_segmentation(path, file)
        exporting.save_im(path, file, mito_mask, '/segmented')
        file_num += 1


def run_masking(path):
    mask_path = path + '/segmented'
    ch1_files = importing.get_filename_list(path, '*ch1*.tif')
    mask_files = importing.get_filename_list(mask_path, '*ch2*.tif')
    for file_num in range(len(ch1_files)):
        print(f"[INFO] masking file {file_num+1} of {len(ch1_files)}")
        masked_phase_and_mod = apply_mask.mask_ch1(path, mask_path, ch1_files[file_num], mask_files[file_num])
        exporting.save_im(path, ch1_files[file_num], masked_phase_and_mod, '/masked')


def run_gs_calculation(path):
    gs_path = path + '/gs'
    mask_path = path + '/segmented'
    mask_files = importing.get_filename_list(mask_path, '*.tif')
    file_num = 0
    for file in mask_files:
        print(f"[INFO] masking file {file_num+1} of {len(ch1_files)}")
        gs_file = calculate_gs.run(path, file)
        exporting.save_im(path, file, gs_file, '/gs')
        file_num += 1

def run():
    RUN_CONVERSION = False
    RUN_MITO_SEGMENTATION = False
    MASK_PHASE_MOD = False
    GET_GS_IMAGE = True
    CALCULATE_FRACTION_BOUND = True

    PATH_TO_R64 = '/Users/austin/Documents/Collaborations/Franco/Austin_Kevin_Tharp'
    if RUN_CONVERSION:
        run_conversion(PATH_TO_R64)

    PATH_TO_TIFS = PATH_TO_R64 + '/tif'
    if RUN_MITO_SEGMENTATION:
        run_segmentation(PATH_TO_TIFS)

    if MASK_PHASE_MOD:
        run_masking(PATH_TO_TIFS)

    if GET_GS_IMAGE:
        run_gs_calculation(PATH_TO_TIFS)


if __name__ == '__main__':
    run()
