# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 10:55:36 2021

@author: Diego Cortínez
"""
import pickle
from flask import Flask
from flask import request
from flask import jsonify
import os

with open('model.bin', 'rb') as f_model:
    dv, model = pickle.load(f_model)

app = Flask('predict')

def predict_single(patient, dv, model):
    X = dv.transform([patient])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]

@app.route('/welcome', methods=['GET'])
def welcome():
    welcome_msg = "<h1>Welcome!</h1>"
    return welcome_msg

@app.route('/predict', methods=['POST'])
def predict():
    patient = request.get_json()
    y_pred = predict_single(patient, dv, model)
    disease = y_pred >= 0.5

    result = {
        "Cardiovascular Disease  Probability": float(y_pred),
        "Disease": bool(disease)
    }
    return jsonify(result)


if __name__ == "__main__":
     current_port = int(os.environ.get("PORT") or 9696)
     app.run(debug=True, host="0.0.0.0", port=current_port) 
     