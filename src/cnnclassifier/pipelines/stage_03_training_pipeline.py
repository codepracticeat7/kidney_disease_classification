from cnnclassifier.components import training
from cnnclassifier import logger
STAGE_NAME="TRAINING STAGE"

def main():
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        training.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
if __name__ == '__main__':
    main()
    
