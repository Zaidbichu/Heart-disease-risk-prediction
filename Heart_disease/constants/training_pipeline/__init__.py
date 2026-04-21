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