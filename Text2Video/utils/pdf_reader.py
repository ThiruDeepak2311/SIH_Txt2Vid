from PyPDF2 import PdfReader
def PDF_Reader(pdf):
    # pdf=r'C:\Users\akash\OneDrive\Desktop\t2v\alexnet.pdf'
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    # print(text)
    return text


