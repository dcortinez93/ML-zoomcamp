# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 16:06:29 2021

@author: Diego Cortínez
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import ExtraTreesRegressor
import pickle

df = pd.read_csv('insurance.csv')
numerical_columns = ["age","bmi","children"]
categorical_columns = ["sex","smoker","region"]
columns = numerical_columns + categorical_columns
df = df.drop_duplicates()

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)


df_test = df_test.reset_index(drop=True)
df_full_train = df_full_train.reset_index(drop=True)


y_full_train = df_full_train.charges.values
y_test = df_test.charges.values


del df_test['charges']
del df_full_train['charges']


y_full_train = np.log1p(y_full_train)
y_test = np.log1p(y_test)

#One Hot Encoding
full_train_dict = df_full_train[categorical_columns +numerical_columns].to_dict(orient='records')

dv = DictVectorizer(sparse=False)
dv.fit(full_train_dict)
X_full_train = dv.transform(full_train_dict)

test_dict = df_test[categorical_columns +numerical_columns].to_dict(orient='records')
X_test = dv.transform(test_dict)

model = ExtraTreesRegressor(n_estimators=90, max_depth=5, min_samples_leaf=1, random_state=1)
model.fit(X_full_train, y_full_train)
y_full_train_pred_et = model.predict(X_full_train)
y_test_pred_et = model.predict(X_test)
print(f"MSE test data: {round((mean_squared_error(y_test,y_test_pred_et)),3)}")
print(f"R^2 test data: {round((r2_score(y_test,y_test_pred_et)),3)}")

#Saving the model
output_file ='model.bin'
f_out = open(output_file, 'wb') 
pickle.dump((dv, model), f_out)
f_out.close()