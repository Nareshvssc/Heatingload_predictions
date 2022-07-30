
from HeatLoads_predictions.exception import HeatLoadsException
from HeatLoads_predictions.logger import logging
from HeatLoads_predictions.entity.config_entity import DataIngestionConfig
from HeatLoads_predictions.entity.artifact_entity import DataIngestionArtifact
import os
import sys 
import urllib
import requests
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import tarfile

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data ingestion log started.{'='*20 }")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    
    def download_heatload_data(self):
        try:
            #download the url in the variable from data_ingestion_config
            download_url = self.data_ingestion_config.dataset_download_url
            # getting the folder location where the download file will be stored 
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir,exist_ok=True)
            #filename of the file which is being downloaded
            heatload_file_name = os.path.basename(download_url)
            raw_data_file_path = os.path.join(raw_data_dir,heatload_file_name)
            logging.info(f"downloading file from :[{download_url}] in the directory [{raw_data_file_path}]")
            urllib.request.urlretrieve(download_url,raw_data_file_path)
            logging.info(f"download completed at :[{raw_data_file_path}] successfully ")
            return raw_data_file_path
        except Exception as e:
            raise HeatLoadsException(e,sys) from e
    


    def split_data_as_train_test(self):
        try:
            train_data_dir = self.data_ingestion_config.ingested_train_dir
            test_data_dir = self.data_ingestion_config.ingested_test_dir
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            heatload_file_path = os.path.join(raw_data_dir,file_name)
            logging.info(f"reading file from folder directory {heatload_file_path}")
            heatload_df = pd.read_excel(heatload_file_path,engine='openpyxl').drop(labels='X2',axis=1)
            split = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
            strat_train_data=None
            strat_test_data = None
            logging.info(f"Based on Orientation i.e X5 variable splitting the dataset ")
            for train_index,test_index in split.split(heatload_df,heatload_df["X5"]):
                strat_train_data = heatload_df.loc[train_index]
                strat_test_data = heatload_df.loc[test_index]
            train_file_path = os.path.join(train_data_dir,file_name)
            test_file_path = os.path.join(test_data_dir,file_name)
            if strat_train_data is not None:
                os.makedirs(train_data_dir,exist_ok=True)
                strat_train_data.to_excel(train_file_path,index=False)
            if strat_test_data is not None:
                os.makedirs(test_data_dir,exist_ok=True)
                strat_test_data.to_excel(test_file_path,index=False)    
            data_ingestion_artifact = DataIngestionArtifact(train_file_path= train_file_path,test_file_path= test_file_path,is_ingested=True,message='the ingestion has happened')
            logging.info(f"Data ingestion artifact returned {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise HeatLoadsException(e,sys) from e       
        

    def initiate_data_ingestion(self):
        try:
            raw_file_path = self.download_heatload_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise HeatLoadsException(e,sys) from e