import PyPDF2
import sys
### Local imports 
from log_file import LeafletLogs


class LeafletMergedPdf:
    def __init__(self):
      pass
     
    def merge_pdfs(self, pdf_list, output_pdf):
      LeafletLogs.info(f"List of merged files: {pdf_list}")    
      try:          
          writer = PyPDF2.PdfWriter()          
          for pdf in pdf_list:
              reader = PyPDF2.PdfReader(pdf)
              for page in reader.pages:
                  writer.add_page(page)
          
          with open(output_pdf, "wb") as out_pdf:
              writer.write(out_pdf)
      except ValueError as e:
          LeafletLogs.info(f"Error:Exceptions: {ex} ")
        