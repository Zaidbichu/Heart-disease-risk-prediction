from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging
from heart_disease.entity.artifact_entity import Datavalidationartifact,Datatransformationartifact
from heart_disease.entity.config_entity import Datatransformationconfig
from heart_disease.constants.training_pipeline import Target_column,drop_colums,numerical_columns,categorical_columns
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import sys,os
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from heart_disease.utils.main_utils.utils import save_numpy_array,save_object
class Datatransformation:
    def __init__(self,data_validation_artifact:Datavalidationartifact,data_transformation_config:Datatransformationconfig):
        self.data_validation_artifact=data_validation_artifact
        self.data_transformation_config=data_transformation_config
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise heart_disease_exception(e,sys)
    def get_transformed_obj(self)->Pipeline:
        try:
            num_pipeline=Pipeline(
                steps=[
                    ('scalar',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("one_hot_encoding",OneHotEncoder(handle_unknown="ignore"))
                ]
            )
            
            processor:Pipeline=ColumnTransformer(
                transformers=[
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("categoriacal_column",cat_pipeline,categorical_columns)
                ],
                remainder="passthrough"
            )
            return processor
        except Exception as e:
            raise heart_disease_exception(e,sys)


    def initiate_data_transformation(self)->Datatransformationartifact:
        logging.info("enterd the initiate data transformation part")
        try:
            train_data=self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_data=self.read_data(self.data_validation_artifact.valid_test_file_path)
            input_feature_train_data=train_data.drop(columns=drop_colums)
            target_feature_trained_data=train_data[Target_column]

            input_feature_test_data=test_data.drop(columns=drop_colums)
            target_test_data=test_data[Target_column]
            processor=self.get_transformed_obj()
            processor_obj=processor.fit(input_feature_train_data)
            transformed_train_data=processor_obj.transform(input_feature_train_data)
            transformed_test_data=processor_obj.transform(input_feature_test_data)
            train_arr=np.column_stack((transformed_train_data,np.array(target_feature_trained_data)))
            test_arr=np.column_stack((transformed_test_data,np.array(target_test_data)))
            save_numpy_array(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.processor_obj_file_path,processor_obj)
            datatranformationartifact=Datatransformationartifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessor_obj_file_path=self.data_transformation_config.processor_obj_file_path
            )
            return datatranformationartifact
        except Exception as e:
            raise heart_disease_exception(e,sys)

from heart_disease.entity.config_entity import (
    trainingpipelineconfig,
    Dataingestionconfig,
    Datavalidationconfig,
    Datatransformationconfig
)
from heart_disease.components.data_ingestion import Dataingestion
from heart_disease.components.data_validation import Datavalidation
'''
if __name__ == "__main__":
    try:
        training_pipeline_config = trainingpipelineconfig()

        data_ingestion_config = Dataingestionconfig(training_pipeline_config)
        data_ingestion = Dataingestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation_config = Datavalidationconfig(training_pipeline_config)
        data_validation = Datavalidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config
        )
        data_validation_artifact = data_validation.initiate_data_validation()

        data_transformation_config = Datatransformationconfig(training_pipeline_config)
        data_transformation = Datatransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        print(data_transformation_artifact)

    except Exception as e:
        raise heart_disease_exception(e, sys)
'''