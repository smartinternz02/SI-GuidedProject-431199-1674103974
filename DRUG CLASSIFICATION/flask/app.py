from flask import Flask, render_template, request
import numpy as np
import pickle


model = pickle.load(open(r'D:\Drug classification\flask\model.pkl','rb'))
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
    prediction = model.predict(total)
    return render_template('index.html', prediction_text = 'Suitable drug type is {}'.format(prediction))



if __name__ == "__main__":
    app.run(debug = False)
