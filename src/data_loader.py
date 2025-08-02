import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class data_load:
    def __init__(self, data):
        self.yahoo_data = data
        self.df = self._load_data()
        self._preprocess()
        self.target_scaler = MinMaxScaler()  # <-- store target scaler
        self._scale_feature()

    def _load_data(self):
        df_d = self.yahoo_data
        df = df_d.copy()
        df.index = pd.to_datetime(df.index).tz_localize(None).date
        numeric = ['Close', 'High', 'Low', 'Open', 'Volume']
        df = df[numeric]
        df['Target'] = df['Close'].shift(-1)
        df.dropna(inplace=True)
        return df
    
    def real_target(target):
        new_target = target
        return new_target
    def _preprocess(self):
        numeric_column = ['Close', 'High', 'Low', 'Open', 'Volume']
        self.df[numeric_column] = self.df[numeric_column].apply(pd.to_numeric)

    def _scale_feature(self):
       self.feature_scaler = MinMaxScaler()
       numeric_column = ['Close', 'High', 'Low', 'Open', 'Volume']
       
       if self.df.empty:
          raise ValueError("DataFrame is empty before scaling!")

       self.df[numeric_column] = self.feature_scaler.fit_transform(self.df[numeric_column])

       if self.df[['Target']].dropna().empty:
          raise ValueError("Target column is empty after shift.")

        # scale target using stored target_scaler
       self.df[['Target']] = self.target_scaler.fit_transform(self.df[['Target']])

    def get_data(self):
        return self.df.copy()

    def get_target_scaler(self):
        return self.target_scaler  # <-- added method
# x=data_load('data/bse_data.csv')
# y = x.get(61).reshape(-1,1)
# z = x.target_scaler.inverse_transform(y)
# print(z)
