# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 16:22:19 2021

@author: Diego Cortínez
"""
import pandas as pd
import numpy as np

df = pd.read_csv (r'C:\Users\Diego Cortínez\Desktop\Tarea 1\data.csv')
#1
print(f"Numpy version: {np.__version__}")

#2
print(f"Pandas version: {pd.__version__}")


#3
print(f"Average price of BMW cars in the dataset : {df[df['Make'] == 'BMW'].groupby('Make').MSRP.mean().values[0]}")

#4
print(f"Missing values for Engine HP : {df[df['Year'] >= 2015]['Engine HP'].isnull().sum()}")

#5
mean_hp_before = df['Engine HP'].mean()
df['Engine HP'] = df['Engine HP'].fillna(mean_hp_before)
mean_hp_after = df['Engine HP'].mean()

print(f"rounded mean before : {round(mean_hp_before)}. ")
print(f"rounded mean before : {round(mean_hp_after)}. ")

#6
filtered = df[df['Make'] == 'Rolls-Royce'][["Engine HP", "Engine Cylinders", "highway MPG"]].drop_duplicates()
#X = np.log1p(filtered.values)
X = filtered.values
XTX = X.T.dot(X)
XTX_inv = np.linalg.inv(XTX)
print("Sum of all the elements of XTX_inv: "+ str(XTX_inv.sum()))

#7
y = [1000, 1100, 900, 1200, 1000, 850, 1300]
w = (XTX_inv.dot(X.T)).dot(y)
print("First element of w : " +str(w[0]))