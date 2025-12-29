import sys
from network_security.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINED_MODEL_NAME
from network_security.logging.logger import logging
from network_security.exception.exception import NetworksecurityException

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
           raise NetworksecurityException(e,sys)
    
          
        
