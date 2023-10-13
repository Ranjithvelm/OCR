from PIL import Image
import fitz  # PyMuPDF

def take_screenshots(input_pdf_path, blank_space_size):
    pdf_document = fitz.open(input_pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)  # Set DPI by adjusting the matrix

        # Convert pix to a PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Iterate through the image to find paragraphs
        paragraph_start = None

        for y in range(image.height):
            if any(image.getpixel((x, y)) != (255, 255, 255) for x in range(image.width)):
                if paragraph_start is None:
                    paragraph_start = y
            elif paragraph_start is not None:
                paragraph_end = y
                paragraph_image = image.crop((0, paragraph_start, image.width, paragraph_end))
                paragraph_image.save(f"output_folder/"f'paragraph_page_{page_number+1}_para_{paragraph_start}.png', dpi=(300, 300), format='png')  # Adjust DPI and use PNG format
                paragraph_start = None

        # Add a blank space after each paragraph
        if paragraph_start is not None:
            paragraph_end = min(paragraph_start + blank_space_size, image.height)
            paragraph_image = image.crop((0, paragraph_start, image.width, paragraph_end))
            paragraph_image.save(f"output_folder/"f'paragraph_page_{page_number+1}_para_{paragraph_start}.png', dpi=(300, 300), format='png')  # Adjust DPI and use PNG format

    pdf_document.close()

# Usage
blank_space_size = int(input("Enter the size of the blank space: "))
take_screenshots('input.pdf', blank_space_size)


