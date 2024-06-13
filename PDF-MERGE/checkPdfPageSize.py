import PyPDF2

def check_pdf_page_size(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            page = reader.pages[i]
            width = page.mediabox.width / 72  # Convert from points to inches
            height = page.mediabox.height / 72  # Convert from points to inches
            print(f"Page {i + 1} size: {width:.3f} x {height:.3f} inches")

pdf_path = 'books/1/book.pdf'  # Replace with your PDF file path
check_pdf_page_size(pdf_path)
