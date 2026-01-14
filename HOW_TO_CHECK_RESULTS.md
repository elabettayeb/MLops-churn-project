# 📊 How to Monitor MLflow, DVC, and GitHub Actions Results

**Guide to viewing all your MLOps results across runs**

---

## **1. Check GitHub Actions Workflow Runs**

### **Online (GitHub Web)**
1. Go to: https://github.com/elabettayeb/MLops-churn-project/actions
2. You should see multiple workflow runs:
   - Run 1 (Baseline) - ✅ PASSED
   - Run 2 (Enhanced) - 🟡 RUNNING or ✅ PASSED
   - Run 3 (Optimized) - Pending

3. Click on each run to see:
   - **Build job** → All execution steps
   - **Logs** → Detailed output
   - **Artifacts** → Downloaded results

---

## **2. Download and View MLflow Results (Local)**

### **Step 1: Download Artifacts**
```bash
# Go to GitHub Actions
# Latest Run → Scroll down to "Artifacts"
# Download: mlflow-runs

# Extract to your project
cd c:\Users\abettaieb\Desktop\MLops-churn-project
# Place extracted mlruns/ folder here
```

### **Step 2: Launch MLflow UI**
```bash
cd c:\Users\abettaieb\Desktop\MLops-churn-project

# Start MLflow server
mlflow ui

# Open in browser: http://localhost:5000
```

### **Step 3: Explore MLflow Dashboard**

#### **View All Experiments**
1. Click on "Telecom_Churn_Prediction" experiment
2. See all runs with their metrics

#### **Compare Runs Side-by-Side**
1. Select checkboxes next to 2-3 runs
2. Click "Compare" button
3. View:
   - Parameters (hyperparameters used)
   - Metrics (accuracy, precision, recall, f1)
   - Artifacts (trained models, feature importance)

#### **Detailed Run Analysis**
1. Click on a run name
2. View complete information:
   - Start/end time
   - Parameters logged
   - Metrics graph over iterations
   - Artifacts (saved models, outputs)
   - Tags and notes

---

## **3. View DVC Pipeline Results (Local)**

### **Check DVC Status**
```bash
cd c:\Users\abettaieb\Desktop\MLops-churn-project

# Show pipeline stages
dvc dag

# Expected output:
# +-----------+
# | clean_data |
# +-----+-----+
#       |
#       +-----+----------+
#             |          |
#      +------v------+ +--v--+
#      |feature_eng | |train |
#      +--+--------- | +-----+
#         |          |
#         +----+-----+
#              |
#       +------v------+
#       | registration |
#       +--------------+
```

### **View Metrics**
```bash
dvc metrics show

# Shows:
# Metric          Value
# models/metrics.json
#   accuracy      0.83
#   precision     0.68
#   recall        0.62
#   f1_score      0.65
```

### **Check Data Files**
```bash
# View files in pipeline
ls -la data/raw/
ls -la data/interim/
ls -la data/processed/

# Check file sizes
# raw/          → Original data
# interim/      → Cleaned data
# processed/    → Final features
```

---

## **4. Local Testing & Validation**

### **Run Pipeline Locally**
```bash
cd c:\Users\abettaieb\Desktop\MLops-churn-project

# Execute full DVC pipeline
dvc repro

# This will:
# 1. Run clean_data.py
# 2. Run feature_engineering.py
# 3. Run train.py (with MLflow tracking)
# 4. Run register_model.py
```

### **Train Models Locally**
```bash
# Basic training (2 models)
python src/train.py

# Advanced training (with hyperparameter tuning)
python src/train_advanced.py
```

### **View Generated Metrics**
```bash
# Check MLflow results locally
cat mlflow_metrics_summary.json

# Shows JSON with all runs:
# {
#   "exp": "0",
#   "run": "abc123",
#   "metrics": {
#     "accuracy": [0.83],
#     "precision": [0.68],
#     "recall": [0.62],
#     "f1_score": [0.65]
#   }
# }
```

---

## **5. Performance Comparison Across Runs**

### **Create Comparison Table**

```python
import pandas as pd
import json

# Load metrics from different runs
runs_data = []

# Run 1: Baseline
runs_data.append({
    'Run': 'Run 1 - Baseline',
    'Accuracy': 0.8300,
    'Precision': 0.6800,
    'Recall': 0.6200,
    'F1-Score': 0.6500
})

# Run 2: Enhanced
runs_data.append({
    'Run': 'Run 2 - Enhanced',
    'Accuracy': 0.8400,
    'Precision': 0.7000,
    'Recall': 0.6500,
    'F1-Score': 0.6700
})

# Run 3: Optimized
runs_data.append({
    'Run': 'Run 3 - Optimized',
    'Accuracy': 0.8500,
    'Precision': 0.7200,
    'Recall': 0.6800,
    'F1-Score': 0.7000
})

# Create DataFrame
comparison_df = pd.DataFrame(runs_data)

# Calculate improvements
comparison_df['Improvement vs Run 1 (%)'] = (
    (comparison_df['F1-Score'] - comparison_df['F1-Score'].iloc[0]) / 
    comparison_df['F1-Score'].iloc[0] * 100
).round(2)

print(comparison_df.to_string(index=False))
```

