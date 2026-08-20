import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

class LogisticModel:
    def __init__(self, random_state=23):
        self.scaler = RobustScaler()
        self.model = LogisticRegression(max_iter=4000, random_state=random_state)
        self.constant_ = None

    def fit(self, X, y):
        y=np.asarray(y,dtype=int)
        if len(np.unique(y))<2:
            self.constant_=float(y.mean()) if len(y) else 0.0
            return self
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X),y)
        return self

    def predict_proba(self, X):
        if self.constant_ is not None:
            return np.full(len(X),self.constant_)
        return self.model.predict_proba(self.scaler.transform(X))[:,1]

class BaseRateModel:
    def fit(self,X,y):
        self.p_=float(np.mean(y))
        return self
    def predict_proba(self,X):
        return np.full(len(X),self.p_,dtype=float)

def boundary_feature(df):
    return pd.DataFrame({
        "boundary_proximity": df["boundary_proximity"].astype(float).fillna(0.0)
        if "boundary_proximity" in df.columns else np.zeros(len(df))
    })

def kinematic_error_feature(df):
    def g(name):
        return df[name].astype(float) if name in df.columns else pd.Series(0.0,index=df.index)
    err=(
        (g("speed_cmd")-g("speed_obs")).abs()
        +(g("heading_cmd")-g("heading_obs")).abs()
        +(g("steering_cmd")-g("steering_obs")).abs()
        +g("lateral_error").abs()
    )/4.0
    return pd.DataFrame({"kinematic_error":err.fillna(0.0)})

def oscillation_feature(df,window=7):
    if "steering_cmd" not in df.columns:
        return pd.DataFrame({"control_oscillation":np.zeros(len(df))})
    s=df["steering_cmd"].astype(float)
    osc=s.diff().abs().rolling(window,min_periods=1).mean().fillna(0.0)
    return pd.DataFrame({"control_oscillation":osc})
