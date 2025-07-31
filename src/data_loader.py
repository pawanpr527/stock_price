import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
class data_loader:
    def __init__(self,file):
        self.filepath = file
        self.df = self._load_data()
        self._preprocess()
        self._scale_feature()

    def _load_data(self):
        df = pd.read_csv(self.filepath)
        df=df.iloc[2:].copy()
        df.columns = ['Date','Close','High','Low','Open','Volume'] 
        df.set_index('Date',inplace=True)
        return df
    
    def _preprocess(self):
        numeric_column = ['Close','High','Low','Open','Volume']
        self.df[numeric_column] = self.df[numeric_column].apply(pd.to_numeric)
        self.df['Target'] = self.df['Close'].shift(-1)
    
    def _scale_feature(self):
        scale = MinMaxScaler()
        self.df['Scale_Volume'] = scale.fit_transform(self.df[['Volume']])
        
    def get_data(self):
        return self.df.copy()
    def head(self,n=5):
        return self.df.head(n)