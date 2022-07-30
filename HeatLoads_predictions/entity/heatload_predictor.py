import os
import sys

from HeatLoads_predictions.exception import HeatLoadsException
from HeatLoads_predictions.utils.utils import load_object
from HeatLoads_predictions.logger import logging
import pandas as pd


class BuildingData:

    def __init__(self,
                Relative_Compactness:float,
                Surface_Area:float,
                Wall_area:float,
                Roof_area:float,
                Overall_height:float,
                Orientation:float,
                Glazing_area:float,
                Glazing_area_distr:float,
                heating_load_value = None
                ):
        try:
            self.Realtive_Compactness = Relative_Compactness
            self.Surface_Area = Surface_Area
            self.Wall_area = Wall_area
            self.Roof_area= Roof_area
            self.Overall_height= Overall_height
            self.Orientation = Orientation
            self.Glazing_area = Glazing_area
            self.Glazing_area_distr = Glazing_area_distr

            self.heat_load_value = heating_load_value
        except Exception as e:
            raise HeatLoadsException(e, sys) from e

    def get_building_input_data_frame(self):

        try:
            housing_input_dict = self.get_building_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise HeatLoadsException(e, sys) from e

    def get_building_data_as_dict(self):
        try:
            input_data ={
                "X1": [self.Realtive_Compactness],
                "X3": [self.Wall_area],
                "X4": [self.Roof_area],
                "X5": [self.Overall_height],
                "X6": [self.Orientation],
                "X7": [self.Glazing_area],
                "X8": [self.Glazing_area_distr],
            }
            return input_data
        except Exception as e:
            raise HeatLoadsException(e, sys)


class HeatLoadPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise HeatLoadsException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise HeatLoadsException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            logging.info(f" the model path is taken from ", model_path)
            model = load_object(file_path=model_path)
            heat_load_value = model.predict(X)
            logging.info("the prediction is  ",heat_load_value)
            return heat_load_value
        except Exception as e:
            raise HeatLoadsException(e, sys) from e