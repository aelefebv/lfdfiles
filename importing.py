import glob


def get_filename_list(path, pattern):
    filename_list = sorted(glob.glob1(path, pattern))
    return filename_list


def get_frame_number(filename, pattern_before_num, num_len):
    split_text = filename.split(pattern_before_num)
    frame_number = split_text[1][0:num_len]
    sample_name = split_text[0]
    return int(frame_number), sample_name


def get_num_samples(filelist, pattern_before_num, num_len):
    sample_num = 1
    frame_num = 0
    for file in filelist:
        frame_num_current, _ = get_frame_number(file, pattern_before_num, num_len)
        if frame_num_current < frame_num:
            sample_num += 1
            frame_num = 0
        else:
            frame_num += 1
    return sample_num
