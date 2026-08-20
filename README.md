# SHARK

**Systemic Hazard Assessment through Recursive Kinematics**

SHARK is an EFMW-derived framework for autonomous systems, robotics, and motion/control reliability.

Its narrow question is:

> Can changing relationships among motion, control, environment, and recovery state reveal impending hazard before a conventional safety threshold is crossed?

## Intended uses

- autonomous vehicles
- mobile robots
- drones
- industrial robots
- navigation systems
- motion planners
- control systems
- fleet autonomy
- embodied AI

## Core signal path

```text
motion state
→ control command
→ observed response
→ environment state
→ controller-response mismatch
→ kinematic contradiction
→ recovery behavior
→ recursive hazard persistence
→ SHARK risk score
```

## Flat-stack repository

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
shark.py
features.py
baselines.py
metrics.py
freeze.py
hazard_schema.json
example_config.yaml
example_data.csv
example_run.py
test_shark.py
MANIFEST.sha256
```

## Scientific hypothesis

> In autonomous systems, hazard may emerge first as deteriorating agreement among commanded motion, realized motion, environmental constraints, and recovery behavior.

SHARK does not assume this is true.

## Example signals

- speed error
- heading error
- lateral error
- acceleration mismatch
- steering mismatch
- control oscillation
- recovery attempts
- boundary proximity
- obstacle pressure
- route deviation
- kinematic contradiction
- recursive hazard persistence

## Baselines

Included:

- raw-state logistic model
- boundary-proximity baseline
- kinematic-error baseline
- control-oscillation baseline
- base-rate predictor

## Primary endpoint

> Does SHARK improve out-of-sample prediction of a future hazard event over a matched raw-state model?

Primary metric:

- Brier score

Secondary metrics:

- log loss
- ROC-AUC
- average precision
- performance by boundary-proximity regime

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python example_run.py
```

## Tests

```bash
pytest -q
```

## Minimal use

```python
import pandas as pd
from shark import SHARKExperiment

df = pd.read_csv("example_data.csv")

exp = SHARKExperiment(
    time_column="time",
    target_column="hazard",
    feature_columns=[
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
    ],
    horizons=(3,7,23),
)

print(exp.run(df))
```

## Freeze discipline

Freeze before prospective use:

- feature semantics
- sampling interval
- hazard definition
- controller-response relation
- recovery definition
- horizons
- recursion rule
- baselines
- split
- metrics
- exclusions
- seeds

Then run:

```bash
python freeze.py
```

## Negative results

If raw kinematics or simple boundary metrics match or beat SHARK, then the explicit recursive-kinematic representation has not demonstrated incremental value.

## Status

Research software. Experimental. Not validated for live safety-critical control.
