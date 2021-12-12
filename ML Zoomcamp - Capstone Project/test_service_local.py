# -*- coding: utf-8 -*-

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

url = 'http://localhost:9696/predict'
response = requests.post(url, json=patient)
result = response.json()

print(json.dumps(result, indent=2))