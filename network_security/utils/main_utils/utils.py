import yaml
import dill
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging
import os
import pymongo
import numpy as np
import sys

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworksecurityException(e,sys)

def write_yaml_file(file_path:str,content:object,replace:bool=False)->bool:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworksecurityException(e,sys)
            
                    
                
    