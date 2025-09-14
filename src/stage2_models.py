from sklearn.linear_model import ElasticNetCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import TimeSeriesSplit
import numpy as np
import joblib

def train_elasticnet(X, y, save_path=None):
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("enet", ElasticNetCV(cv=5, l1_ratio=[0.1,0.5,0.9],
                                n_alphas=50, random_state=42))
    ])
    model.fit(X, y)
    if save_path:
        joblib.dump(model, save_path)
    return model

def train_random_forest(X, y, n_estimators=300, max_depth=8, save_path=None):
    rf = RandomForestRegressor(
        n_estimators=n_estimators, max_depth=max_depth,
        random_state=42, n_jobs=-1
    )
    rf.fit(X, y)
    if save_path:
        joblib.dump(rf, save_path)
    return rf