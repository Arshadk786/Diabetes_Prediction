import pickle
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
from mangum import Mangum


class predict(BaseModel):
    pregnancies: int = Query(..., description="Number of pregnancies", ge=0)
    glucose: float = Query(..., description="Glucose level", ge=0)
    bloodpressure: float = Query(..., description="Blood pressure", ge=0)
    skinthickness: float = Query(..., description="Skin thickness", ge=0)
    insulin: float = Query(..., description="Insulin level", ge=0)
    bmi: float = Query(..., description="Body Mass Index (BMI)", ge=0)
    diabetespedigreefunction: float = Query(..., description="Diabetes pedigree function", ge=0)
    age: int = Query(..., description="Age", ge=0)

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

with open("../svc.pkl", "rb") as f:
    clf = pickle.load(f)

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
            return f"You have Diabetes, You gonna die nigga!!"
    
        # return json.dumps(results)
    
    except Exception as e:
        # Return an appropriate error message if an exception occurs
        return {"error": str(e)}
 
    
    
    


