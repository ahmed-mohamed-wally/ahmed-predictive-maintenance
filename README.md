# Ziad — Predictive Maintenance AI Project

An organized version of the predictive-maintenance work built from the machine sensor dataset. The project is intentionally separated into clear stages so that EDA, preprocessing, modeling, and inference are not mixed together.

## Pipeline

`Raw data → EDA → Preprocessing → Model 1 → Model 2 → Integrated inference`

### Model 1 — Machine failure prediction
Inputs: machine type + five sensor readings.
Target: `Machine failure` (0/1).
Model: Random Forest with balanced class weights.
Threshold: selected on validation data with a minimum recall constraint; the current experimental run selected **0.35**.

The final run achieved on the held-out test set: failure precision **0.5096**, recall **0.7794**, F1 **0.6163**, ROC-AUC **0.9594**, PR-AUC **0.7137**.

### Model 2 — Failure type prediction
Failure-only rows are used. Targets are `TWF`, `HDF`, `PWF`, and `OSF` as a multi-label problem because some rows contain multiple failure types. `RNF` occurs only once in the dataset and is not trained as a separate label in this version.

The current held-out test run achieved: micro F1 **0.9091** and macro F1 **0.9222**.

## Folder structure

```text
ziad_predictive_maintenance_organized/
├── data/
│   └── predictive_maintenance.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_failure.ipynb
│   ├── 04_model_failure_types.ipynb
│   └── 05_inference_demo.ipynb
├── models/
├── outputs/
│   ├── eda/
│   ├── model_failure/
│   └── model_failure_types/
├── requirements.txt
└── README.md
```

## Run order

Open the notebooks in this order:

1. `01_eda.ipynb`
2. `02_preprocessing.ipynb`
3. `03_model_failure.ipynb`
4. `04_model_failure_types.ipynb`
5. `05_inference_demo.ipynb`

Run notebooks 03 and 04 before 05 because 05 loads their saved model artifacts.

## Notes

- The test set is not used to choose the Model 1 threshold.
- Direct failure-type flags are not Model 1 inputs; they are Model 2 labels.
- `RNF` is not modeled independently because there is only one positive example.
- Risk/action thresholds in the inference demo are project-level rules, not industrial safety standards.
- The underlying project source describes its smart-factory stream simulation as simulated rather than real factory telemetry.
