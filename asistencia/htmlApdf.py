from xhtml2pdf import xhtml2pdf

def htmlToPdf(html, pdfFile):
    """
    Converts HTML content to a PDF file.

    :param html: The HTML content to convert.
    :param pdfFile: The path where the PDF file will be saved.
    """
    try:
        # Create a PDF from the HTML content
        pdf = xhtml2pdf.pisa.CreatePDF(html, dest=pdfFile)
        
        # Check if there were any errors during the conversion
        if pdf.err:
            raise Exception("Error converting HTML to PDF")
    except Exception as e:
        print(f"An error occurred while converting HTML to PDF: {e}")
        raise