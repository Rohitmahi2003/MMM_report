import numpy as np
import pandas as pd

def apply_adstock(x, theta=0.6, lags=8):
    x = np.array(x)
    x_adstock = np.zeros_like(x)
    for i in range(len(x)):
        for l in range(0, min(lags+1, i+1)):
            x_adstock[i] += x[i - l] * (theta ** l)
    return x_adstock

def apply_saturation(x, half_saturation):
    return x / (x + half_saturation)

def add_trend_seasonality(df):
    df = df.copy()
    df['trend'] = np.arange(len(df))
    df['week_of_year'] = df['week'].dt.isocalendar().week.astype(int)
    df['sin_52'] = np.sin(2 * np.pi * df['week_of_year'] / 52)
    df['cos_52'] = np.cos(2 * np.pi * df['week_of_year'] / 52)
    df['sin_26'] = np.sin(2 * np.pi * df['week_of_year'] / 26)
    return df