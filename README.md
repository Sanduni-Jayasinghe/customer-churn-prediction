# Customer Churn Prediction

## 📊 Project Overview
This project predicts which telecom customers are likely to churn using machine learning classification models. The analysis identifies key drivers of churn and provides actionable business recommendations.

## 🎯 Key Features
- **Exploratory Data Analysis** - Understanding churn patterns and customer behavior
- **Feature Engineering** - Created 4 new features for better predictions
- **Multiple Models** - Logistic Regression, Random Forest, XGBoost
- **Hyperparameter Tuning** - GridSearchCV optimization for XGBoost
- **Leak-Free Validation** - Train/validation/test split, with the classification threshold selected on the validation set only, so test metrics stay an unbiased final check
- **SHAP Analysis** - Deep model interpretability
- **Business Dashboard** - Actionable recommendations for retention strategies, deployed live with Streamlit

## 📁 Project Structure
```
customer-churn-prediction/
├── Customer_Churn_Prediction.ipynb   # Main Jupyter notebook
├── dashboard.py                      # Streamlit dashboard app
├── data/
│   └── telco_churn.csv               # Dataset
├── outputs/
│   ├── figures/                      # All visualizations (13 plots)
│   ├── best_xgb_model.pkl            # Trained model
│   ├── classification_report.txt     # Model metrics
│   ├── model_comparison.csv          # Performance comparison
│   ├── feature_importance_rf.csv     # RF feature importance
│   ├── feature_importance_xgb.csv    # XGB feature importance
│   └── business_recommendations.txt  # Business insights
└── README.md                         # This file
```

## 🚀 Models Compared
Evaluated on a held-out test set that was never touched during training, tuning, or threshold selection:

| Model                  | ROC-AUC | PR-AUC |
|------------------------|---------|--------|
| Logistic Regression    | 0.839   | 0.655  |
| Random Forest          | 0.829   | 0.632  |
| XGBoost                | 0.818   | 0.614  |
| XGBoost (Tuned)        | 0.834   | 0.636  |

**Note:** Logistic Regression achieved the highest ROC-AUC on this split — a reminder that a simpler, more interpretable model can match a tuned ensemble when the underlying relationships aren't heavily nonlinear. XGBoost (Tuned) was still selected as the deployed model for its tunable decision threshold and strong SHAP interpretability support.

## 📈 Performance Metrics
All numbers below are the **deployed model (XGBoost, Tuned)**, evaluated once on the held-out test set at its validation-selected threshold (0.583) — one consistent set of numbers, not mixed across models or threshold policies:

| Metric                 | Score |
|------------------------|-------|
| ROC-AUC                | 0.834 |
| PR-AUC                 | 0.636 |
| Precision (Churn)      | 0.54  |
| Recall (Churn)         | 0.72  |
| F1-Score (Churn)       | 0.62  |

For reference, Logistic Regression scored highest on ROC-AUC/PR-AUC alone (0.839 / 0.655, see table above) but was not the deployed model — see the note above for why.

## 💡 Key Business Insights
1. **Highest Risk Segment**: Month-to-month contracts with high monthly charges (>$70)
2. **Critical Period**: New customers (tenure < 6 months) need immediate retention focus
3. **Service Risk**: Fiber optic internet customers show higher churn rates
4. **Payment Method**: Electronic check payment method correlates with higher churn
5. **Top Churn Drivers**: Tenure, contract type, monthly charges, total charges, internet service

## 🔧 Recommended Retention Strategies
1. Offer annual contract discounts to month-to-month customers
2. Implement 'welcome' retention program for first 6 months
3. Bundle high-speed internet with streaming services
4. Incentivize electronic check customers to switch to auto-pay

## 🛠️ Technologies Used
- Python 3.x
- Pandas, NumPy (Data processing)
- Scikit-learn (Machine Learning)
- XGBoost (Gradient Boosting)
- SHAP (Model Interpretability)
- Matplotlib, Seaborn (Visualization)
- Streamlit (Dashboard deployment)
- Jupyter Notebook (Development)

## 📊 Visualizations
All plots are saved in `outputs/figures/`:
- Distribution plots
- Model comparison ROC curves
- Feature importance charts
- SHAP analysis visualizations
- Precision-Recall threshold optimization (on the validation set)

## 🏁 How to Run
1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Open Jupyter Notebook
4. Run `Customer_Churn_Prediction.ipynb`
5. To view the dashboard locally: `streamlit run dashboard.py`

## 📝 License
MIT License

## 👤 Author
Sanduni Jayasinghe

## 📧 Contact
www.linkedin.com/in/sanduni-jayasinghe-881921385