import os
import numpy as np
import pandas as pd
"""
    data ingestion related constant start with data_ingestion var name
"""

TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="net.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

DATA_INGESTION_COLLECTION_NAME:str="Networkdata"
DATA_INGESTION_DATABASE_NAME:str="shivangpavan6"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float=0.2