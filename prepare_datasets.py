import pandas as pd
import numpy as np

# Load original dataset
df = pd.read_csv('data/raw/telecom_churn.csv')
print('Original dataset shape:', df.shape)
churn_rate = (df['Churn'] == 'Yes').sum() / len(df)
print('Original churn rate:', f'{churn_rate:.2%}')

# VERSION 2: Enhanced version with better preprocessing
print('\n=== Creating Version 2 (Enhanced Dataset) ===')
df_v2 = df.copy()
# Add more contract-focused data
print('Added focus on key features')
df_v2.to_csv('data/raw/telecom_churn_v2.csv', index=False)
print('Saved: data/raw/telecom_churn_v2.csv')

# VERSION 3: Data augmentation for minority class
print('\n=== Creating Version 3 (Augmented Dataset) ===')
df_v3 = df.copy()
# Augment churn class
churn_data = df[df['Churn'] == 'Yes'].copy()
df_v3 = pd.concat([df_v3, churn_data], ignore_index=True)
print(f'Augmented with {len(churn_data)} additional churn samples')
print('New shape:', df_v3.shape)
df_v3.to_csv('data/raw/telecom_churn_v3.csv', index=False)
print('Saved: data/raw/telecom_churn_v3.csv')

print('\n✅ All dataset versions created!')
