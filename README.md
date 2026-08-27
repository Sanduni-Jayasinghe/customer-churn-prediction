# Customer Churn Prediction

## 📊 Project Overview
This project predicts which telecom customers are likely to churn using machine learning classification models. The analysis identifies key drivers of churn and provides actionable business recommendations.

## 🎯 Key Features
- **Exploratory Data Analysis** - Understanding churn patterns and customer behavior
- **Feature Engineering** - Created 4 new features for better predictions
- **Multiple Models** - Logistic Regression, Random Forest, XGBoost
- **Hyperparameter Tuning** - GridSearchCV optimization for XGBoost
- **Threshold Optimization** - Find optimal probability threshold for business decisions
- **SHAP Analysis** - Deep model interpretability
- **Business Dashboard** - Actionable recommendations for retention strategies

## 📁 Project Structure
customer-churn-prediction/
├── Customer_Churn_Prediction.ipynb # Main Jupyter notebook
├── data/
│ └── telco_churn.csv # Dataset
├── outputs/
│ ├── figures/ # All visualizations (13 plots)
│ ├── best_xgb_model.pkl # Trained model
│ ├── classification_report.txt # Model metrics
│ ├── model_comparison.csv # Performance comparison
│ ├── feature_importance_rf.csv # RF feature importance
│ ├── feature_importance_xgb.csv # XGB feature importance
│ └── business_recommendations.txt # Business insights
└── README.md # This file


## 🚀 Models Compared
|      Model          | ROC-AUC  | PR-AUC  |
|---------------------|----------|---------|
| Logistic Regression | ~0.839   | ~0.655  |
| Random Forest       | ~0.829   | ~0.632  |
| XGBoost (Tuned)     | ~0.834   | ~0.636  |

## 📈 Performance Metrics
|          Metric           | Best Model          | Score |
|---------------------------|---------------------|-------|
| **ROC-AUC**               | Logistic Regression | 0.839 |
| **PR-AUC**                | Logistic Regression | 0.655 |
| **F1-Score (Churn)**      | Tuned XGBoost       | 0.616 |
| **Recall (Churn)**        | Random Forest       | 0.77  |
| **Precision (Churn)**     | Tuned XGBoost       | 0.54  |
| **Optimal Threshold**     | Validation Set      | 0.583 |

## 💡 Key Business Insights
1. **Highest Risk Segment**: Month-to-month contracts with high monthly charges (>$70)
2. **Critical Period**: New customers (tenure < 6 months) need immediate retention focus
3. **Service Risk**: Fiber optic internet customers show higher churn rates
4. **Payment Method**: Electronic check payment method correlates with higher churn
5. **Top Churn Drivers**: Tenure, Contract Type, Monthly Charges, Total Charges, Internet Service

## 🔧 Recommended Retention Strategies
1. Offer annual contract discounts to month-to-month customers
2. Implement 'welcome' retention program for first 6 months
3. Bundle high-speed internet with streaming services
4. Incentivize electronic check customers to switch to auto-pay

## 📈 Performance Metrics
- **Best Model by ROC-AUC**: Logistic Regression (0.839)
- **Best for Recall**: Random Forest (0.77 recall)
- **Precision (Churn)**: 0.54
- **Recall (Churn)**: 0.72 (Tuned XGBoost)
- **F1-Score (Churn)**: 0.62 (Tuned XGBoost)

## 🛠️ Technologies Used
- Python 3.x
- Pandas, NumPy (Data processing)
- Scikit-learn (Machine Learning)
- XGBoost (Gradient Boosting)
- SHAP (Model Interpretability)
- Matplotlib, Seaborn (Visualization)
- Streamlit (Web Dashboard)
- Jupyter Notebook (Development)

## 📊 Visualizations
All plots are saved in `outputs/figures/`:
- Distribution plots
- Model comparison ROC curves
- Feature importance charts
- SHAP analysis visualizations
- Precision-Recall threshold optimization

## 🏁 How to Run
1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Open Jupyter Notebook
4. Run `Customer_Churn_Prediction.ipynb`

## 📝 License
MIT License

## 👤 Author
Sanduni Jayasinghe

## 📧 Contact
www.linkedin.com/in/sanduni-jayasinghe-881921385
