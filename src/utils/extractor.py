import pymupdf4llm

def extract_pdf(prFilePath):
    vrPDF = pymupdf4llm.to_markdown(prFilePath)
    return vrPDF

def extract_text(prFilePath):
    with open(prFilePath, 'r', encoding="utf-8") as file:
        vrText = file.read()

    return vrText