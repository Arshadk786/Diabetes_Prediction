import pickle
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel


class predict(BaseModel):
    pregnancies: int
    glucose: float
    bloodpressure: float
    skinthickness: float
    insulin: float
    bmi: float
    diabetespedigreefunction: float
    age: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

# with open("s3://svcmodel/svc.pkl", "rb") as f:
#     clf = pickle.load(f)

s3 = boto3.client('s3')
response = s3.get_object(Bucket='svcmodel', Key='svc.pkl')
clf = pickle.loads(response['Body'].read())


#Index
@app.get('/')
def index():
    return {'message': 'Welcome to Diabetes Prediction API'}


#Predict
@app.post("/predict")
async def predict_diabetes(data: predict):
    try:
        data_list = pd.DataFrame([data.pregnancies, data.glucose, data.bloodpressure,
                      data.skinthickness, data.insulin, data.bmi,
                      data.diabetespedigreefunction, data.age])
        sc = StandardScaler()
        
        # Standardise the input data
        standardised_input = sc.fit_transform(data_list)

        # Make prediction using a trained model (clf)
        results = int(clf.predict(standardised_input.reshape(1, -1)))
        
        if results == 0:
            return f"You are Healthy"
        elif results == 1:
            return f"You have Diabetes"
    
        # return json.dumps(results)
    
    except Exception as e:
        # Return an appropriate error message if an exception occurs
        return {"error": str(e)}
 
    
    
    


