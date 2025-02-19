
import json
import sys
import os
import shutil
#### Local import 
from stamp_footer import LeafletStampingFooter
from merge_pdf import LeafletMergedPdf
from log_file import LeafletLogs
#from pretrainTest import PretrainedInfoClass

####------11-FEB-2025--------PreTrained File Check for Demo Requirement----------------#####


def pretrained_file(jsonpath):
    jsondata = get_json_data(jsonpath)    
    out_pdf = jsondata["outFile"]
    filename=os.path.basename(out_pdf).strip()
    LeafletLogs.info(f"filename: {filename}")
    #pretrainedinfo=r"f:\AmazonShare\PreTrainedOCR\PreTrainedInfo.json"
    pretrainedinfo=r"C:\Users\leaflet_vba_delhi\Desktop\AmazonShare\PreTrainedOCR\PreTrainedInfo.json"
    if (os.path.exists(pretrainedinfo)==False):
        LeafletLogs.info(f" pretrainedinfo Path: {pretrainedinfo} does'not exists. ") 

    file_extension = os.path.splitext(filename)[0]
    pre_matterpath=find_pretrained_info(pretrainedinfo,file_extension.lower())
    LeafletLogs.info(f" pre_matterpath: {pre_matterpath} pretrainedinfo: {pretrainedinfo}")  
    if(len(pre_matterpath)==0):
        return False
    
    filepath=os.path.join(pre_matterpath, "combined.pdf")
    LeafletLogs.info(f" filename: {filename}")           
    LeafletLogs.info(f" filepath: {filepath}")
    shutil.copy(filepath, out_pdf)
    LeafletLogs.info(f" Copy Sucess")
    return True

def find_pretrained_info(jsonPath, case_name):
    data=None
    LeafletLogs.info(f"jsonPath: {jsonPath}")
    with open(jsonPath, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    LeafletLogs.info(f"CaseName: {case_name} data: {len(data)}")
    for item in data:
        LeafletLogs.info(f"-----{item.get('caseName')}")
        jcName=str(item.get('caseName'))      
        
        #if jcName.lower().startswith(case_name.lower()):
        if case_name[:len(jcName)].lower() == jcName.lower():
            LeafletLogs.info("Matched Case Name")
            return str(item.get('matterPath'))          
        
    return "" 

def write_text_file(file_path, total_pages):
    file = open(file_path, 'w')
    file.write(total_pages)
    file.close()

def get_json_data(file_path):
    data = None
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data


def run(file_path):
    parent_directory = os.path.dirname(file_path)
    page_count_file = os.path.join(parent_directory,  "pagecount.txt")
    LeafletLogs.info(" Before start_process")
    try:
        ispretrained=pretrained_file(file_path)
        LeafletLogs.info(f"Pretrained File: {ispretrained}")
        if ispretrained == False:
            start_process(file_path)
    except ValueError as e:
          LeafletLogs.info(f"Error:Exceptions: {e} ")        
    finally:
        LeafletLogs.info("Finally completed run process")
        write_text_file(page_count_file, "completed.txt")
    
    
def start_process(file_path):
    out_pdf = ""
    LeafletLogs.info("Start_process has been invoke.")
    try:            
        jsondata = get_json_data(file_path)    
        out_pdf = jsondata["outFile"]
        input_files = jsondata["inputFiles"]
        current_file = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_file)
        file_name = os.path.basename(file_path)
        #stamp_file_path = get_stamp_blank_path(file_path)
        objStamp = LeafletStampingFooter()
        objMerged = LeafletMergedPdf()
        output_stamp_files = []
        LeafletLogs.info("Start Collecting file paths")
        for fl in input_files:
            parent_directory = os.path.dirname(fl)
            file_name = "out_" + os.path.basename(fl)
            outfile = os.path.join(parent_directory,  file_name)
            output_stamp_files.append(outfile)

        length = len(input_files)
        LeafletLogs.info(f"Total inputs files : {length}")
        for i in range(0,length):
            content_pdf = input_files[i]
            pdf_result = output_stamp_files[i]
            isStamp= objStamp.add_footer(content_pdf, pdf_result)    
            if isStamp:    
                output_stamp_files.remove(pdf_result)
                output_stamp_files.append(input_files[i])              
        
        LeafletLogs.info("Stamping process completed.")
        
        if(len(output_stamp_files)==0):
            LeafletLogs.info(f"output_stamp_files is empty.")
        else:
            objMerged.merge_pdfs(output_stamp_files, out_pdf)

        LeafletLogs.info(f"start_proceess completed : outpdf: {out_pdf}")
        return out_pdf
        
    except ValueError as e:
        LeafletLogs.info(f"Error:Exceptions: {e} ")
        return out_pdf

        

def get_stamp_blank_path(file_path):
    parent_directory = os.path.dirname(file_path)
    stamp_file_path = os.path.join(parent_directory,  "stamp.pdf")
    return stamp_file_path

def set_log_filepath(file_path):
    parent_directory = os.path.dirname(file_path)
    log_file = os.path.join(parent_directory,  "log.txt")
    return log_file
    

if __name__ == '__main__': 
  arguments = sys.argv
  file_path = r"E:\Downloads\CODES\fff.json"
  file_path = arguments[1] 
  log_path = set_log_filepath(file_path) 
  LeafletLogs.initialize(log_path)
  LeafletLogs.info("====================== Begin process ===============")
  LeafletLogs.info("####------11-FEB-2025--------PreTrained File Check for Demo Requirement----------------#####")
  result=run(file_path)
  LeafletLogs.info("================== Completed process ===============")
