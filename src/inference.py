from __future__ import annotations

import os
from typing import Any

import joblib
import pandas as pd


# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# Load Model 1
model1 = joblib.load(
    os.path.join(MODEL_DIR, "model_failure_rf.joblib")
)

prep1 = joblib.load(
    os.path.join(MODEL_DIR, "model_failure_preprocessor.joblib")
)

meta1 = joblib.load(
    os.path.join(MODEL_DIR, "model_failure_metadata.joblib")
)


# Load Model 2
model2 = joblib.load(
    os.path.join(MODEL_DIR, "model_failure_types_rf.joblib")
)

prep2 = joblib.load(
    os.path.join(MODEL_DIR, "model_failure_types_preprocessor.joblib")
)

meta2 = joblib.load(
    os.path.join(MODEL_DIR, "model_failure_types_metadata.joblib")
)


def predict_machine(
    machine_type: str,
    air_temp: float,
    process_temp: float,
    rpm: float,
    torque: float,
    tool_wear: float,
) -> dict[str, Any]:
    """
    Predict machine failure, failure types, risk level,
    and maintenance action.
    """

    # -----------------------------
    # Input validation
    # -----------------------------
    if machine_type not in {"L", "M"}:
        raise ValueError("machine_type must be 'L' or 'M'.")

    if air_temp <= 0:
        raise ValueError("air_temp must be positive.")

    if process_temp <= 0:
        raise ValueError("process_temp must be positive.")

    if rpm <= 0:
        raise ValueError("rpm must be positive.")

    if torque < 0:
        raise ValueError("torque cannot be negative.")

    if tool_wear < 0:
        raise ValueError("tool_wear cannot be negative.")

    # -----------------------------
    # Prepare input row
    # -----------------------------
    row = pd.DataFrame(
        [
            {
                "Type": machine_type,
                "Air temperature [K]": air_temp,
                "Process temperature [K]": process_temp,
                "Rotational speed [rpm]": rpm,
                "Torque [Nm]": torque,
                "Tool wear [min]": tool_wear,
            }
        ]
    )

    # -----------------------------
    # Model 1
    # -----------------------------
    x1 = prep1.transform(row)

    failure_probability = float(
        model1.predict_proba(x1)[:, 1][0]
    )

    threshold = float(meta1["threshold"])

    failed = failure_probability >= threshold

    result: dict[str, Any] = {
        "failure_probability": round(failure_probability, 4),
        "failure": bool(failed),
        "failure_types": [],
    }

    # -----------------------------
    # Model 2
    # -----------------------------
    if failed:
        x2 = prep2.transform(row)

        type_pred = model2.predict(x2)[0]

        detected_types = [
            label
            for label, flag in zip(meta2["labels"], type_pred)
            if flag == 1
        ]

        result["failure_types"] = detected_types

        if detected_types:
            result["failure_type_status"] = (
                "Specific failure type(s) identified."
            )
        else:
            result["failure_type_status"] = (
                "Failure detected, but no specific failure "
                "type was identified."
            )
    else:
        result["failure_type_status"] = "No failure predicted."

    # -----------------------------
    # Project-level risk rule
    # -----------------------------
    p = failure_probability

    if p < 0.20:
        risk = "LOW"
        action = "Continue monitoring"

    elif p < 0.35:
        risk = "MEDIUM"
        action = "Inspect during planned maintenance"

    elif p < 0.60:
        risk = "HIGH"
        action = "Schedule inspection soon"

    else:
        risk = "CRITICAL"
        action = "Prioritize immediate inspection"

    result["risk"] = risk
    result["maintenance_action"] = action

    return result


if __name__ == "__main__":
    demo_result = predict_machine(
        machine_type="L",
        air_temp=302.0,
        process_temp=311.0,
        rpm=1400,
        torque=55.0,
        tool_wear=180,
    )

    print(demo_result)