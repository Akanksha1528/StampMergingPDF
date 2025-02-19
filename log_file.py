
from datetime import datetime


class LeafletLogs:
    file_path = ""

    @classmethod
    def initialize(cls, value):
        cls.file_path = value
    
    @classmethod
    def info(cls, msg):
        content_to_write = f"{datetime.now().time()}: \t   {msg} \n"
        with open(LeafletLogs.file_path, 'a') as file:
            file.write(content_to_write)
    


