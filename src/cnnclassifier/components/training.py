from datetime import datetime
import os
import subprocess
from cnnclassifier.utils.common import read_yaml, create_directories,get_cpu_temp,monitor_training
from cnnclassifier.config.configuration import ConfigurationManager
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import threading


from cnnclassifier.components.cpu_monitor import CPUUsageMonitor,  CPUMonitorCallback,gmail_service# assuming your monitor class is in cpu_monitor.py





from cnnclassifier import logger

def main():
    o=ConfigurationManager()
    m=o.get_prepare_Trainingconfig()
    load_model=tf.keras.models.load_model(m.updated_base_model_path)
    early_stop = EarlyStopping(
        monitor='val_loss',       # You can also use 'val_accuracy'
        patience=2,               # Number of epochs to wait before stopping
        restore_best_weights=True
    )

    datagenerator_kwargs = dict(
                rescale = 1./255,
                validation_split=0.20
            )
    dataflow_kwargs = dict(
                target_size=m.params_image_size[:-1],
                batch_size=m.params_batch_size,
                interpolation="bilinear"
                )
    VALID_DATAGENERATOR= tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)
    valid_generator= VALID_DATAGENERATOR.flow_from_directory(directory=m.training_data,subset="validation",
                                                            shuffle=False,
                                                            **dataflow_kwargs)

    if m.params_is_augmentation:
        train_datagenerator=tf.keras.preprocessing.image.ImageDataGenerator(rotation_range=40,
                                                                            horizontal_flip=True,
                                                                            width_shift_range=0.2,
                                                                            height_shift_range=0.2,
                                                                            shear_range=0.2,
                                                                            zoom_range=0.2,
                                                                            **datagenerator_kwargs)
    else:
        train_datagenerator=VALID_DATAGENERATOR

    train_generator=train_datagenerator.flow_from_directory(directory=m.training_data,
                                                            subset="training",
                                                            shuffle=True,
                                                            **dataflow_kwargs)

    time_stamp=datetime.now()
    time=time_stamp.strftime("%Y%m%d_%H%M%S")
    trained_model_root=os.path.join(f"{m.root_dir}/training{time}")
    create_directories([trained_model_root])
    trained_model_path=os.path.join(trained_model_root,"vgg16model.h5")

    steps_per_epoch = train_generator.samples // train_generator.batch_size
    validation_steps =valid_generator.samples // valid_generator.batch_size
    service = gmail_service()

    # 2. Start CPU Monitor in background
    monitor = CPUUsageMonitor(
        gmail_service=service,
        sender=os.getenv("sender"),     # replace with your Gmail
        receiver=os.getenv("receiver"),     # replace with recipient
        threshold=85,
        check_interval=5
    )
    monitor.start()
    
    

    # Now start training
    try:
        

        load_model.fit(train_generator,
                    epochs=m.params_epochs,
                    steps_per_epoch=steps_per_epoch,
                    validation_steps=validation_steps,
                    validation_data=valid_generator,
                    callbacks=[
                CPUMonitorCallback(monitor),
                EarlyStopping(
                    monitor="val_loss",       # metric to watch
                    patience=3,               # stop after 3 bad epochs
                    restore_best_weights=True # rollback to best weights
                )
            ]
        )
    except KeyboardInterrupt:
        print("🛑 Training interrupted manually.")

    load_model.save(trained_model_path)
    

   

    latest_model = trained_model_path
    print(f"trained model path{trained_model_path}")
    symlink_path = "artifacts/model/latest_model"
    trained_model_path = trained_model_path.replace("\\", "/")
    symlink_path = symlink_path.replace("\\", "/")

    
    # Remove old symlink if it exists
    if os.path.islink(symlink_path):
        os.unlink(symlink_path)
        print(f"Removed existing symlink at {symlink_path}")
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)

    else:
        logger.info(f"No previous symlink found at {symlink_path}")


    # Create new symlink (Windows only)
    cmd = f'mklink "{symlink_path}" "{trained_model_path}"'
    import shutil

    try:
        subprocess.run(["cmd", "/c", cmd], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.info(f"Command for creating symlink failed with exit code {e.returncode}")
        # Create the symlink
    if os.path.exists(trained_model_path):
        os.symlink(trained_model_path, symlink_path)
        print(f"Symlink created: {symlink_path} → {trained_model_path}")
    else:
        print(f"Target model not found: {trained_model_path}")

        if not os.path.exists(symlink_path):
            shutil.copy(trained_model_path, symlink_path)
        else:
            print(f"{symlink_path} already exists. Skipping copy.")


if __name__=="__main__":
    main()
# import os
# import urllib.request as request
# from zipfile import ZipFile
# import tensorflow as tf
# import time
# from pathlib import Path
# from cnnClassifier.entity.config_entity import TrainingConfig


# class Training:
#     def __init__(self, config: TrainingConfig):
#         self.config = config

    
#     def get_base_model(self):
#         self.model = tf.keras.models.load_model(
#             self.config.updated_base_model_path
#         )

#     def train_valid_generator(self):

#         datagenerator_kwargs = dict(
#             rescale = 1./255,
#             validation_split=0.20
#         )

#         dataflow_kwargs = dict(
#             target_size=self.config.params_image_size[:-1],
#             batch_size=self.config.params_batch_size,
#             interpolation="bilinear"
#         )

#         valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
#             **datagenerator_kwargs
#         )

#         self.valid_generator = valid_datagenerator.flow_from_directory(
#             directory=self.config.training_data,
#             subset="validation",
#             shuffle=False,
#             **dataflow_kwargs
#         )

#         if self.config.params_is_augmentation:
#             train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
#                 rotation_range=40,
#                 horizontal_flip=True,
#                 width_shift_range=0.2,
#                 height_shift_range=0.2,
#                 shear_range=0.2,
#                 zoom_range=0.2,
#                 **datagenerator_kwargs
#             )
#         else:
#             train_datagenerator = valid_datagenerator

#         self.train_generator = train_datagenerator.flow_from_directory(
#             directory=self.config.training_data,
#             subset="training",
#             shuffle=True,
#             **dataflow_kwargs
#         )

    
#     @staticmethod
#     def save_model(path: Path, model: tf.keras.Model):
#         model.save(path)



    
#     def train(self):
#         self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
#         self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

#         self.model.fit(
#             self.train_generator,
#             epochs=self.config.params_epochs,
#             steps_per_epoch=self.steps_per_epoch,
#             validation_steps=self.validation_steps,
#             validation_data=self.valid_generator
#         )

#         self.save_model(
#             path=self.config.trained_model_path,
#             model=self.model
#         )
