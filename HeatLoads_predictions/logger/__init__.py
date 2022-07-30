import logging
import os
from datetime import datetime
import pandas as pd 
from HeatLoads_predictions.constants import get_current_time_stamp


LOG_DIR="HeatLoadsLogs"

def get_log_file_name():
    return f"log_{get_current_time_stamp()}.log"


LOG_FILE_NAME=get_log_file_name()

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)

os.makedirs(LOG_DIR,exist_ok=True)

file_name = get_log_file_name()

log_file_path = os.path.join(LOG_DIR,file_name) 


logging.basicConfig(
filename=log_file_path,
filemode="w",
level= logging.INFO,
format=f"%(asctime)s||%(levelname)s||%(lineno)d||%(filename)s||%(funcName)s||%(message)s "
)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("||"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]