import sys
class HeatLoadsException(Exception):
    def __init__(self,error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.message = HeatLoadsException.get_message(error_message,error_details)
   
    @staticmethod
    def get_message(error_message,error_details)->str:
        _,_,exec_tb = error_details.exc_info()
        exception_block_line_number = exec_tb.tb_frame.f_lineno
        try_block_line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"error occured in script: [{file_name}] at try blocknumber [{try_block_line_number}] and exception raised from line number [{exception_block_line_number}]"
        return error_message
    
    #def __str__(self):
        #return "hello this is petrol prices object"
        
    #def __repr__(self):
        #return HeatLoadsException.__name__.str()