from pathlib import Path
from cnnclassifier.config.configuration import ConfigurationManager
ConfigurationManager=ConfigurationManager()
from cnnclassifier.components.prepare_base_model import PreparebaseModel
from cnnclassifier import logger
STAGE_NAME="PREPARE MODEL STAGE"
class load_full_model_pipeline:
    try:
        def load_full_model_pipeline():

            config=ConfigurationManager.get_prepare_basemodel_config()

            cls=PreparebaseModel(config=config)
            logger.info("_____lodaing base model______")
            cls.get_base_model()
            logger.info("_____ base model loaded______")
            logger.info("_____ updating base model to full model ______")
            cls.update_base_model()
            logger.info("_____ prepared full model ready to train ______")
    except Exception as e:
        raise e
if __name__== "__main__":
    try:

        full_model=load_full_model_pipeline
        full_model.load_full_model_pipeline()
    except Exception as e:
        logger.exception(e)
        raise e    
