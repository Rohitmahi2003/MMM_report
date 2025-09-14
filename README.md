# Marketing Mix Modeling (MMM) with Mediation

This repository implements a **Marketing Mix Modeling (MMM)** pipeline to explain **Revenue** as a function of marketing spend, price, promotions, and CRM activity.  

We explicitly treat **Google spend as a mediator** between Social channels (Facebook, TikTok, Instagram, Snapchat) and Revenue.  
The project is designed to be **causally aware, reproducible, and product-oriented**.

---

## Objectives
- Quantify the impact of media and control variables on Revenue.  
- Capture **carryover (Adstock)** and **diminishing returns (Saturation)**.  
- Respect causal structure: **Social → Google → Revenue** (mediated effect).  
- Validate using **time-series CV** (no look-ahead).  
- Provide **diagnostics, sensitivity tests, ROAS estimates, and stability checks**.  
- Deliver **practical recommendations** for marketing/growth teams.  

---

## Causal Framing

We assume that part of Social’s effect on Revenue is **mediated by Google spend** (social ads trigger search intent → higher Google spend → revenue). At the same time, Social may have a **direct effect** on Revenue.  

Controls (Price, Promotions, Emails, SMS, Seasonality, Trend) adjust for confounding.

### DAG

![Causal DAG](artifacts/figures/causal_dag.png)

- **Social → Google → Revenue** = *Indirect (mediated) effect*  
- **Social → Revenue** = *Direct effect*  
- **Controls → Revenue** = adjustment for confounding  
- We use **residualized Google** to avoid leakage.  

---

## 📊 Modeling Approach

### 1. Data Preparation
- Handle missing/zero spends with forward fill → 0.  
- Apply **Adstock** (θ=0.6, lags=8).  
- Apply **Saturation** (Hill transform, half-sat = 70th percentile).  
- Add **Trend & Seasonality** (time index, sin/cos terms).  

### 2. Stage 1 – Mediator Model
- `Google Spend ~ Social Channels`  
- Extract:
  - `google_pred` (predicted Google from social)  
  - `google_resid` (residual, non-social Google component)  

### 3. Stage 2 – Revenue Model
- `Revenue ~ Social_sat + google_resid + Controls`  
- **ElasticNet** (main interpretable model).  
- **Random Forest** (non-linear benchmark).  
- **Validation:** TimeSeriesSplit (5 folds).  

### 4. Diagnostics
- Predicted vs Actual plots  
- Residuals over time  
- Rolling stability checks  

### 5. Mediation Effects
- Decompose **direct vs indirect** effects for each social channel.  

### 6. Sensitivity Analysis
- Price elasticity: ±10%  
- Promotions ON vs OFF  

### 7. ROAS
- Marginal ROAS from +5% spend scenarios.  

---

## 📂 Project Structure

MMM-Project/
├── README.md # How to run (this file)
├── REPORT.md # Analysis write-up (stakeholder-facing)
├── requirements.txt # Environment (pinned versions)
├── MMM_end_to_end.ipynb # End-to-end notebook
│
├── data/
│ └── weekly_data.csv # Input dataset
│
├── artifacts/
│ ├── enet_coefs.csv
│ ├── predictions_test.csv
│ ├── rf_importances.csv
│ ├── rf_predictions_oof.csv
│ ├── mediation_effects.csv
│ ├── sensitivity_summary.csv
│ ├── roas_table.csv
│ ├── rolling_scores.csv
│ ├── stage2_enet.pkl
│ ├── rf_stage2.pkl
│ └── figures/
│ ├── pred_vs_actual.png
│ ├── residuals_over_time.png
│ ├── rf_top20_importances.png
│ ├── price_sensitivity.png
│ ├── promo_lift.png
│ ├── roas_bars.png
│ ├── rolling_performance.png
│ └── causal_dag.png

yaml
Copy code

---

## ▶️ How to Run

### Option 1 — Google Colab
1. Mount Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
Copy repo into Drive.

Open MMM_end_to_end.ipynb.

Run all cells → outputs saved to /artifacts/.

Option 2 — Local
Clone repo.

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Put weekly_data.csv in /data/.

Run MMM_end_to_end.ipynb.

Outputs will be in /artifacts/.

📊 Key Outputs
Coefficients: enet_coefs.csv

Predictions: predictions_test.csv

Mediation effects: mediation_effects.csv

Sensitivity analysis: sensitivity_summary.csv

ROAS table: roas_table.csv

Rolling scores: rolling_scores.csv

Figures: prediction fit, residuals, importances, sensitivity, ROAS, rolling performance, DAG.

💡 Insights & Recommendations
Social impact: some channels have positive direct effects but negative indirect (via Google).

Snapchat: negative both ways → candidate for budget reduction.

Pricing: highly elastic; increases reduce revenue unless offset by promotions.

Promotions: selective promos provide lift; avoid always-on.

ROAS: use marginal ROAS for budget allocation.

Stability: coefficients vary → suggests structural changes; RF/boosting as robustness checks.

✅ Reproducibility
Deterministic results (fixed seed).

Dependencies pinned in requirements.txt.

Notebook runs end-to-end.

Artifacts saved in /artifacts/.

