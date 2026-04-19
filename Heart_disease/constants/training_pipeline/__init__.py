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
##data ingesiton constants starts with data ingestion
Data_ingestion_dir:str="data_ingestion"
Data_ingestion_train_test_split_ratio:float=0.2
Data_ingestion_raw_data_dir:str="raw_data"
Data_ingestion_ingested_dir:str="ingested_dir"