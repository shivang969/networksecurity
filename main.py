from network_security.components.data_ingestion import DataIngestion
import os
import sys
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestconfig
from network_security.entity.config_entity import TrainigPipelineConfig
from network_security.entity.config_entity import DataValidationConfig,DataTransformConfig
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainigPipelineConfig()
        dataingestionconfig=DataIngestconfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("intiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation)
        data_transformation_config=DataTransformConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
    except Exception as e:
        raise NetworksecurityException(e,sys)