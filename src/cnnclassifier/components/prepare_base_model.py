     
import tensorflow as tf
from cnnclassifier.entity.config_entity import Preparebasemodelconfig
from cnnclassifier import logger
from pathlib import Path
import os
from cnnclassifier.utils.common import read_yaml, create_directories


class PreparebaseModel:
    def __init__(self,config:Preparebasemodelconfig):
        self.config=config
        



    def get_base_model(self):
        root_dir=self.config.root_dir

        self.base_model=tf.keras.applications.vgg16.VGG16(include_top=self.config.params_include_top,input_shape=self.config.params_image_size,weights=self.config.params_weights)
        self.save_model(path=self.config.base_model_dir,model=self.base_model)
    @staticmethod
    def prepare_full_model(model,classes,freeze_all,freeze_till,learning_rate):
        if freeze_all:
            for layer in model.layers:
                model.trainable=False
        elif (freeze_till is not None) and (freeze_till>0):
            for layer in model.layers[:-freeze_till]:
                model.trainable=False
        flatten_in=tf.keras.layers.Flatten()(model.output)
        prediction_layer=tf.keras.layers.Dense(units=classes,
                                               activation="softmax")(flatten_in)
        full_model=tf.keras.models.Model(inputs=model.input,
                                         outputs=prediction_layer)
        loss_map = {
                            "categorical_crossentropy": tf.keras.losses.CategoricalCrossentropy(),
                            "binary_crossentropy": tf.keras.losses.BinaryCrossentropy()
                        }
     
        full_model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
                           loss=loss_map["binary_crossentropy"],
                           metrics=["accuracy"])
        full_model.summary()
        return full_model
    def update_base_model(self):
        self.full_model=self.prepare_full_model(model=self.base_model,
                                                classes=self.config.params_classes,
                                                freeze_all=True,
                                                freeze_till=None,
                                                learning_rate=self.config.params_learning_rate
                                                )
        #create_directories([self.config.self.config.updated_base_model_path])
        logger.info("_____ prepared full model ______")
        
        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)
        logger.info("_____  full model saved ______")

    @staticmethod
    def save_model(path: Path, model:tf.keras.Model):
        model.save(path)






