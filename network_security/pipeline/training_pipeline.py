import os
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.logging.logger import logging
from network_security.exception.exception import NetworksecurityException
from network_security.entity.config_entity import(
    TrainigPipelineConfig,
    DataIngestconfig,
    ModelTrainerConfig,
    DataTransformConfig,
    DataValidationConfig
)
from network_security.entity.artifact_entity import(
    ModelTrainerArtifact,
    DataTransforArtifact,
    DataIngestionArtifact,
    DataValidArtifact
)

import sys


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainigPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestconfig(training_pipeline_config=self.training_pipeline_config)
            self.data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifact=self.data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed and artifact {self.data_ingestion_artifact}")
            return self.data_ingestion_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_validation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            logging.info("intiate the data validation")
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact 
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidArtifact):
        try:
            data_transformation_config=DataTransformConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_srtifact:DataTransforArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config:ModelTrainerConfig=ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            model_trainer=ModelTrainer(
                data_transfromation_artifact=data_transformation_srtifact,
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_srtifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
            
                               