import importing
import exporting


def run():
    PATH_TO_R64 = '/Users/austin/Documents/Collaborations/Franco/Austin_Kevin_Tharp/'
    all_files = importing.get_filename_list(PATH_TO_R64, '*.R64')
    file_num = 0
    for file in all_files:
        print(f"exporting file {file_num + 1} of {len(all_files)}")
        exporting.convert_r64_to_tiff(PATH_TO_R64, file)
        file_num += 1


if __name__ == '__main__':
    run()
