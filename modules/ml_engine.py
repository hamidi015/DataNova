import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from typing import Dict, Any

class MLEngine:
    """Train and evaluate ML models for forecasting"""
    
    def __init__(self):
        self.lr_model = LinearRegression()
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.dt_model = DecisionTreeRegressor(random_state=42)
        self.X_train = None
        self.y_train = None
        self.is_trained = False

    def train(self, X: pd.DataFrame, y: pd.Series):
        """Train all 3 models"""
        self.X_train = X
        self.y_train = y
        
        self.lr_model.fit(X, y)
        self.rf_model.fit(X, y)
        self.dt_model.fit(X, y)
        self.is_trained = True

    def evaluate(self) -> Dict[str, float]:
        """Get accuracy scores (R² scores)"""
        if not self.is_trained:
            return {"error": "Models not trained yet"}
        
        lr_pred = self.lr_model.predict(self.X_train)
        rf_pred = self.rf_model.predict(self.X_train)
        dt_pred = self.dt_model.predict(self.X_train)

        return {
            "linear_regression": float(r2_score(self.y_train, lr_pred)),
            "random_forest": float(r2_score(self.y_train, rf_pred)),
            "decision_tree": float(r2_score(self.y_train, dt_pred))
        }

    def predict(self, X: pd.DataFrame) -> Dict[str, float]:
        """Make predictions on new data"""
        if not self.is_trained:
            return {"error": "Models not trained yet"}
        
        return {
            "linear_regression": float(self.lr_model.predict(X)[0]),
            "random_forest": float(self.rf_model.predict(X)[0]),
            "decision_tree": float(self.dt_model.predict(X)[0])
        }
    
    def get_best_model(self, accuracy_dict: Dict[str, float]) -> str:
        """Get model with highest accuracy"""
        return max(accuracy_dict, key=accuracy