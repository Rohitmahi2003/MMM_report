import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_percentage_error

def plot_pred_vs_actual(dates, y_true, y_pred, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(dates, y_true, label="Actual", color="black")
    plt.plot(dates, y_pred, label="Predicted", color="red")
    plt.legend()
    plt.title("Predicted vs Actual Revenue")
    if save_path: plt.savefig(save_path, dpi=300)
    plt.close()

def plot_residuals(dates, residuals, save_path=None):
    plt.figure(figsize=(10,4))
    plt.plot(dates, residuals, color="blue")
    plt.axhline(0, color="red", linestyle="--")
    plt.title("Residuals Over Time")
    if save_path: plt.savefig(save_path, dpi=300)
    plt.close()

def rolling_cv(df, model, features, target="revenue", step=4, save_path=None):
    X = df[features].values
    y = df[target].values
    weeks = df["week"].values

    results = []
    train_size = int(len(df) * 0.7)
    test_size = int(len(df) * 0.1)

    for start in range(0, len(df) - (train_size + test_size), step):
        train_idx = range(start, start + train_size)
        test_idx = range(start + train_size, start + train_size + test_size)

        model.fit(X[train_idx], y[train_idx])
        y_pred = model.predict(X[test_idx])

        r2 = r2_score(y[test_idx], y_pred)
        mape = mean_absolute_percentage_error(y[test_idx], y_pred)

        results.append({
            "start_week": weeks[train_idx[0]],
            "end_week": weeks[test_idx[-1]],
            "R2": r2,
            "MAPE": mape
        })

    results_df = pd.DataFrame(results)
    if save_path:
        results_df.to_csv(save_path, index=False)
    return results_df