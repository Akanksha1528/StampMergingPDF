import json
import os
from log_file import LeafletLogs

class PretrainedInfoClass:
    def __init__(self):
        pass

    def matterId_path(self, jsonPath, case_name, matter_id):
        with open(jsonPath, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        matter_paths = [item["matterPath"] for item in data]
        if(len(matter_paths) <=0):
            return ""
        for mp in matter_paths:
            mid =self.read_info_file(mp, "Matterinfo.txt")
            if(mid == str(matter_id)):
                return mp
        
        return ""
            

    def find_pretrained_info(self, jsonPath, case_name):
        data=None
        with open(jsonPath, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            if item['caseName'].lower().startswith(case_name.lower()):
                 return  item["filePath"], item["matterPath"]               
            print(f"Key: {item['caseName']} Value: ")

        return "", ""        

    def read_info_file(self, dirpath, file_name):
        file_path = os.path.join(dirpath, file_name)
        content = ""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()   
        
        return content
        