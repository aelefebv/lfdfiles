import lfdfiles.lfdfiles
import os
import tifffile


# Function to check if a directory exists and create it if it doesn't
def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Function to convert a .r64 file to a .tiff file
def convert_r64_to_tiff(r64_path, file):
    # Create the output directory if it doesn't exist
    output_path = r64_path + '/tif'
    check_and_make_dir(output_path)
    # Read the .r64 file and convert it to .tiff
    with lfdfiles.lfdfiles.SimfcsR64(r64_path + file) as f:
        f.totiff(output_path + file + '.tif')


# Function to save an image in a specified output folder
def save_im(tif_path, file, im, output_folder_name):
    # Create the output directory if it doesn't exist
    output_path = tif_path + output_folder_name
    check_and_make_dir(output_path)
    # Save the image as a .tif file
    with tifffile.TiffWriter(output_path + '/' + file) as tif:
        tif.write(im, photometric='minisblack')
