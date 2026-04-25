import numpy as np
import pandas as pd
from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging
from heart_disease.entity.artifact_entity import Datatransformationartifact, model_training_artifact as ModelTrainingArtifact
from heart_disease.entity.config_entity import Modeltrainingconfig
from heart_disease.utils.main_utils.utils import load_numpy_array,evaluate_model,save_object,load_object
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
    
)
import os,sys
from heart_disease.utils.ml_utils.metric_utils.classification_metric import get_classification_score
from heart_disease.utils.ml_utils.model.estimator import heart_disease_model

from sklearn.neighbors import KNeighborsClassifier
class Model_training:
    def __init__(self,data_transformation_artifact:Datatransformationartifact,model_training_config:Modeltrainingconfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_training_config=model_training_config
    def model_train(self,x_train,y_train,x_test,y_test):
        logging.info("we have enterd the model traininf part")
        models={
            "Random_forest_classifier":RandomForestClassifier(),
            "decision_tree_classifier":DecisionTreeClassifier(),
            "k_neighbour_classifier":KNeighborsClassifier(),
            "Ada_boost_classifier":AdaBoostClassifier(),
            "gradient_boost_classifier":GradientBoostingClassifier()


        }
        params = {
                "Random_forest_classifier": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [None, 5, 10, 20],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                },
                "decision_tree_classifier": {
                    "criterion": ["gini", "entropy", "log_loss"],
                    "max_depth": [None, 5, 10, 20],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                },
                "k_neighbour_classifier": {
                    "n_neighbors": [3, 5, 7, 9],
                    "weights": ["uniform", "distance"],
                    "metric": ["minkowski", "euclidean", "manhattan"]
                },
                "Ada_boost_classifier": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0]
                },
                "gradient_boost_classifier": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.2],
                    "max_depth": [3, 5, 10],
                    "subsample": [0.8, 1.0]
                }
            }


        model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)
        best_score=max(model_report.values())
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_score)
        ]
        best_model=models[best_model_name]
        ''' for model_name, score in model_report.items():
                 print(f"{model_name}: {score}")'''
        best_model.fit(x_train, y_train)
        y_train_pred=best_model.predict(x_train)
        classification_trained_metric=get_classification_score(y_train,y_train_pred)
        Y_test_pred=best_model.predict(x_test)
        classfication_test_metric=get_classification_score(y_test,Y_test_pred)
        processor=load_object(self.data_transformation_artifact.preprocessor_obj_file_path)
        heart_disease_model_instance=heart_disease_model(best_model,processor)
        save_object(self.model_training_config.save_model_file_path,obj=heart_disease_model_instance)
    
    
        heart_disease_model_instance=heart_disease_model(best_model,processor)
        save_object(self.model_training_config.save_model_file_path,obj=heart_disease_model_instance)
        model_artifact = ModelTrainingArtifact(
            trained_model_file_path=self.model_training_config.save_model_file_path,
            train_metric_artifact=classification_trained_metric,
            test_metric_artifact=classfication_test_metric

        )
        logging.info(f"model artifact completed {model_artifact}")
        return model_artifact

    def initiate_model_training(self)->ModelTrainingArtifact:
        try:
            logging.info("we have entered the initate model training part")
            logging.info("we are loadding the data")
            train_data=load_numpy_array(self.data_transformation_artifact.transformed_train_file_path)
            test_data=load_numpy_array(self.data_transformation_artifact.transformed_test_file_path)
            logging.info("we have loaded the train and test file")
            logging.info("now we need to create the train test split")
            x_train,y_train,x_test,y_test=(
                train_data[:,:-1],
                train_data[:,-1],
                test_data[:,:-1],
                test_data[:,-1]
            )
            model_trainer_artifact=self.model_train(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise heart_disease_exception(e,sys)
