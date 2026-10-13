# SHARK

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/Shark) · This repository is linked through its source; GitHub Pages is not enabled.

<details>
<summary>Recent repositories (9)</summary>

- [Oroboros](https://github.com/enuminous/Oroboros) · [README](https://github.com/enuminous/Oroboros/blob/main/README.md) · [Page](https://enuminous.github.io/Oroboros/)
- [P-NP](https://github.com/enuminous/P-NP) · [README](https://github.com/enuminous/P-NP/blob/main/README.md) · [Page](https://enuminous.github.io/P-NP/)
- [Research-Program](https://github.com/enuminous/Research-Program) · [README](https://github.com/enuminous/Research-Program/blob/main/README.md) · [Page](https://enuminous.github.io/Research-Program/)
- [I-Have-Guts](https://github.com/enuminous/I-Have-Guts) · [README](https://github.com/enuminous/I-Have-Guts/blob/main/README.md) · [Page](https://enuminous.github.io/I-Have-Guts/)
- [Wrights-Law](https://github.com/enuminous/Wrights-Law) · [README](https://github.com/enuminous/Wrights-Law/blob/main/README.md) · [Page](https://enuminous.github.io/Wrights-Law/)
- [Aristotle-eNuminous](https://github.com/enuminous/Aristotle-eNuminous) · [README](https://github.com/enuminous/Aristotle-eNuminous/blob/main/README.md) · [Page](https://enuminous.github.io/Aristotle-eNuminous/)
- [Multiverse-Simulator](https://github.com/enuminous/Multiverse-Simulator) · [README](https://github.com/enuminous/Multiverse-Simulator/blob/main/README.md) · [Page](https://enuminous.github.io/Multiverse-Simulator/)
- [accelerando-8192](https://github.com/enuminous/accelerando-8192) · [README](https://github.com/enuminous/accelerando-8192/blob/main/README.md) · [Page source](https://github.com/enuminous/accelerando-8192/blob/main/docs/index.html)
- [Codex-888](https://github.com/enuminous/Codex-888) · [README](https://github.com/enuminous/Codex-888/blob/main/README.md) · [Page](https://enuminous.github.io/Codex-888/)

</details>
<!-- ENUMINOUS-NETWORK:END -->

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
