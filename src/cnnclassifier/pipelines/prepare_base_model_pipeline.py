from pathlib import Path
from cnnclassifier.config.configuration import ConfigurationManager
ConfigurationManager=ConfigurationManager()
from cnnclassifier.components.prepare_base_model import PreparebaseModel
def load_full_model_pipeline():

    config=ConfigurationManager.get_prepare_basemodel_config()
    cls=PreparebaseModel(config=config)
    cls.get_base_model()
    cls.update_base_model()
if __name__=="__main__":
    
    load_full_model_pipeline()
