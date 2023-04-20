import glob

# Function to get a list of filenames that match a pattern in a given path
def get_filename_list(path, pattern):
    # Get the sorted list of filenames that match the pattern
    filename_list = sorted(glob.glob1(path, pattern))
    return filename_list

# Function to extract the frame number and sample name from a given filename
def get_frame_number(filename, pattern_before_num, num_len):
    # Split the filename using the pattern_before_num
    split_text = filename.split(pattern_before_num)
    # Get the frame_number and sample_name from the split_text
    frame_number = split_text[1][0:num_len]
    sample_name = split_text[0]
    return int(frame_number), sample_name


# Function to count the number of samples in a list of files
def get_num_samples(filelist, pattern_before_num, num_len):
    sample_num = 1
    frame_num = 0
    # Iterate over the filelist
    for file in filelist:
        # Get the current frame number and sample name
        frame_num_current, _ = get_frame_number(file, pattern_before_num, num_len)
        # If the current frame number is less than the previous frame number,
        # it means we have a new sample
        if frame_num_current < frame_num:
            sample_num += 1
            frame_num = 0
        else:
            frame_num += 1
    return sample_num
