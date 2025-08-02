import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout,BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error
from src.data_loader import data_load

def lstm_sequence(df, feature_col, target_col, sequence=60):
    X, y = [], []
    for i in range(sequence, len(df) - 1):
        X_seq = df[feature_col].iloc[i-sequence:i].values
        y_val = df[target_col[0]].iloc[i + 1]
        X.append(X_seq)
        y.append(y_val)
    X = np.array(X)
    y = np.array(y)
    print(f"Built sequence: X.shape={X.shape}, y.shape={y.shape}")
    return X, y

def model_building(file):
    feature = ['Close', 'High', 'Low', 'Open', 'Volume']
    target = ['Target']
    df = data_load(file).get_data()
    df.dropna(inplace=True)
    x_train, y_train = lstm_sequence(df, feature, target)
    print("X shape:", x_train.shape)
    print("y shape:", y_train.shape)
    return x_train, y_train

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm_model(X, y, epoch=10, batch_size=32):

    split = int(0.8 * len(X))

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = build_lstm_model((X.shape[1], X.shape[2]))

    es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    model.fit(X_train, y_train, validation_data=(X_test, y_test),
              epochs=epoch, batch_size=batch_size,
              callbacks=[es], verbose=1)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test.ravel(), y_pred.ravel())
    
    print(f"Test MSE: {mse:.4f}")
    
    return model,y_pred




