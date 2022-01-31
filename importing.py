import glob


def get_filename_list(path, pattern):
    filename_list = sorted(glob.glob1(path, pattern))
    return filename_list
