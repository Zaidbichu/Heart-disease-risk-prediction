import numpy as np
import pandas as pd
import os,sys

##defining the constant variables for training pipeline

Target_column:str="target_binary"
pipeline_name:str="heart_disease"
artifact_dir:str="artifact"
train_file_name:str="train.csv"
test_file_name:str="test.csv"
file_name:str="heart_disease.csv"
drop_colums=["num","target_binary"]

numerical_columns= ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

categorical_columns= ['cp', 'restecg', 'slope', 'ca', 'thal']
binary_columns:str = ['sex', 'fbs', 'exang']
schema_file_path=os.path.join('data_schema','schema.yaml')
##data ingesiton constants starts with data ingestion
Data_ingestion_dir:str="data_ingestion"
Data_ingestion_train_test_split_ratio:float=0.2
Data_ingestion_raw_data_dir:str="raw_data"
Data_ingestion_ingested_dir:str="ingested_dir"

##data validation constants starts with data validation
Data_validation_dir:str="data_validation"
Data_validation_validated_dir:str="validated_dir"
Data_validation_invalid_dir:str="invalid_dir"
Data_validation_drift_report_dir:str="Drift_report"
Data_validation_drift_report_file_name:str="report.yaml"

##data transformation coinstants
Data_transforamtion_dir:str="data_transformation"
Data_transformation_tranformed_dir_name:str="transformed"
Data_transformation_processor_object_file_name:str="transformed_object"
processor_obj_file_path:str="processor.pkl"
Data_tranformation_trained_file_path:str="trained.npy"
Data_transformation_test_file_path:str="test.npy"

## model training constants
Model_training_dir:str="model_training"
Model_trained_file_name:str="model.pkl"
Model_training_train_metric_dir:str="train_metric"
Model_training_test_metric_dir:str="test_metric"
Model_trained_expected_score:float=0.6
Model_trained_overfitting_underfitting_threshold:float=0.05