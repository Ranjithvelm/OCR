from pdf2image import convert_from_path
from PIL import Image
import img2pdf
import os

def get_file_paths(folder_name):
    file_paths = []
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def split_pages(input_pdf, output_folder):
    images = convert_from_path(input_pdf, dpi=300)
    j = 0
    for i, image in enumerate(images):
        width, height = image.size
        left_half = image.crop((0, 0, width/2, height))
        right_half = image.crop((width/2, 0, width, height))

        left_half.save(os.path.join(output_folder, f"temp_page_{j}.png"), "PNG")
        right_half.save(os.path.join(output_folder, f"temp_page_{j+1}.png"), "PNG")
        j += 2

def merge_images_to_pdf(output_folder, output_pdf):
    with open(output_pdf, "wb") as pdf_file:
        image_paths = [os.path.join(output_folder, f"temp_page_{i}.png") for i in range(len(os.listdir(output_folder))-1)]
        # print(type(image_list))
        image_list = []
        for path in image_paths:
            with open(path, "rb") as image_file:
                image_list.append(image_file.read())
        pdf_file.write(img2pdf.convert(image_list))

if __name__ == "__main__":
    folder_name = "Aptitude"  # Replace with the actual folder name
    file_paths = get_file_paths(folder_name)
    file_paths = list(filter(lambda x: x != 'Aptitude/.DS_Store', file_paths))
    print(file_paths)
    for path in file_paths:
        input_pdf = path
        part_name = input_pdf.split("/")[1]
        parts = part_name.split(".")[0]
        os.makedirs(parts)
        output_folder = parts
        output_pdf = part_name

        split_pages(input_pdf, output_folder)
        merge_images_to_pdf(output_folder, output_pdf)


