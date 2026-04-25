import os
from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging
import numpy as np
import yaml,sys
import pickle
from sklearn.metrics import f1_score as f1
from sklearn.model_selection import GridSearchCV
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise heart_disease_exception(e,sys)
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise heart_disease_exception(e,sys)
def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise heart_disease_exception(e,sys)
def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
            logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise heart_disease_exception(e,sys)
def load_object(file_path:str)->object:
    try:
        logging.info("Entered the load_object method of MainUtils class")
        with open(file_path,'rb') as file_obj:
            obj = pickle.load(file_obj)
            logging.info("Exited the load_object method of MainUtils class")
            return obj
    except Exception as e:
        raise heart_disease_exception(e,sys)
def load_numpy_array(file_path:str)->np.array:
    """
    load numpy error data from the file
    file path were the data is stored
    then return type should be np.array
    """
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise heart_disease_exception(e,sys)
def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}
        for i in range(len(models)):
            model=list(models.values())[i]
            
            param=params[list(models.keys())[i]]
            gs=GridSearchCV(model,param_grid=param,cv=3)
            gs.fit(x_train,y_train)
            y_test_pred=gs.predict(x_test)
            y_train_pred=gs.predict(x_train)
            test_model_score=f1(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise heart_disease_exception(e,sys)

