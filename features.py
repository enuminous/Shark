import numpy as np
import pandas as pd

EPS = 1e-8

def build_shark_features(df, feature_columns, horizons=(3,7,23)):
    x = df[feature_columns].astype(float).ffill().fillna(0.0)
    out = pd.DataFrame(index=df.index)

    def get(name):
        return x[name] if name in x.columns else pd.Series(0.0, index=x.index)

    # Command-response mismatches.
    out["speed_error"] = (get("speed_cmd") - get("speed_obs")).abs()
    out["heading_error"] = (get("heading_cmd") - get("heading_obs")).abs()
    out["steering_error"] = (get("steering_cmd") - get("steering_obs")).abs()
    out["lateral_error_state"] = get("lateral_error").abs()

    # Dynamic mismatch.
    out["speed_error_velocity"] = out["speed_error"].diff().fillna(0.0)
    out["heading_error_velocity"] = out["heading_error"].diff().fillna(0.0)
    out["steering_error_velocity"] = out["steering_error"].diff().fillna(0.0)

    # Control oscillation.
    steer_delta = get("steering_cmd").diff().fillna(0.0)
    out["control_oscillation"] = steer_delta.abs().rolling(7, min_periods=1).mean()
    out["control_reversal_rate"] = (
        np.sign(steer_delta) != np.sign(steer_delta.shift(1))
    ).astype(float).rolling(7, min_periods=1).mean().fillna(0.0)

    # Environmental pressure.
    out["boundary_pressure"] = get("boundary_proximity").clip(0,1)
    out["obstacle_pressure"] = get("obstacle_pressure").clip(0,1)
    out["recovery_pressure"] = get("recovery_attempt").clip(lower=0).rank(pct=True)

    # Contradiction: controller demand is rising while realized motion agreement worsens.
    mismatch = (
        out["speed_error"].rank(pct=True)
        + out["heading_error"].rank(pct=True)
        + out["steering_error"].rank(pct=True)
        + out["lateral_error_state"].rank(pct=True)
    ) / 4.0

    environment = (
        out["boundary_pressure"].rank(pct=True)
        + out["obstacle_pressure"].rank(pct=True)
    ) / 2.0

    out["kinematic_contradiction"] = (mismatch + environment) / 2.0
    out["hazard_velocity"] = out["kinematic_contradiction"].diff().fillna(0.0)
    out["hazard_acceleration"] = out["hazard_velocity"].diff().fillna(0.0)

    for h in horizons:
        out[f"contradiction_mean_{h}"] = out["kinematic_contradiction"].rolling(h, min_periods=1).mean()
        out[f"oscillation_mean_{h}"] = out["control_oscillation"].rolling(h, min_periods=1).mean()
        out[f"boundary_mean_{h}"] = out["boundary_pressure"].rolling(h, min_periods=1).mean()
        out[f"recovery_mean_{h}"] = out["recovery_pressure"].rolling(h, min_periods=1).mean()

    # Recursive hazard persistence.
    base = pd.concat([
        out["kinematic_contradiction"],
        out["control_oscillation"],
        out["boundary_pressure"],
        out["obstacle_pressure"],
        out["recovery_pressure"],
    ], axis=1).fillna(0.0).to_numpy()

    rec = np.zeros(len(out), dtype=float)
    for t in range(len(out)):
        prev = rec[t-1] if t > 0 else 0.0
        current = float(np.mean(base[t]))
        s = current
        for _ in range(3):
            s = 0.5*s + 0.5*np.tanh(s + prev)
        rec[t] = s
    out["recursive_hazard"] = rec

    components = [
        out["kinematic_contradiction"],
        out["control_oscillation"],
        out["control_reversal_rate"],
        out["boundary_pressure"],
        out["obstacle_pressure"],
        out["recovery_pressure"],
        out["hazard_velocity"].clip(lower=0),
        out["hazard_acceleration"].clip(lower=0),
        out["recursive_hazard"],
    ]
    for h in horizons:
        components.extend([
            out[f"contradiction_mean_{h}"],
            out[f"oscillation_mean_{h}"],
            out[f"boundary_mean_{h}"],
            out[f"recovery_mean_{h}"],
        ])

    ranked = pd.concat(components, axis=1).rank(pct=True)
    out["shark_hazard_score"] = ranked.mean(axis=1).fillna(0.0)

    return out.replace([np.inf,-np.inf], np.nan).fillna(0.0)
