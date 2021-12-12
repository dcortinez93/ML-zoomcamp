# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 12:14:22 2021

@author: Diego Cortínez
"""
import requests
import json

patient = {
"age"	:	90,
"gender"	:	"man",
"height"	:	150,
"weight"	:	85,
"ap_hi"		:	110,
"ap_lo"		:	70,
"cholesterol"	:	"well above normal",
"gluc"		:	"well above normal",
"smoke"		:	1,
"alco"		:	1,
"active"	:	0	
}

url = 'https://capstone-cardio.herokuapp.com/predict'
response = requests.post(url, json=patient)
result = response.json()

print(json.dumps(result, indent=2))