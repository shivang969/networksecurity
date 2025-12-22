import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)
import certifi
ca=certifi.where()
import numpy as np
import pandas as pd
import pymongo 
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging

class Networkdataextract():
    def __init__(self):
        try:
            self.mongo_client = None
        except Exception as e:
            raise NetworksecurityException(e,sys)
    def cv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworksecurityException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.records=records
            self.collection=collection
            self.mongo_url=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_url[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworksecurityException(e,sys)


if __name__=="__main__":
    file_path="network_data/net.csv"
    database="shivangpavan6"
    collection="Networkdata"
    network_obj=Networkdataextract()
    records=network_obj.cv_to_json(file_path=file_path)
    print(records)
    no_of_records=network_obj.insert_data_mongodb(records,database,collection)
    print(no_of_records)