from flask import Flask, request
import sys

import pip
from HeatLoads_predictions.utils.utils import read_yaml_file, write_yaml_file
from matplotlib.style import context
from HeatLoads_predictions.logger import logging
from HeatLoads_predictions.exception import HeatLoadsException
import os, sys
import json
from HeatLoads_predictions.config.configuration import Configuration
from HeatLoads_predictions.constants import config_dir, get_current_time_stamp
from HeatLoads_predictions.pipeline.pipeline import Pipeline
from HeatLoads_predictions.entity.heatload_predictor import BuildingData , HeatLoadPredictor
from flask import send_file, abort, render_template


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "HeatLoadslogs"
PIPELINE_FOLDER_NAME = "HeatLoads_predictions"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, config_dir, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from HeatLoads_predictions.logger import get_log_dataframe

BUILDING_DATA_KEY = 'building_data'
HEATLOAD_VALUE_KEY = "heat_load_value"

app = Flask(__name__)


@app.route('/artifact', defaults={'req_path': 'HeatLoads_predictions'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("HeatLoads_predictions", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuration(time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        BUILDING_DATA_KEY: None,
        HEATLOAD_VALUE_KEY: None
    }

    if request.method == 'POST':
        Relative_Compactness = float(request.form['Relative_Compactness'])
        Surface_Area = float(request.form['Surface_Area'])
        Wall_area = float(request.form['Wall_area'])
        Roof_area = float(request.form['Roof_area'])
        Overall_height = float(request.form['Overall_height'])
        Orientation = float(request.form['Orientation'])
        Glazing_area = float(request.form['Glazing_area'])
        Glazing_area_distr = float(request.form['Glazing_area_distr'])
        building_data = BuildingData(Relative_Compactness= Relative_Compactness,
                                    Surface_Area= Surface_Area,
                                    Wall_area = Wall_area,
                                    Roof_area = Roof_area,
                                    Overall_height = Overall_height,
                                    Orientation = Orientation,
                                    Glazing_area = Glazing_area,
                                    Glazing_area_distr = Glazing_area_distr,
                                   )
        HeatLoads_predictions_df = building_data.get_building_input_data_frame()
        heatload_predictor = HeatLoadPredictor(model_dir=MODEL_DIR)
        heat_load_value = heatload_predictor.predict(X=HeatLoads_predictions_df)
        logging.info("the prediction is  ",heat_load_value)
        context = {
            BUILDING_DATA_KEY: building_data.get_building_data_as_dict(),
            HEATLOAD_VALUE_KEY: heat_load_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/HeatLoadslogs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()
