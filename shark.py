from dataclasses import dataclass
import pandas as pd

from features import build_shark_features
from baselines import LogisticModel, BaseRateModel, boundary_feature, kinematic_error_feature, oscillation_feature
from metrics import binary_metrics, stratify

@dataclass
class SHARKExperiment:
    time_column: str
    target_column: str
    feature_columns: list
    horizons: tuple = (3,7,23)
    train_fraction: float = 0.65
    random_state: int = 23

    def run(self, df):
        df=df.sort_values(self.time_column).reset_index(drop=True).copy()
        cut=max(20,int(len(df)*self.train_fraction))
        y=df[self.target_column].astype(int).to_numpy()

        sf=build_shark_features(df,self.feature_columns,self.horizons)
        raw=df[self.feature_columns].astype(float).ffill().fillna(0.0)
        full=pd.concat([raw,sf],axis=1).fillna(0.0)

        boundary=boundary_feature(df)
        kinematic=kinematic_error_feature(df)
        oscillation=oscillation_feature(df)

        models={
            "shark":(LogisticModel(self.random_state),full),
            "raw_state":(LogisticModel(self.random_state),raw),
            "boundary_only":(LogisticModel(self.random_state),boundary),
            "kinematic_error_only":(LogisticModel(self.random_state),kinematic),
            "oscillation_only":(LogisticModel(self.random_state),oscillation),
            "base_rate":(BaseRateModel(),raw),
        }

        results={}
        for name,(model,X) in models.items():
            model.fit(X.iloc[:cut],y[:cut])
            p=model.predict_proba(X.iloc[cut:])
            results[name]={
                "overall":binary_metrics(y[cut:],p),
                "by_boundary_pressure":stratify(
                    y[cut:],p,sf["boundary_pressure"].to_numpy()[cut:]
                )
            }

        return {
            "n_total":len(df),
            "train_n":cut,
            "test_n":len(df)-cut,
            "results":results,
            "primary_delta_brier_raw_minus_shark":(
                results["raw_state"]["overall"]["brier"]
                - results["shark"]["overall"]["brier"]
            ),
            "interpretation":(
                "Positive delta favors SHARK over the matched raw-state model. "
                "Inspect whether any gain concentrates near environmental or control boundaries."
            )
        }
