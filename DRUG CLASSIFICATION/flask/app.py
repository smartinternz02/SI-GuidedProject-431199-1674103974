from flask import Flask, render_template, request
import numpy as np
import pickle

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ekeuIk2TNfFCEym_f-b61LNFOG2YgHtnUok-XK92i1Q_"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#model = pickle.load(open(r'F:/notebook/drug/Drug classification/flask/model.pkl','rb'))
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
    payload_scoring = {"input_data": [{"field": ["Age","Sex","BP","Cholesterol","Na_to_K","Drug"], "values":total}]}

  #  prediction = model.predict(total)
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b31dc4af-3bfa-49cd-9c23-1dec85475f60/predictions?version=2023-02-10', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predict=response_scoring.json()
    pred=predict['predictions'][0]['values'][0][0]
    return render_template('index.html', prediction_text = 'Suitable drug type is {}'.format(pred))



if __name__ == "__main__":
    app.run(debug = False)
