from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np
import pandas as pd
import joblib

app = FastAPI(title='Project Success Prediction', version='1.0', description='KNN Model is used for prediciton')

model = joblib.load('./success_pred_model.pkl')

class Data(BaseModel):
    parent_category: str
    sub_category: str
    days: int
    backers_count: int
    pledged_amt: float
    converted_pledged_amt: float
    goal: int
    country: str


@app.get("/")
@app.get("/home")

def read_home():
    """
    Home page to check if the app is running
    """

    return {"message": "Welcome to the Kickstarter Success Prediction App"}

@app.post("/predict")
def predict(data: Data):
    result = model.predict(pd.DataFrame(columns=['parent_category', 'sub_category', 'days', 'backers_count', 'pledged_amt', 'converted_pledged_amt', 'goal', 'country'], 
                           data=np.array([data.parent_category, data.sub_category, data.days, data.backers_count, data.pledged_amt, data.converted_pledged_amt, data.goal, data.country]).reshape(1, -1)))
    return str(result)[1]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)