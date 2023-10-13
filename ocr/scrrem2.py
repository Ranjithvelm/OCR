from PIL import Image
import fitz  # PyMuPDF

def take_screenshots(input_pdf_path):
    pdf_document = fitz.open(input_pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(alpha=False)  # Disable alpha channel for compatibility with PIL

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
                paragraph_image.save("output_folder/"f'paragraph_page_{page_number+1}_para_{paragraph_start}.png')
                paragraph_start = None

    pdf_document.close()

# Usage
take_screenshots('input.pdf')
