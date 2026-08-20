import json
import pandas as pd
from shark import SHARKExperiment

df=pd.read_csv("example_data.csv")

features=[
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

exp=SHARKExperiment(
    time_column="time",
    target_column="hazard",
    feature_columns=features,
    horizons=(3,7,23),
    random_state=23,
)

result=exp.run(df)
print(json.dumps(result,indent=2))
