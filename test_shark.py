import pandas as pd
from features import build_shark_features
from shark import SHARKExperiment

FEATURES=[
    "speed_cmd",
    "speed_obs",
    "heading_cmd",
    "heading_obs",
    "steering_cmd",
    "steering_obs",
    "lateral_error",
    "boundary_proximity",
    "obstacle_pressure",
    "recovery_attempt",
]

def test_features():
    df=pd.read_csv("example_data.csv")
    sf=build_shark_features(df,FEATURES)
    assert len(sf)==len(df)
    assert "shark_hazard_score" in sf.columns
    assert sf["shark_hazard_score"].between(0,1).all()

def test_experiment_runs():
    df=pd.read_csv("example_data.csv")
    exp=SHARKExperiment(
        time_column="time",
        target_column="hazard",
        feature_columns=FEATURES,
    )
    out=exp.run(df)
    assert "results" in out
    assert "shark" in out["results"]
    assert "raw_state" in out["results"]
