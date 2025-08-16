from cnnclassifier.config.configuration import ConfigurationManager
from cnnclassifier.components.data_ingestion import data
from cnnclassifier import logger

STAGE_NAME = "Data Ingestion stage"
class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = data(config=data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.unzip_data()
        except Exception as e:
            raise e
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        ob = DataIngestionTrainingPipeline()
        ob.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e