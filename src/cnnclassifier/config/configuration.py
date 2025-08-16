from cnnclassifier.constants import *
import os
from cnnclassifier.utils.common import read_yaml, create_directories
from cnnclassifier.entity.config_entity import *


class ConfigurationManager:
    def __init__(
                self,
                config_filepath = CONFIG_FILE_PATH,
                params_filepath= PARAMS_FILE_PATH):
        
        self.config=read_yaml(config_filepath)
        self.params=read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])
    def get_data_ingestion_config(self)->DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config=DataIngestionConfig(root_dir=config.root_dir,
                                                  source_URL=config.source_URL,
                                                  local_data_file=config.local_data_file,
                                                  unzip_dir=config.unzip_dir)
        return data_ingestion_config
    def get_prepare_basemodel_config(self)->Preparebasemodelconfig:
        config=self.config.prepare_basemodel
        create_directories([config.root_dir])

        Preparebasemodelconfigs=Preparebasemodelconfig(root_dir=config.root_dir,
                                base_model_dir=config.base_model_dir,
                                updated_base_model_path=config.updated_base_model_path,
                                params_image_size=self.params.IMAGE_SIZE,
                                params_learning_rate=self.params.LEARNING_RATE,
                                params_include_top=self.params.INCLUDE_TOP,
                                params_weights=self.params.WEIGHTS,
                                params_classes=self.params.CLASSES,
                                )
        return Preparebasemodelconfigs
    def get_prepare_Trainingconfig(self)->trainingconfig:
        config=self.config.training
        params=self.params
        print(config)
        training_data=os.path.join(self.config.data_ingestion.unzip_dir,"data","kidney-ct-scan-image")
        Trainingconfig=trainingconfig(root_dir=config.root_dir,trained_model_name=str,
                                      updated_base_model_path=config.updated_base_model_path,
                                      training_data=Path(training_data),
                                    params_loss=self.params.params_loss,
                                    params_epochs=params.EPOCHS,
                                    params_batch_size=params.BATCH_SIZE,
                                    params_is_augmentation=params.AUGMENTATION,
                                    params_image_size=params.IMAGE_SIZE)
        return Trainingconfig
    def get_evaluation_config(self) -> EvaluationConfig:
        symlink_path = "artifacts/model/latest_model"
       

        print("Symlink target:", os.readlink("artifacts/model/latest_model"))
        # Resolve the actual path the symlink points to
        real_path = os.readlink(symlink_path)



        print("Symlink points to:",real_path)
        model_path= real_path

        eval_config = EvaluationConfig(
            path_of_model=model_path,
            training_data="artifacts/data_ingestion/data/kidney-ct-scan-image",
            mlflow_uri="https://dagshub.com/albertmichael/kidney_disease_classification.mlflow",
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config
        
    

    
    

