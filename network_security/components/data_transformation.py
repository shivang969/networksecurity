import os
import pandas as pd
import numpy as np
from network_security.entity.artifact_entity import DataIngestionArtifact,DataTransforArtifact,DataValidArtifact
from network_security.entity.config_entity import DataIngestconfig,DataTransformConfig,DataValidationConfig
import sys
from network_security.constant import training_pipeline
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constant.training_pipeline import DATA_TANSFORMATION_IMPUTER_PARAMS

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidArtifact,
                 data_transformation_config:DataTransformConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    
    
    def get_data_transformer(cls)->Pipeline:
        logging.info("entered get_data_transformer object")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"intitialise knnimputer with {DATA_TANSFORMATION_IMPUTER_PARAMS}"
            )
            preprocessor=Pipeline([("imputer",imputer)])
            return preprocessor
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
        
    def initiate_data_transformation(self)->DataTransforArtifact:
        logging.info("entered data_transformation_method ")
        try:
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_train_df=train_df.drop(columns=[training_pipeline.TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[training_pipeline.TARGET_COLUMN]
            input_test_df=test_df.drop(columns=[training_pipeline.TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[training_pipeline.TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            preprocessor=self.get_data_transformer()
            preprocessor_obj=preprocessor.fit(input_train_df)
            transformed_input_train_feature=preprocessor_obj.transform(input_train_df)
            transformed_input_test_feature=preprocessor_obj.transform(input_test_df)
            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)
            save_object("final_model/preprocessor.pkl",preprocessor_obj)
            
            
            data_transformation_artifact=DataTransforArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path
            )
            
            return data_transformation_artifact            
            
            
        except Exception as e:
            raise NetworksecurityException(e,sys)        
        
        
