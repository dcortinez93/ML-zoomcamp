# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv('cardio_train.csv',sep=";")
df = df.drop(df.columns[0],axis=1)
gender_values = {
    1: 'woman',
    2: 'man',
}

df.gender = df.gender.map(gender_values)

cholesterol_values = {
    1: 'normal',
    2: 'above normal',
    3: 'well above normal'
}

df.cholesterol = df.cholesterol.map(cholesterol_values)

gluc_values = {
    1: 'normal',
    2: 'above normal',
    3: 'well above normal'
}

df.gluc = df.gluc.map(gluc_values)

cardio_values = {
    0: 'no',
    1: 'yes',
}

df.cardio = df.cardio.map(cardio_values)
df.age = np.round(df.age/365.25,decimals=1)
df.smoke = df.smoke.astype('object')
df.alco = df.alco.astype('object')
df.active = df.active.astype('object')
df.cardio = df.cardio.astype('object')

numerical_columns = ["age","height","weight", "ap_hi", "ap_lo"]
categorical_columns = ["gender","cholesterol","gluc", "smoke", "alco", "active"]
columns = numerical_columns + categorical_columns

df = df.drop_duplicates()

#Setting up the validation framework
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
df_test = df_test.reset_index(drop=True)
df_full_train = df_full_train.reset_index(drop=True)


#Outliers
df_full_train.drop(df_full_train[(df_full_train['height'] > df_full_train['height'].quantile(0.99)) | (df_full_train['height'] < df_full_train['height'].quantile(0.01))].index,inplace=True)
df_full_train.drop(df_full_train[(df_full_train['weight'] > df_full_train['weight'].quantile(0.99)) | (df_full_train['weight'] < df_full_train['weight'].quantile(0.01))].index,inplace=True)
df_full_train.drop(df_full_train[(df_full_train['ap_hi'] > df_full_train['ap_hi'].quantile(0.99)) | (df_full_train['ap_hi'] < df_full_train['ap_hi'].quantile(0.01))].index,inplace=True)
df_full_train.drop(df_full_train[(df_full_train['ap_lo'] > df_full_train['ap_lo'].quantile(0.99)) | (df_full_train['ap_lo'] < df_full_train['ap_lo'].quantile(0.01))].index,inplace=True)
df_full_train.drop(df_full_train[(df_full_train['ap_lo'] > df_full_train['ap_lo'].quantile(0.98))].index,inplace=True)
df_full_train.drop(df_full_train[(df_full_train['ap_hi'] > df_full_train['ap_hi'].quantile(0.99))].index,inplace=True)
df_full_train.drop(df_full_train[(df_full_train['age'] > df_full_train['age'].quantile(0.99)) | (df_full_train['age'] < df_full_train['age'].quantile(0.01))].index,inplace=True)

df_test.drop(df_test[(df_test['height'] > df_test['height'].quantile(0.99)) | (df_test['height'] < df_test['height'].quantile(0.01))].index,inplace=True)
df_test.drop(df_test[(df_test['weight'] > df_test['weight'].quantile(0.99)) | (df_test['weight'] < df_test['weight'].quantile(0.01))].index,inplace=True)
df_test.drop(df_test[(df_test['ap_hi'] > df_test['ap_hi'].quantile(0.99)) | (df_test['ap_hi'] < df_test['ap_hi'].quantile(0.01))].index,inplace=True)
df_test.drop(df_test[(df_test['ap_lo'] > df_test['ap_lo'].quantile(0.99)) | (df_test['ap_lo'] < df_test['ap_lo'].quantile(0.01))].index,inplace=True)
df_test.drop(df_test[(df_test['ap_lo'] > df_test['ap_lo'].quantile(0.98))].index,inplace=True)
df_test.drop(df_test[(df_test['ap_hi'] > df_test['ap_hi'].quantile(0.99))].index,inplace=True)
df_test.drop(df_test[(df_test['age'] > df_test['age'].quantile(0.99)) | (df_test['age'] < df_test['age'].quantile(0.01))].index,inplace=True)

df_full_train.cardio = df_full_train.cardio.astype('object')
df_test.cardio = df_test.cardio.astype('object')


y_full_train = df_full_train.cardio.values
y_test = df_test.cardio.values



del df_test['cardio']
del df_full_train['cardio']


#One Hot Encoding
dv = DictVectorizer(sparse=False)
full_train_dict = df_full_train.to_dict(orient='records')
test_dict = df_test.to_dict(orient='records')
X_full_train = dv.fit_transform(full_train_dict)
X_test = dv.transform(test_dict)

r = 3 
md = 10
s = 3
f = 5
n = 80
model = RandomForestClassifier(n_estimators=n, max_depth=md, max_features=f, min_samples_leaf=s, random_state=r, n_jobs=-1)
model.fit(X_full_train, y_full_train)
y_pred_test = model.predict_proba(X_test)[:,1]
auc_test = roc_auc_score(y_test, y_pred_test)
y_pred_full_train = model.predict_proba(X_full_train)[:,1]
auc_full_train = roc_auc_score(y_full_train, y_pred_full_train)
print(f"AUC train data: {round(auc_full_train,3)}")
print(f"AUC val data: {round(auc_test,3)}")

#Saving the model
output_file ='model.bin'
f_out = open(output_file, 'wb') 
pickle.dump((dv, model), f_out)
f_out.close()