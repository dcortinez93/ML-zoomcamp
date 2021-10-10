# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 17:56:59 2021

@author: Diego Cortínez
"""
import requests

url = "http://localhost:9696/predict"
customer = {"contract": "two_year", "tenure": 1, "monthlycharges": 10}

res = requests.post(url, json=customer).json()
print(res)