from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging
import os,sys
class heart_disease_model:
    def __init__(self,model,processor):
       
        try:
           self.model=model
           self.processor=processor
        except Exception as e:
           raise heart_disease_exception(e,sys)
    def predict_model(self,data):
        try:
            x_transform=self.processor.transform(data)
            y_predict=self.model.predict(x_transform)
            return y_predict
        except Exception as e:
            raise heart_disease_exception(e,sys)
