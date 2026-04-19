import pandas as pd
import numpy as np
import os,sys
from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging
from heart_disease.entity.config_entity import Dataingestionconfig, trainingpipelineconfig
from heart_disease.entity.artifact_entity import Dataingestionartifact
from sklearn.model_selection import train_test_split
class Dataingestion:
    def __init__(self,data_Ingestion_config:Dataingestionconfig):
        self.data_ingestion_config=data_Ingestion_config
    def load_data(self):
        try:
            logging.info("we have entered the load data method of data ingestion class")
            logging.info("we are loading the data from database")
            df=pd.read_csv('heart_disease_data/heart_disease.csv')
            logging.info("we have loaded the data as dataframe")
            return df
        except Exception as e:
            raise heart_disease_exception(e,sys)
    def export_data_to_feature_store(self,df:pd.DataFrame):
        try:
            feature_store=self.data_ingestion_config.raw_data_file_path
            dir_path=os.path.dirname(feature_store)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store,index=False,header=True)
            logging.info("exported the data to the feature store")
            return df
            
        except Exception as e:
            raise heart_disease_exception(e,sys)
    def split_data_as_train_test(self,df:pd.DataFrame):
        try:
            logging.info("we are spliiting the data into train and test")
            train,test=train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info("we have splited the data into train and test")
            dir_path=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("we have exported the train and test data")
        except Exception as e:
            raise heart_disease_exception(e,sys)

    def initiate_data_ingestion(self)->Dataingestionartifact:
        try:
            logging.info("entered the data ingestion method or component")
            dataset=self.load_data()
            logging.info('we have loaded the data set as dataframe')
            dataset=self.export_data_to_feature_store(dataset)
            logging.info("we have exported the data to feature store")
            logging.info("now the data is ready to be splitted into train and test")
            self.split_data_as_train_test(dataset)
            dataingestion_artifact=Dataingestionartifact(raw_data_path=self.data_ingestion_config.raw_data_file_path,train_file_path=self.data_ingestion_config.train_file_path,test_file_path=self.data_ingestion_config.test_file_path)
            return dataingestion_artifact
        except Exception as e:
            raise heart_disease_exception(e,sys)
if __name__ == "__main__":
    training_pipeline_config = trainingpipelineconfig()
    data_ingestion_config = Dataingestionconfig(training_pipeline_config)
    data_ingestion = Dataingestion(data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)
