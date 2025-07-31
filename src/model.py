# Deep Learning Model LSTM
import pandas as pd
from tensorflow.keras.models import Sequential
import numpy as np
from data_loader import data_load
def lstm_sequence(df,feature_col,target_col,sequence=60):
    X,y = [],[]
    for i in range(sequence,len(df)-1):
        X.append(df[feature_col].iloc[i-sequence:i].values)
        y.append(df.iloc[i+1][target_col])
    return np.array(X),np.array(y)

feature = ['Close','High','Low','Open','Volume']
target = ['Target']
df = data_load('data/bse_data.csv').get_data()
x_tarin , y_train = lstm_sequence(df,feature,target)

def train_lstm_model(X,y,epoch=30,batch_size=32):
    split = int(0.8*len(X))
    X_train,X_test = X[:split],X[split:]
    Y_train,Y_test = y[:split],y[split:]

def model_building():
    pass