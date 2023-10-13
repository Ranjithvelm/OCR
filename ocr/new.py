from PIL import Image
import fitz  # PyMuPDF

def take_screenshots(input_pdf_path, blank_line_threshold=5):
    pdf_document = fitz.open(input_pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(alpha=False)  # Disable alpha channel for compatibility with PIL

        # Convert pix to a PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Iterate through the image to find paragraphs
        paragraph_start = None
        consecutive_blank_lines = 0

        for y in range(image.height):
            if all(image.getpixel((x, y)) == (255, 255, 255) for x in range(image.width)):
                consecutive_blank_lines += 1
                if consecutive_blank_lines >= blank_line_threshold:
                    if paragraph_start is not None:
                        paragraph_end = y - blank_line_threshold
                        paragraph_image = image.crop((0, paragraph_start, image.width, paragraph_end))
                        paragraph_image.save(f"output_folder/paragraph_page_{page_number+1}_para_{paragraph_start}.png")
                        paragraph_start = None
            else:
                if paragraph_start is None:
                    paragraph_start = y
                consecutive_blank_lines = 0

    pdf_document.close()

# Usage
take_screenshots('input.pdf', blank_line_threshold=5)
