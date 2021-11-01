# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 16:16:53 2021

@author: Diego Cortínez
"""
import requests
import json

customer = {
'age'	:	19,
'sex'	:	'female',
'bmi'	:	27.9,
'children'	:	0,
'smoker'	:	'yes',
'region'	:	'southwest'
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=customer)
result = response.json()

print(json.dumps(result, indent=2))






