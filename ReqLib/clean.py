from mics import concat, get_all_files_in_folder, merge_pdfs
import os
path = ["chapter/", "images/", "pdf/"]
for i in path:
    files = get_all_files_in_folder(i)
    for files_path in files:
        print(f"Deleteing {files_path}")
        os.remove(files_path)