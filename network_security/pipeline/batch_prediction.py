import pandas as pd
import os
import sys
import numpy as np
from network_security.exception.exception import NetworksecurityException   
from network_security.utils.main_utils.utils import load_object 
if __name__=="__main__":
    try:
        input_file_path=os.path.join("network_data","net.csv")
        df=pd.read_csv(input_file_path)
        df=df.drop(columns=["Result"],axis=1)
        model=load_object("final_model/model.pkl")
        preprecessor=load_object("final_model/preprocessor.pkl")
        y_pred=model.predict(preprecessor.transform(df))
        print(y_pred)
        df["predicted_result"]=y_pred
        output_file_path=os.path.join("network_data","predicted_net.csv")
        df.to_csv(output_file_path,index=False)
    except Exception as e:
        raise NetworksecurityException(e,sys)
        
        
