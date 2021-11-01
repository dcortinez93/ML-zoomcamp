# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 16:16:53 2021

@author: Diego Cortínez
"""
import pickle
import numpy as np
from flask import Flask
from flask import request
from flask import jsonify


with open('./model.bin', 'rb') as f_in:
	dv, model = pickle.load(f_in)

# with open('./dv.bin', 'rb') as f_in:
# 	dv = pickle.load(f_in)

app = Flask('predict')

@app.route('/predict', methods=['POST'])
def predict():
	customer = request.get_json()

	X = dv.transform([customer])
	y_pred = model.predict(X)
	result = {'insurance cost': float((np.expm1(y_pred)))
           
           }
	return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)


