import sys

from heart_disease.components.data_ingestion import Dataingestion
from heart_disease.components.data_transformation import Datatransformation
from heart_disease.components.data_validation import Datavalidation
from heart_disease.components.model_training import Model_training
from heart_disease.entity.artifact_entity import (
    Dataingestionartifact,
    Datatransformationartifact,
    Datavalidationartifact,
    model_training_artifact,
)
from heart_disease.entity.config_entity import (
    Dataingestionconfig,
    Datatransformationconfig,
    Datavalidationconfig,
    Modeltrainingconfig,
    trainingpipelineconfig,
)
from heart_disease.exception.exception import heart_disease_exception
from heart_disease.logging.logger import logging


class training_pipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = trainingpipelineconfig()
        except Exception as e:
            raise heart_disease_exception(e, sys)

    def start_data_ingestion(self) -> Dataingestionartifact:
        try:
            logging.info("Data ingestion started")
            data_ingestion_config = Dataingestionconfig(self.training_pipeline_config)
            data_ingestion = Dataingestion(data_Ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            raise heart_disease_exception(e, sys)

    def start_data_validation(
        self, data_ingestion_artifact: Dataingestionartifact
    ) -> Datavalidationartifact:
        try:
            logging.info("Data validation started")
            data_validation_config = Datavalidationconfig(self.training_pipeline_config)
            data_validation = Datavalidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config,
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise heart_disease_exception(e, sys)

    def start_data_transformation(
        self, data_validation_artifact: Datavalidationartifact
    ) -> Datatransformationartifact:
        try:
            logging.info("Data transformation started")
            data_transformation_config = Datatransformationconfig(
                self.training_pipeline_config
            )
            data_transformation = Datatransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transformation_config,
            )
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise heart_disease_exception(e, sys)

    def start_model_training(
        self, data_transformation_artifact: Datatransformationartifact
    ) -> model_training_artifact:
        try:
            logging.info("Model training started")
            model_training_config = Modeltrainingconfig(self.training_pipeline_config)
            model_trainer = Model_training(
                data_transformation_artifact=data_transformation_artifact,
                model_training_config=model_training_config,
            )
            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info("Model training completed")
            return model_trainer_artifact
        except Exception as e:
            raise heart_disease_exception(e, sys)

    def run_pipeline(self) -> model_training_artifact:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_training(
                data_transformation_artifact=data_transformation_artifact
            )
            return model_trainer_artifact
        except Exception as e:
            raise heart_disease_exception(e, sys)


if __name__ == "__main__":
    pipeline = training_pipeline()
    artifact = pipeline.run_pipeline()
    print(artifact)
