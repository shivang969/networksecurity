from network_security.entity.artifact_entity import ClassificationMetrices
from network_security.exception.exception import NetworksecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import os,sys

def get_classification_score(y_true,y_pred)->ClassificationMetrices:
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)
        Classification_metrices=ClassificationMetrices(
            precision_score=model_precision_score,
            f1_score=model_f1_score,
            recall_score=model_recall_score
        )
        return Classification_metrices
    except Exception as e:
        raise NetworksecurityException(e,sys)    
        
        