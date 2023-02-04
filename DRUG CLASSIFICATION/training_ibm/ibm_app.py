from flask import Flask, render_template, request
import numpy as np
import requests
import pickle
import json

API_KEY = "_uQJaQRra2V-2lHNbQY1-q314HMfQ3Rkw1ZhkFeVDtWN"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict',methods =['GET','POST'])
def predict():
    age = request.form['Age']
    sex = request.form['Sex']
    if sex == 'MALE':
        sex = 1
    if sex == 'FEMALE':
        sex = 0
    bp = request.form['BP']
    if bp == 'LOW':
        bp = 0
    if bp == 'NORMAL':
        bp = 1
    if bp == 'HIGH':
        bp = 2
    cholesterol = request.form['Cholesterol']
    if cholesterol == 'NORMAL':
        cholesterol = 0
    if cholesterol == 'HIGH':
        cholesterol = 1
    na_to_k = request.form['Na_to_K']
    total = [[age,sex,bp,cholesterol,na_to_k]]
    
    payload_scoring = {"input_data": [{"field": [["pH","Temprature", "Taste","Odor", "Fat","Turbidity","Colour"]], "values": [[8.5,70,1,1,1,1,246]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f7293f6f-67be-4c43-9eb5-917a520bac11/predictions?version=2022-06-07', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    
    
if __name__ == "__main__":
    app.run(debug = True)