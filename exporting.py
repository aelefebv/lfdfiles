import lfdfiles.lfdfiles
import os
import tifffile


def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def convert_r64_to_tiff(r64_path, file):
    output_path = r64_path + '/tif'
    check_and_make_dir(output_path)
    with lfdfiles.lfdfiles.SimfcsR64(r64_path + file) as f:
        f.totiff(output_path + file + '.tif')


def save_im(tif_path, file, im, output_folder_name):
    output_path = tif_path + output_folder_name
    check_and_make_dir(output_path)
    with tifffile.TiffWriter(output_path + '/' + file) as tif:
        tif.write(im, photometric='minisblack')