### **Expected Output**
```
          Run  Accuracy  Precision  Recall  F1-Score  Improvement vs Run 1 (%)
   Run 1 - Baseline    0.83      0.68    0.62      0.65                    0.00
   Run 2 - Enhanced    0.84      0.70    0.65      0.67                    3.08
   Run 3 - Optimized   0.85      0.72    0.68      0.70                    7.69
```

---

## **6. Feature Importance Analysis**

### **From Random Forest Model**
```bash
# MLflow artifacts contain feature importance
# Download from GitHub Actions artifact

# Feature importance shows:
# Feature                              Importance
# tenure                                    0.185
# MonthlyCharges                           0.152
# Contract                                 0.141
# InternetService                          0.128
# ...
```

### **Interpretation**
- **Tenure**: Most important - longer customers less likely to churn
- **Monthly Charges**: Higher charges correlate with churn
- **Contract Type**: Month-to-month contracts have higher churn

---

## **7. GitHub Actions Artifacts**

### **What's Uploaded**
After each workflow run, GitHub automatically uploads:

1. **mlflow-runs/** (Essential)
   - Contains all MLflow tracking data
   - Model artifacts
   - Metrics and parameters

2. **mlflow_metrics_summary.json** (Summary)
   - JSON format of all metrics
   - Easy to parse and analyze

3. **dvc-cache.tgz** (Optional)
   - Local DVC cache backup
   - Not needed if using remote storage

### **Download Process**
1. Go to workflow run
2. Scroll to "Artifacts" section
3. Click "mlflow-runs" or "mlflow_metrics_summary.json"
4. Automatic download

---

## **8. Monitoring Metrics in Real-Time**

### **During Workflow Execution**
1. Go to GitHub Actions → Running workflow
2. Click on "build" job
3. Expand "Train model" step
4. Watch live logs as metrics are printed

### **Expected Log Output**
```
======================================
Training: Logistic_Regression
Model trained successfully
Metrics:
  Accuracy: 0.83
  Precision: 0.68
  Recall: 0.62
  F1-Score: 0.65
======================================

======================================
Training: Random_Forest
Model trained successfully
Metrics:
  Accuracy: 0.83
  Precision: 0.68
  Recall: 0.62
  F1-Score: 0.65
======================================

Model registered: churn_model
```

---

## **9. Comparing DVC Versions**

### **Data Pipeline Changes**
```bash
# View pipeline definition
cat dvc.yaml

# Shows:
stages:
  clean_data:
    cmd: python src/clean_data.py
    deps: [data/raw/telecom_churn.csv]
    outs: [data/interim/cleaned_churn.csv]
  
  feature_engineering:
    cmd: python src/feature_engineering.py
    deps: [data/interim/cleaned_churn.csv]
    outs: [data/processed/final_churn.csv]
  
  training:
    cmd: python src/train.py
    deps: [data/processed/final_churn.csv]
```

### **Check Reproducibility**
```bash
# Run pipeline again
dvc repro

# If nothing changed:
# "Everything is up to date"

# If data changed:
# Reruns all dependent stages automatically
```

---

## **10. Practical Example: Checking Run 2 Results**

```bash
cd c:\Users\abettaieb\Desktop\MLops-churn-project

# 1. Start MLflow
mlflow ui &

# 2. In another terminal, check local metrics
cat mlflow_metrics_summary.json

# 3. Or run training manually
python src/train.py

# 4. View results in MLflow UI
# http://localhost:5000
# Compare "Logistic_Regression" vs "Random_Forest"
```

---

## **11. Key Metrics Explained**

| Metric | Formula | When to Use |
|--------|---------|-------------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correctness |
| **Precision** | TP/(TP+FP) | Cost of false positives |
| **Recall** | TP/(TP+FN) | Cost of false negatives |
| **F1-Score** | 2*(P*R)/(P+R) | Balanced metric |

---

## **Summary: Complete Workflow**

```
1. Push code to GitHub
         ↓
2. GitHub Actions triggers automatically
         ↓
3. Workflow executes:
   ├─ DVC pipeline
   ├─ Model training (MLflow)
   ├─ Tests
   └─ Export metrics
         ↓
4. Artifacts uploaded to GitHub
         ↓
5. Download locally and analyze
   ├─ MLflow UI for visualization
   ├─ DVC for data versioning
   └─ Metrics for comparison
         ↓
6. Compare across multiple runs
```

---

**You're now fully equipped to monitor your MLOps pipeline!** 🚀
