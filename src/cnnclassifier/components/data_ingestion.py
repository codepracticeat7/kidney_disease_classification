import os
import zipfile
import gdown
from cnnclassifier import logger
from cnnclassifier.utils.common import get_size
from pathlib import Path
from cnnclassifier.entity.config_entity import (DataIngestionConfig)
class data:
    def __init__(self,config:DataIngestionConfig):
        self.config=config
        
    def download_data(self):
        try:
            '''
            Fetch data from the url
            '''
            
            dataset_url=self.config.source_URL
            os.makedirs(self.config.root_dir,exist_ok=True)
            zip_download_dir=self.config.local_data_file
            logger.info(f"creating directeries for data as {zip_download_dir} ")
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")
            file_id =dataset_url.split("/")[-2]
            prefix_url= 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix_url+file_id,zip_download_dir)
            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            raise e
    def unzip_data(self):

        Path(self.config.unzip_dir).mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(self.config.unzip_dir)
            logger.info(f"Downloaded data extracted into the folder {self.config.unzip_dir}")

       



