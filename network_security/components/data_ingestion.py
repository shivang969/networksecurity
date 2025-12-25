from network_security.exception.exception import NetworksecurityException
from network_security.entity.config_entity import DataIngestconfig
from network_security.logging.logger import logging
import os
import sys
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import pymongo
from sklearn.model_selection import train_test_split
from network_security.entity.artifact_entity import DataIngestionArtifact
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestconfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.tolist():
                df.drop(columns="_id",inplace=True)
            df.replace(["na", "NA", "N/A", "null", ""], np.nan, inplace=True)
            return df    
        except Exception as e:
           raise NetworksecurityException(e,sys)  
    
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
           raise NetworksecurityException(e,sys)  
    
    def train_test_split_(self,dataframe:pd.DataFrame):
        try:
           train_set,test_set=train_test_split(
               dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,
               random_state=42
           )
           logging.info("performed train test split on the dataframe")
           dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
           os.makedirs(dir_path,exist_ok=True)
           logging.info(f"exporitng train and test file path")
           train_set.to_csv(
               self.data_ingestion_config.training_file_path,index=False,header=True
           )
           test_set.to_csv(
               self.data_ingestion_config.testing_file_path,index=False,header=True
           )
            
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            df=self.export_collection_as_dataframe()
            df=self.export_data_into_feature_store(df)
            self.train_test_split_(df)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
            
            
        except Exception as e:
           raise NetworksecurityException(e,sys)    
        