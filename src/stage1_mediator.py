import statsmodels.api as sm
import pandas as pd

def fit_google_residuals(df, social_features, google_col="google_spend"):
    X = sm.add_constant(df[social_features])
    y = df[google_col]
    model = sm.OLS(y, X).fit()
    df["google_pred"] = model.predict(X)
    df["google_resid"] = y - df["google_pred"]
    return df, model