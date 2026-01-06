import pandas as pd
import os

def feature_engineering(input_path, output_path):
    print(f"Feature engineering from {input_path}...")
    df = pd.read_csv(input_path)

    # Tenure buckets
    if 'tenure' in df.columns:
        df['TenureBucket'] = pd.cut(df['tenure'], bins=[-1, 12, 24, 48, 60, 200], labels=[0,1,2,3,4]).astype(int)

    # Average charges per month (handle tenure==0)
    if 'TotalCharges' in df.columns and 'tenure' in df.columns and 'MonthlyCharges' in df.columns:
        df['AvgChargesPerMonth'] = df.apply(lambda r: r['TotalCharges'] / r['tenure'] if r['tenure'] > 0 else r['MonthlyCharges'], axis=1)

    # Class Balancing (Basic Oversampling for churn class if needed)
    if 'Churn' in df.columns:
        df_churn = df[df['Churn'] == 1]
        df_not_churn = df[df['Churn'] == 0]
        if len(df_churn) < len(df_not_churn):
            df_churn_oversampled = df_churn.sample(len(df_not_churn), replace=True, random_state=42)
            df = pd.concat([df_not_churn, df_churn_oversampled], axis=0)
            print("Class balancing applied: Oversampled churn class.")

    # Drop columns that are no longer needed
    cols_to_drop = ['customerID']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Enhanced data saved to {output_path}")

if __name__ == "__main__":
    feature_engineering("data/interim/cleaned_churn.csv", "data/processed/final_churn.csv")
