from datetime import datetime
import os

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    
ROOT_DIR = os.getcwd()

config_dir = 'config'
config_file_name ='config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,config_dir,config_file_name)
TARGET_COLUMN_KEY = 'target_column_pred'
BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

CURRENT_TIME_STAMP = get_current_time_stamp()
#TRAINING PIPELINE CONFIG CONSTANTS

TRAINING_PIPELINE_CONFIG_KEY ='training_pipeline_config'
TRAINING_PIPELINE_NAME_KEY ='pipeline_name'
TRAINING_ARTIFACT_DIR_KEY = 'artifact_dir'

#DATA INGESTION CONFIG CONSTANTS

DATA_INGESTION_CONFIG_KEY ='data_ingestion_config'
DATA_INGESTION_RAW_DATA_DIR_KEY ='raw_data_dir'
DATA_INGESTION_TGZ_DATA_DIR_KEY ='tgz_download_dir'
DATA_INGESTION_ARTIFACT_NAME_KEY ='data_ingestion'
DATA_INGESTION_INGESTED_DIR_KEY ='ingested_dir'
DATA_INGESTION_TRAIN_DIR_KEY ='ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY ='ingested_test_dir'
DATA_INGESTION_DOWNLOAD_URL_KEY ='dataset_download_url'

#DATA VALIDATION CONFIG DETAILS

DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = 'schema_file_name'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_dir'
DATA_VALIDATION_ARTIFACT_DIR_NAME = 'data_validation'
DATA_VALIDATION_REPORT_FILE_NAME_KEY= 'report_file_name'
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY= 'report_page_file_name'
DATA_VALIDATION_SCHEMA_KEY = 'columns'
DATA_TARGET_KEY ='target_column'
DATA_VALIDATION_CATEGORICAL_KEY ='categorical_columns'
DATA_VALIDATION_DOMAIN_KEY ='domain_value'

# DATA TRANFORMATION CONFIG DETAILS
NUMERICAL_COLUMN_KEY = 'numerical_columns'
DATA_TRANSFORMATION_CONFIG_KEY ='data_transformation_config'
DATA_TRANSFORMATION_TRANSFORMED_DIR ='transformed_dir'
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR ='transformed_train_dir'
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR ='transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSED_DIR ='preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME='preprocessed_object_file_name'
DATA_TRANSFORMATION_ARTIFACT_DIR = 'data_transformation'



#MODEL TRAINER CONFIG_ DETAILS
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"
#MODEL EVALUATION CONFIG DETAILS
MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR = "model_evaluation"

#MODEL PUSHER CONFIG DETAILS
MODEL_PUSHER_CONFIG_KEY = "model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = "model_export_dir"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"




