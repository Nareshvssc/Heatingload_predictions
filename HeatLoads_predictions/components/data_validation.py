from HeatLoads_predictions.logger import logging
from HeatLoads_predictions.exception import HeatLoadsException
from HeatLoads_predictions.entity.config_entity import DataValidationConfig
from HeatLoads_predictions.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
import pandas  as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
from HeatLoads_predictions.utils.utils import read_yaml_file
from HeatLoads_predictions.constants import *

class DataValidation:
    

    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HeatLoadsException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_excel(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_excel(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise HeatLoadsException(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    def data_validate(self,path,config):
        try:
            column_key_validation_status = False
            logging.info(f"logging data from: {path} ")
            dataframe = pd.read_excel(path)
            logging.info(f"reading the yaml file from {config.schema_file_path}")
            schema_file_config = read_yaml_file(config.schema_file_path)
            columns_in_schema = list(schema_file_config[DATA_VALIDATION_SCHEMA_KEY].keys())
            for i,column_name in enumerate(dataframe.columns):
                if columns_in_schema[i]!=column_name:
                    logging.info(f"The columns in schema doesnt match || {columns_in_schema[i]} and || {column_name} ")
                    column_key_validation_status = False
                    break
                else:
                    logging.info(f"The columns in schema  match || {columns_in_schema[i]} and || {column_name} ")
            else:
                column_key_validation_status = True

            logging.info(f"checking for domain values in X4 , X5 ,X6 , X7 , X8 ")
            categorical_columns_list = schema_file_config[DATA_VALIDATION_CATEGORICAL_KEY]
            domain_val_count = []
            domain_val_status = None
            for variable in categorical_columns_list:
                value_in_var = schema_file_config[DATA_VALIDATION_DOMAIN_KEY][variable]
                value_in_df = list(dataframe[variable].unique())
                domain_val_count.extend([False for first in value_in_df if first not in value_in_var])
            if len(domain_val_count)==0:
                domain_val_status = True
                logging.info(f"checked values and no. of counts of values in categorical columns is same ")
            else:
                domain_val_status = False
                logging.info(f"checked values and no. of counts of values in categorical columns is not same ")

            if column_key_validation_status and domain_val_status:
                return True 
            else:
                return False   
        except Exception as e:
            raise HeatLoadsException(e,sys) from e    

    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            train_file_path = self.data_ingestion_artifact.train_file_path
            train_validate_status = self.data_validate(train_file_path,self.data_validation_config)
            test_file_path = self.data_ingestion_artifact.test_file_path
            test_validate_status = self.data_validate(test_file_path,self.data_validation_config)

            if train_validate_status and test_validate_status:
                logging.info("Both validated and schema is validated.............>>>")
                return True
            else:
                return False
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

