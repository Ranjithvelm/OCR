from PIL import Image
import fitz  # PyMuPDF

def take_question_screenshots(input_pdf_path):
    pdf_document = fitz.open(input_pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)  # Set DPI by adjusting the matrix

        # Convert pix to a PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Initialize variables to track question position
        question_start = None
        question_end = None

        # Define threshold for blank space (adjust as needed)
        blank_space_threshold = 10 # Adjust this value based on your PDF layout

        # Iterate through the image to find the question
        for y in range(image.height):
            if all(image.getpixel((x, y)) == (255, 255, 255) for x in range(image.width)):
                if question_start is None:
                    question_start = y
            elif question_start is not None:
                if y - question_start > blank_space_threshold:
                    question_end = y
                    break

        if question_start is not None and question_end is not None:
            # Define the rectangle for the question
            question_rect = (0, question_start, image.width, question_end)

            # Crop the question section
            question_image = image.crop(question_rect)

            # Save the question section
            question_image.save(f"output_folder/"f'question_page_{page_number+1}.png', dpi=(300, 300), format='png')  # Adjust DPI and use PNG format

    pdf_document.close()

# Usage
take_question_screenshots('input.pdf')
