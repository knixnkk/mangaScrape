import os
import PyPDF2
import random
def generate_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def generate_gradient(text):
    start_color = generate_random_color()
    end_color = generate_random_color()
    num_chars = len(text)
    color_diff = [(end - start) / num_chars for start, end in zip(start_color, end_color)]
    gradient_text = ""

    for i, char in enumerate(text):
        r = start_color[0] + int(color_diff[0] * i)
        g = start_color[1] + int(color_diff[1] * i)
        b = start_color[2] + int(color_diff[2] * i)
        gradient_text += f"\033[38;2;{r};{g};{b}m{char}\033[0m"

    return gradient_text

def merge_pdfs(input_folder, output_file):
    pdf_merger = PyPDF2.PdfMerger()
    pdf_files = [file for file in os.listdir(input_folder) if file.lower().endswith(".pdf")]
    sorted_image_paths = sorted(pdf_files, key=get_image_number)
    gradient_result = generate_gradient(sorted_image_paths)
    print(gradient_result)
    for pdf_file in sorted_image_paths:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_merger.append(pdf_path)

    with open(output_file, "wb") as output:
        pdf_merger.write(output)

    pdf_merger.close()

    for pdf_file in sorted_image_paths:
        pdf_path = os.path.join(input_folder, pdf_file)
        os.remove(pdf_path)

def get_all_files_in_folder(folder_path):
    file_paths = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    return file_paths
def concat(keys, values):
    my_dict = dict(zip(keys, values))
    return my_dict
def get_image_number(image_path):
    return int(image_path.split('/')[-1].split('.')[0])