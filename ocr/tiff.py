from wand.image import Image

def convert_pdf_to_tiff(input_pdf, output_folder):
    with Image(filename=input_pdf, resolution=300) as pdf:
        for i, page in enumerate(pdf.sequence):
            with Image(page) as img:
                img.save(filename=f'{output_folder}/page_{i + 1}.tiff')

# Example usage
input_pdf = 'input.pdf'
output_folder = 'output_folder'

# Create output folder if it doesn't exist
import os
os.makedirs(output_folder, exist_ok=True)

convert_pdf_to_tiff(input_pdf, output_folder)
