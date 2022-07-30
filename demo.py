import sys
from HeatLoads_predictions.logger import logging
from HeatLoads_predictions.pipeline.pipeline import Pipeline
from HeatLoads_predictions.exception import HeatLoadsException
from HeatLoads_predictions.config.configuration import Configuration
from HeatLoads_predictions.constants import *

def main():
    try:
        pipeline = Pipeline(Configuration())
        pipeline.start()
        #logging.info("main function execution completed.")
    except Exception as e:
        raise HeatLoadsException(e,sys) from e

if __name__=="__main__":
    main()