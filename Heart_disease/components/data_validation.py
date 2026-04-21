

import pandas as pd
import numpy as np
import os,sys
from scipy.stats import ks_2samp
from heart_disease.utils.main_utils.utils import read_yaml_file,write_yaml_file
from heart_disease.constants.training_pipeline import schema_file_path
from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging
from heart_disease.components.data_ingestion import Dataingestion
from heart_disease.entity.config_entity import Datavalidationconfig,trainingpipelineconfig,Dataingestionconfig
from heart_disease.entity.artifact_entity import Dataingestionartifact,Datavalidationartifact
class Datavalidation:
    def __init__(self,data_ingestion_artifact:Dataingestionartifact,data_validation_config:Datavalidationconfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_file_path=read_yaml_file(schema_file_path)
        except Exception as e:
            raise heart_disease_exception(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        return pd.read_csv(file_path)
    def valid_no_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            no_of_columns=len(self._schema_file_path['columns'])
            if no_of_columns==len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise heart_disease_exception(e,sys)
    def missing_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            missing_columns=[]
            for col in self._schema_file_path['columns'].keys():
                if col not in dataframe.columns:
                    missing_columns.append(col)
            if len(missing_columns)==0:
                return True
            return False
        except Exception as e:
            raise heart_disease_exception(e,sys)
    def detect_dataset_drift(self,base_df,current_df,threshold=0.5):
        try:
            logging.info("we have enterd into the dataset drift part")
            status=True
            report={}
            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]
                result=ks_2samp(d1,d2)
                if result.pvalue < threshold:
                    is_found = True
                    status = False
                else:
                    is_found = False

                report[col]={
                    "p_value":float(result.pvalue),
                    "drift_status":is_found
                    
                    }
                drift_report_file_path=self.data_validation_config.drift_report_file_path
                dir=os.path.dirname(drift_report_file_path)
                os.makedirs(dir,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise heart_disease_exception(e,sys)
        


        
    def initiate_data_validation(self)->Datavalidationartifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_dataframe=self.read_data(train_file_path)
            logging.info("we have read the train data ")
            test_dataframe=self.read_data(test_file_path)
            logging.info("we have read the test data")
            status=self.valid_no_of_columns(train_dataframe)
            if not status:
                error_message="the no of columns in train data set is not equal"
            else:
                numerical_columns=[columns for columns in train_dataframe.columns if train_dataframe[columns].dtype!='O']
                print(f"the total no of numerical columns are {len(numerical_columns)}")
            status=self.valid_no_of_columns(test_dataframe)
            if not status:
                error_message="the no of columns in test data is not equal"
            else:
                numerical_columns=[col for col in test_dataframe.columns if test_dataframe[col].dtype!='O']
                print(f"the no of numerical columns are {len(numerical_columns)}")
            missing_columns_status=self.missing_columns(train_dataframe)
            if not missing_columns_status:
                error_message="the no of columns in the dataframe and the train is not equal"
                raise Exception(error_message)
            else:
                print("there are no missing columns")
            missing_columns_status=self.missing_columns(test_dataframe)
            if not missing_columns_status:
                error_message="the no of columns in the dataframe and the test is not equal"
                raise Exception(error_message)
            else:
                print("there are no missing columns")
            
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            datavalidationartifact=Datavalidationartifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path

            )
            return datavalidationartifact
        except Exception as e:
            raise heart_disease_exception(e,sys)
"""
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
        print(data_validation_artifact)

    except Exception as e:
        raise heart_disease_exception(e, sys) """