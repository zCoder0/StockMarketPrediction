from src.logging import logger
import sys


class ProjectException(Exception):
    
    def __init__(self,error_msg,error_details:sys):
        
        self.error_msg = error_msg
        _,_,exc_tb = error_details.exc_info()
        
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        
        logger.logging.info(self.__str__())
        
    
    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name,
            self.lineno,
            self.error_msg
        )