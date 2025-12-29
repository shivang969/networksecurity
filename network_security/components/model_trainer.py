import os
import pandas as pd
import numpy as np
from network_security.entity.artifact_entity import DataIngestionArtifact,DataTransforArtifact,DataValidArtifact,ModelTrainerArtifact
from network_security.entity.config_entity import DataIngestconfig,DataTransformConfig,DataValidationConfig
import sys
from network_security.constant import training_pipeline
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object,evaluate_m
from network_security.constant.training_pipeline import DATA_TANSFORMATION_IMPUTER_PARAMS
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object,load_numpy_array_data,load_object
from network_security.entity.config_entity import ModelTrainerConfig
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transfromation_artifact:DataTransforArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transfromation_artifact
            
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
                "RandomForest": RandomForestClassifier(verbose=1),
                "DecisionTree": DecisionTreeClassifier(),
                "GradientBoosting": GradientBoostingClassifier(verbose=1),
                "LogisticRegression": LogisticRegression(max_iter=1000),
                "AdaBoost": AdaBoostClassifier(),
                "KNN": KNeighborsClassifier()
            }
        
        param_grids = {

            "RandomForest": {
                "n_estimators": [100, 200, 500],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "bootstrap": [True, False]
            },

            "DecisionTree": {
                "max_depth": [None, 5, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "criterion": ["gini", "entropy"]
            },

            "GradientBoosting": {
                "n_estimators": [100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "subsample": [0.8, 1.0]
            },

            "LogisticRegression": {
                "C": [0.01, 0.1, 1, 10, 100],
                "penalty": ["l1", "l2"],
                "solver": ["liblinear"],
                "max_iter": [200, 500, 1000]
            },

            "AdaBoost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 1.0]
            },

            "KNN": {
                "n_neighbors": [3, 5, 7, 9, 11],
                "weights": ["uniform", "distance"],
                "metric": ["euclidean", "manhattan", "minkowski"]
            }
        }

        
        model_report=evaluate_m(x_train,y_train,x_test,y_test,models,param_grids)
        best_model_name=max(
            model_report,
            key=lambda x: model_report[x]["score"]
        )
        best_model=model_report[best_model_name]["model"]
        best_model_score=model_report[best_model_name]["score"]
        best_params=model_report[best_model_name]["best_param"]
        y_test_pred=best_model.predict(x_test)
        y_train_pred=best_model.predict(x_train)
        classification_test_report=get_classification_score(y_test_pred,y_test)
        classification_train_report=get_classification_score(y_train_pred,y_train)
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.model_trainer_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        Network_Model=NetworkModel(preprocessor,best_model)
        save_object(self.model_trainer_config.model_trainer_file_path,Network_Model)
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=model_dir_path,
        train_metric_artifact=classification_train_report,
        test_metric_artifact=classification_test_report)
        
        logging.info(f" Model trainer artifact {model_trainer_artifact}")
        return model_trainer_artifact
       
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
        