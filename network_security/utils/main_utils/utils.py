import yaml
import dill
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging
import os
import pymongo
import numpy as np
import sys
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import RandomizedSearchCV

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

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworksecurityException(e,sys)
    
def save_object(file_path: str,obj:object)->None:
    try:
        logging.info("entered the save_object function")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
          pickle.dump(obj,file_obj)
        logging.info("exited the save_object method")
    except Exception as e:
        raise NetworksecurityException(e,sys)
                
def load_object(file_path:str,)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file {file_path} does not exist" )
        with open(file_path,"rb") as file_obj:
             print(file_obj)
             return pickle.load(file_obj)
    except Exception as e:
        raise NetworksecurityException(e,sys)


def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworksecurityException(e,sys)


def evaluate_m(x_train,y_train,x_test,y_test,models,param):
    try:
        report={}
        for key,model in models.items():
            logging.info(f"hypertuning for {key}")
            rv=RandomizedSearchCV(
                estimator=model,
                param_distributions=param[key],
                cv=3,
                scoring="r2",
                n_jobs=-1
            )
            rv.fit(x_train,y_train)
            model=rv.best_estimator_
            y_pred=model.predict(x_test)                              
            score=r2_score(y_test,y_pred)
            report[key]={
                "score":score,
                "model":model,
                "best_param":rv.best_params_
            }
        return report
    except Exception as e:
        raise NetworksecurityException(e,sys)
    
        
            
                    
                
    