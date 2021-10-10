# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 17:37:17 2021

@author: Diego Cortínez
"""
import pickle

with open('./dv.bin', 'rb') as f_in:
	dv = pickle.load(f_in)

with open('./model1.bin', 'rb') as f_in:
	model = pickle.load(f_in)

customer = {"contract": "two_year", "tenure": 12, "monthlycharges": 19.7}

X = dv.transform([customer])

score = model.predict_proba(X)[0, 1]
print(f"Probability a custom is churning: {round(score,3)}")


