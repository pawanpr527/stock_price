import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from data_loader import data_load
import yfinance as yf
def lstm_sequence(df, feature_col, target_col, sequence=60):
    X, y = [], []
    for i in range(sequence, len(df) - 1):
        X_seq = df[feature_col].iloc[i-sequence:i].values
        y_val = df[target_col[0]].iloc[i + 1]
        X.append(X_seq)
        y.append(y_val)
    X = np.array(X)
    y = np.array(y)
    return X, y

def model_building(df):
    feature = ['Close', 'High', 'Low', 'Open', 'Volume']
    target = ['Target']
    df.dropna(inplace=True)
    x_train, y_train = lstm_sequence(df, feature, target)
    return x_train


def prediction(stock_model):
    from tensorflow.keras.models import load_model

    model = load_model(f'model/{stock_model}.h5', compile=False)

    # Download at least 61 rows
    raw_data = yf.Ticker(f'{stock_model}.NS').history(period='max')
    
    loader = data_load(raw_data)
    df = loader.get_data()
    target_scaler = loader.get_target_scaler()

    x_input = model_building(df)
    last_input = x_input[-1]          # shape: (60, 5)
    last_input = last_input.reshape((1, 60, 5))  # shape: (1, 60, 5) → ready for prediction

    print("x_input shape:", last_input.shape)  # Should be (1, 60, 5)
    
    predict = model.predict(last_input, verbose=0)
    real_output = target_scaler.inverse_transform(predict)
    
    print("Predicted next target:", real_output[0][0])

indian_stocks = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
    "ICICIBANK.NS", "HINDUNILVR.NS", "SBIN.NS", "LT.NS",
    "AXISBANK.NS", "KOTAKBANK.NS", "BHARTIARTL.NS", "ITC.NS", "MARUTI.NS",
    "HCLTECH.NS", "WIPRO.NS", "TATAMOTORS.NS", "BAJFINANCE.NS", "ASIANPAINT.NS",
    "NTPC.NS", "POWERGRID.NS", "COCHINSHIP.NS", "GRSE.NS", "BSE.NS",
    "CYIENT.NS", "ADANIPOWER.NS"
]
indian_stocks = [i.replace('.NS','') for i in indian_stocks]
for i in range(5):
   print(indian_stocks[i])
   prediction(indian_stocks[i])

