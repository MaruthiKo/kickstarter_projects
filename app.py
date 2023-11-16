import pandas as pd
import requests
import json
import streamlit as st
from pipelines.training_pipeline import DataPreprocessor


preprocessor = DataPreprocessor("./data/data.csv")
df = preprocessor.preprocess()

def run():
    st.title("Kickstarter Project Success Prediction")
    parent_category = st.selectbox("Parent Category", df["parent_category"].unique())
    sub_category = st.selectbox("Sub Category", df["sub_category"].unique())
    days = st.number_input("Number of Days", min_value=1, max_value=120)
    backers_count = st.number_input("Number of Backers")
    pledged_amt = st.number_input("Pledged Amount")
    converted_pledged_amt = st.number_input("Converted Pledged Amount")
    goal = st.number_input("Goal")
    country = st.selectbox("Country", df["country"].unique())

    data = {
        'parent_category': parent_category,
        'sub_category': sub_category,
        'days': days,
        'backers_count': backers_count,
        'pledged_amt': pledged_amt,
        'converted_pledged_amt': converted_pledged_amt,
        'goal': goal,
        'country': country
    }

    if st.button("Predict"):
        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        prediction = response.json()
        if prediction == "1":
            st.success("The project is going to be successful")
            # print("The project is going to be successful")
        elif prediction == "0":
            st.error("The project is likely to fail. Don't lose hope! Keep trying")
            # print("The project is likely to fail. Don't lose hope!, Keep trying")

if __name__ == "__main__":
    run()
