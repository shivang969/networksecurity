import os
import sys
import fastapi
import certifi
import io
ca=certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.exception.exception import NetworksecurityException
from network_security.logging.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,requests,UploadFile,File
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from network_security.utils.main_utils.utils import load_object
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
from network_security.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])

async def index():
    return RedirectResponse(url="/docs")


@app.get("/train",tags=["training"])
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("training successfull")
    except Exception as e:
        raise NetworksecurityException(e,sys)
    

@app.post("/predict", tags=["prediction"])  # Changed to POST
async def predict_route(file: UploadFile = File(...)):
    try:
        # Read file content properly
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        model = load_object("final_model/model.pkl")
        preprocessor = load_object("final_model/preprocessor.pkl")  # Fixed typo
        
        # Check if 'Result' column exists before dropping
        if "Result" in df.columns:
            input_feature = df.drop(columns=["Result"], axis=1)
        else:
            input_feature = df
        
        # Transform and predict
        transformed_data = preprocessor.transform(input_feature)
        prediction = model.predict(transformed_data)
        
        return {"prediction": prediction.tolist()}
    
    except Exception as e:
        raise NetworksecurityException(e, sys)
    


if __name__=="__main__":
    app_run(app,host="localhost",port=8000)
        