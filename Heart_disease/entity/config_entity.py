import os
import datetime
from heart_disease.constants import training_pipeline

print(training_pipeline.pipeline_name,training_pipeline.artifact_dir)
class trainingpipelineconfig:
    def __init__(self):
        timestamp=datetime.datetime.now().strftime('%m_%d_%y_%H_%M_%S')
        self.pipeline_name=training_pipeline.pipeline_name
        self.artifact_name=training_pipeline.artifact_dir
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp:str=timestamp
class Dataingestionconfig:
    def __init__(self,training_pipeline_config:trainingpipelineconfig):
        self.data_ingestion_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.Data_ingestion_dir)
        self.raw_data_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.Data_ingestion_raw_data_dir,training_pipeline.file_name)
        self.train_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.Data_ingestion_ingested_dir,training_pipeline.train_file_name)
        self.test_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.Data_ingestion_ingested_dir,training_pipeline.test_file_name)
        self.train_test_split_ratio:float=training_pipeline.Data_ingestion_train_test_split_ratio
class Datavalidationconfig:
    def __init__(self,training_pipeline_config:trainingpipelineconfig):
        
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.Data_validation_dir)
        self.valid_dir:str=os.path.join(self.data_validation_dir,training_pipeline.Data_validation_validated_dir)
        self.invalid_dir:str=os.path.join(self.data_validation_dir,training_pipeline.Data_validation_invalid_dir)
        self.valid_train_file_path:str=os.path.join(self.valid_dir,training_pipeline.train_file_name)
        self.valid_test_file_path:str=os.path.join(self.valid_dir,training_pipeline.test_file_name)
        self.invalid_train_file_path:str=os.path.join(self.invalid_dir,training_pipeline.train_file_name)
        self.invalid_test_file_path:str=os.path.join(self.invalid_dir,training_pipeline.test_file_name)
        self.drift_report_file_path:str=os.path.join(
            self.data_validation_dir,training_pipeline.Data_validation_drift_report_dir,training_pipeline.Data_validation_drift_report_file_name
        )


