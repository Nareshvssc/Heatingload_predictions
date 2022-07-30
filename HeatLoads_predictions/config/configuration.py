from pyexpat import model
from time import time
import sys
from HeatLoads_predictions.constants import *
from datetime import datetime
from HeatLoads_predictions.exception import HeatLoadsException
from HeatLoads_predictions.utils.utils import read_yaml_file
#from HeatLoads_predictions.entity.config_entity import DataTransformConfig, DataValidationConfig, ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig, TrainingPipelineConfig,DataIngestionConfig,ModelEvaluationConfig
from HeatLoads_predictions.logger import logging
from HeatLoads_predictions.entity.config_entity import ModelPusherConfig, TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig

class Configuration:

    def __init__(self,config_file_path:str=CONFIG_FILE_PATH,time_stamp:datetime=CURRENT_TIME_STAMP):
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = time_stamp
        except Exception as e:
            raise HeatLoadsException(e,sys) from e

    def get_training_pipeline_config(self,)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HeatLoadsException(e,sys) from e
    
    
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
            data_ingestion_artifact_dir = os.path.join(artifact_dir,data_ingestion_info[DATA_INGESTION_ARTIFACT_NAME_KEY],self.time_stamp)
            tgz_download_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_info[DATA_INGESTION_TGZ_DATA_DIR_KEY])
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_info[DATA_INGESTION_INGESTED_DIR_KEY])
            train_data_dir = os.path.join(ingested_data_dir,data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])
            test_data_dir = os.path.join(ingested_data_dir,data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])
            logging.info(f"data ingestion config created succefully :{data_ingestion_info}")
            return DataIngestionConfig(dataset_download_url,tgz_download_dir,raw_data_dir,train_data_dir,test_data_dir)                                       

        except Exception as e:
            raise HeatLoadsException(e,sys) from e
    
    
    def get_data_validation_config(self)->DataValidationConfig:
        try:
            logging.info("searching and finding the data validation config ")
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR_NAME,
                self.time_stamp
            )
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]


            schema_file_path = os.path.join(ROOT_DIR,
            data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
            data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            report_file_path = os.path.join(data_validation_artifact_dir,
            data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path = os.path.join(data_validation_artifact_dir,
            data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]

            )

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
            )
            return data_validation_config
            
        except Exception as e:
            logging.info(e)
            raise HeatLoadsException(e,sys) from e   

    

    def get_data_transform_config(self)->DataTransformationConfig:
        try:
            logging.info("searching for the data transformation config-------------------")
            data_transform_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir

            data_transformation_artifact_dir = os.path.join(artifact_dir,DATA_TRANSFORMATION_ARTIFACT_DIR,self.time_stamp)

            transformed_dir = os.path.join(data_transformation_artifact_dir,data_transform_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR])

            transformed_train_dir = os.path.join(transformed_dir,data_transform_config_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR])

            transformed_test_dir = os.path.join(transformed_dir,data_transform_config_info[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR])
 
            preprocessed_obj_dir = os.path.join(data_transformation_artifact_dir,data_transform_config_info[DATA_TRANSFORMATION_PREPROCESSED_DIR])
      
            preprocssed_obj_file_path = os.path.join(preprocessed_obj_dir,data_transform_config_info[DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME])
          
            data_transform_config = DataTransformationConfig(transformed_train_dir=transformed_train_dir,
                                                        transformed_test_dir=transformed_test_dir,
                                                        preprocessed_object_file_path=preprocssed_obj_file_path)
            logging.info(f"the data transformation config is found {data_transform_config} and returned to pipeline ")
            return data_transform_config

        except Exception as e:
            logging.info(e)
            raise HeatLoadsException(e,sys) from e 

    
    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            model_trainer_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR,
                self.time_stamp
            )
            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY]
            )

            model_config_file_path = os.path.join(model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY]
            )

            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=model_config_file_path
            )
            logging.info(f"Model trainer config: {model_trainer_config}")
            return model_trainer_config
        except Exception as e:
            raise HeatLoadsException(e,sys) from e    

    
    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = os.path.join(self.training_pipeline_config.artifact_dir,
                                        MODEL_EVALUATION_ARTIFACT_DIR, )

            model_evaluation_file_path = os.path.join(artifact_dir,
                                                    model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])
            response = ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path,
                                            time_stamp=self.time_stamp)
            
            
            logging.info(f"Model Evaluation Config: {response}.")
            return response
        except Exception as e:
            raise HeatLoadsException(e,sys) from e 

    
  
    def get_model_pusher_config(self)->ModelPusherConfig:
        try:
            time_stamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            model_pusher_config_info = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path = os.path.join(ROOT_DIR, model_pusher_config_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY],
                                           time_stamp)
            
            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)

            logging.info(f"Model pusher config {model_pusher_config}")

            return model_pusher_config

        except Exception as e:
            raise HeatLoadsException(e,sys) from e 
