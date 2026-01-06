import os
import pandas as pd

from src.clean_data import clean_data
from src.feature_engineering import feature_engineering


def test_smoke_pipeline(tmp_path):
    # Create a small sample input CSV
    sample = pd.DataFrame({
        "customerID": ["0001", "0002"],
        "tenure": [1, 24],
        "MonthlyCharges": [29.85, 56.95],
        "TotalCharges": [29.85, 1370.0],
        "Churn": ["No", "Yes"],
        "gender": ["Female", "Male"],
    })

    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    input_path = raw_dir / "small_telecom.csv"
    sample.to_csv(input_path, index=False)

    interim = tmp_path / "data" / "interim" / "cleaned_small.csv"
    processed = tmp_path / "data" / "processed" / "final_small.csv"

    # Run clean_data and feature_engineering
    clean_data(str(input_path), str(interim))
    assert os.path.exists(str(interim))

    feature_engineering(str(interim), str(processed))
    assert os.path.exists(str(processed))

    df_proc = pd.read_csv(str(processed))
    # Check engineered columns
    assert "TenureBucket" in df_proc.columns
    assert "AvgChargesPerMonth" in df_proc.columns
