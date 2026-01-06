import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

def clean_data(input_path, output_path):
    print(f"Cleaning data from {input_path}...")
    df = pd.read_csv(input_path)

    # Drop identifier if present
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    # Convert TotalCharges to numeric and fill missing values
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

    # Fill numeric nulls with median
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill categorical nulls with mode
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in cat_cols:
        if col == 'Churn':
            continue
        df[col] = df[col].fillna(df[col].mode()[0])

    # Encode Churn to 0/1 if present
    if 'Churn' in df.columns:
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0}).fillna(df['Churn'])

    # Convert binary Yes/No object columns to 0/1
    binary_map = {'Yes': 1, 'No': 0}
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() == 2:
            df[col] = df[col].map(binary_map)

    # Label encode remaining categorical columns
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    clean_data("data/raw/telecom_churn.csv", "data/interim/cleaned_churn.csv")
