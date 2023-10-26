if __name__ != "__main__":
    from .pract_funcs import *

import os


def rename_files(desired_name="new_file_", num_digits=3, source_ext="txt", target_ext="doc", name_range=None):
    if not os.path.exists(test_folder):
        print(f"Директория {test_folder} не найдена")
        return
    
    backDir = os.getcwd()
    os.chdir(test_folder)
    
    try:
        fileCount = 1
        for file in os.listdir().sort():
            name, ext = os.path.splitext(file)
            if ext[1:] == source_ext:
                name = (name[name_range[0]-1:name_range[1]] if name_range else "") + desired_name
                name += str(fileCount).zfill(num_digits)
                os.rename(file, name + "." + target_ext)
                fileCount += 1
    finally:
        os.chdir(backDir)


if __name__ == "__main__":
    from pprint import pprint
    from pract_funcs import test_folder
    
    pprint(list(os.walk(test_folder)))
