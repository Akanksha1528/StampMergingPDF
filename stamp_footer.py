import fitz  # PyMuPDF
import os
import re
import PyPDF2
from log_file import LeafletLogs

class LeafletStampingFooter:
    def __init__(self):
        pass 

    def detect_bates_stamping(self,text):        
        bates_pattern = re.compile(r'\d{6,8}')  # Bates numbers are often 6-8 digits long
        return bates_pattern.search(text) is not None
    
    def check_bates_stamping(self, page, page_num):        
        text_instances = page.get_text("dict")["blocks"]
        last_line=None
        last_prev_line=[]
        rect_last=None
        count=0
        try:
            for block in text_instances: 
                if "lines" in block:
                    for line in block["lines"]:
                        txt=page.get_text("text", clip=line["bbox"])       
                        #print(f'Line: {line["bbox"]} and text:{txt} ') 
                        last_prev_line.append(line["bbox"])                            
                        if last_line is None or line["bbox"][1] > last_line["bbox"][1]: 
                            last_line = line 

            count=len(last_prev_line)   
            if(count>0):
                lprev_val= page.get_text("text", clip=last_prev_line[count-2])      
            if last_line is None:                
                return None, rect_last
            rect_last=last_line['bbox']
            footer_text = page.get_text("text", clip=rect_last)
            cord_list= str(rect_last).replace('(',"").replace(')',"").split(',')          
            cord_vt=int(cord_list[1].split('.')[0])
            cord_vb=int(cord_list[3].split('.')[0])

            if self.detect_bates_stamping(footer_text) and cord_vt>750 and cord_vb>750:
                LeafletLogs.info(f"Page {page_num+1} likely contains Bates stamping.")
                #print(f"Page {page_num+1} likely contains Bates stamping.")
                return None, rect_last
            elif self.detect_bates_stamping(lprev_val) and cord_vt>750 and cord_vb>750:
                LeafletLogs.info(f"Page {page_num+1} likely contains Bates stamping.")
                #print(f"Page {page_num+1} likely contains Bates stamping.")
                return None, last_prev_line[count-2]
            elif footer_text is not None and len(footer_text)>0:
                LeafletLogs.info(f"Page {page_num+1} likely contains Other text :{len(footer_text)}.")
                return "vertical", rect_last
            else:
                LeafletLogs.info(f"Page {page_num+1} does not contain Bates stamping.")
                #print(f"Page {page_num+1} does not contain Bates stamping.")
                return "footer", rect_last
        except ValueError as e:
            LeafletLogs.info(f"Error:Exceptions: {e} ")
    
    def add_footer(self, input_pdf, output_pdf):
        LeafletLogs.info("Start stamping process.")
        pdf_document = fitz.open(input_pdf)
        file_name_only = os.path.splitext(os.path.basename(input_pdf))[0]
        cont=1
        try:
            for page_num in range(len(pdf_document)):
                page=pdf_document[page_num]                 
                formatted_number = str(cont).zfill(6)
                content= f"{file_name_only} - {formatted_number}"
                stampType, rect=self.check_bates_stamping(page,page_num)
                if stampType is None:
                    continue                
                elif stampType is None and rect is None: 
                    continue
                elif stampType in "vertical":
                    page=self.insert_vertical_bates_stamp(page, content)                    
                    LeafletLogs.info("Insert vertical bates stamp END.")
                elif stampType in "footer":
                    LeafletLogs.info("Insert Footer bates stamp process.")                    
                    page=self.insert_footer_bates_stamp(page,content,rect) 
                else:
                    return True
                cont=cont+1
        except ValueError as e:
            LeafletLogs.info(f"Error:Exceptions: {e} ")

        pdf_document.save(output_pdf)
        pdf_document.close()

        LeafletLogs.info(f"Stamping has been created for: {file_name_only}")
    
    def insert_vertical_bates_stamp(self,page, bates_number):
        LeafletLogs.info("Insert vertical bates stamp process.")
        x = page.rect.width - 10 
        y = page.rect.height / 3 
        rotation = 90 # Rotate text 90 degrees to make it vertical 
        page.insert_text( 
            point=(x, y), 
            text=bates_number,
            rotate=rotation, 
            fontsize=10, 
            fontname="helv", 
            color=(0, 0, 0) 
            )        
        LeafletLogs.info("Insert vertical bates stamp END.")
        return page
    
    def insert_footer_bates_stamp(self, page, text, rect):
        cord_list= str(rect).replace('(',"").replace(')',"").split(',')          
        x=int(cord_list[0].split('.')[0])
        y=int(cord_list[1].split('.')[0])
        if(y<750):
            y=750
        if(x<280):
            x=280
        page.insert_text((x,y), text, fontsize=10, fontname="helv")
        return page