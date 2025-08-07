from cnnclassifier.pipelines import data_injection_pipeline
from cnnclassifier.pipelines.data_injection_pipeline import DataIngestionTrainingPipeline
from cnnclassifier.pipelines.prepare_base_model_pipeline import 
from cnnclassifier import logger
STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e
STAGE_NAME = "Prepare base model"