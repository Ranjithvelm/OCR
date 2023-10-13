from PIL import Image
import fitz  # PyMuPDF
import os

def take_screenshots(input_pdf_path, output_folder):
    pdf_document = fitz.open(input_pdf_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        
        # Set DPI to increase image quality (e.g., 300 DPI)
        pix = page.get_pixmap(matrix=fitz.Matrix(250/72, 250/72))  # 300 DPI

        # Convert pix to a PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Initialize flags and variables
        paragraph_start = None
        in_paragraph = False
        blank_space_found = False

        for y in range(image.height):
            # Check for blank space (more than 90% white pixels)
            if sum(1 for x in range(image.width) if image.getpixel((x, y))[:3] == (255, 255, 255)) / image.width > 0.9:
                if not in_paragraph:
                    paragraph_start = y
                    in_paragraph = True
                    blank_space_found = True
            else:
                if in_paragraph and blank_space_found:
                    paragraph_end = y
                    paragraph_image = image.crop((0, paragraph_start, image.width, paragraph_end))
                    paragraph_image.save(os.path.join(output_folder, f'paragraph_page_{page_number+1}_para_{paragraph_start}.png'))
                    in_paragraph = False
                    blank_space_found = False

    pdf_document.close()

# Usage
take_screenshots('input.pdf', 'output_folder')
