from network_security.components.data_ingestion import DataIngestion
import os
import sys
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestconfig
from network_security.entity.config_entity import TrainigPipelineConfig

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainigPipelineConfig()
        dataingestionconfig=DataIngestconfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("intiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        
    except Exception as e:
        raise NetworksecurityException(e,sys)