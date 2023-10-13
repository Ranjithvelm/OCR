from PIL import Image
import fitz  # PyMuPDF

def take_screenshots(input_pdf_path):
    pdf_document = fitz.open(input_pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(5, 5), alpha=False)
        v = []
        # Convert pix to a PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        for i in range(image.width):
            for j in range(image.height):
                k = image.getpixel((i,j))
                v.append(k)
    pp = set(v)
    ppp = list(pp)
    

take_screenshots('input.pdf')