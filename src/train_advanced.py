import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import warnings
warnings.filterwarnings('ignore')

def train_with_tuning():
    """Advanced training with hyperparameter tuning and cross-validation"""
    
    print("=" * 80)
    print("ADVANCED TRAINING: Hyperparameter Tuning + Cross-Validation")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv("data/processed/final_churn.csv")
    X = df.drop(columns=['Churn'])
    y = df['Churn']
    
    print(f"\nDataset shape: {X.shape}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Setup MLflow
    mlflow.set_experiment("Telecom_Churn_Prediction_Advanced")
    
    # ==================== Model 1: Logistic Regression with GridSearch ====================
    print("\n" + "=" * 80)
    print("MODEL 1: Logistic Regression - Hyperparameter Tuning")
    print("=" * 80)
    
    lr_params = {
        'C': [0.001, 0.01, 0.1, 1, 10],
        'solver': ['lbfgs', 'liblinear'],
        'max_iter': [500, 1000, 2000]
    }
    
    lr_model = LogisticRegression(random_state=42)
    lr_grid = GridSearchCV(lr_model, lr_params, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    
    print("\nPerforming grid search...")
    lr_grid.fit(X_train, y_train)
    
    print(f"Best parameters: {lr_grid.best_params_}")
    print(f"Best CV F1-Score: {lr_grid.best_score_:.4f}")
    
    # Get best model
    best_lr = lr_grid.best_estimator_
    y_pred_lr = best_lr.predict(X_test)
    
    # Calculate metrics
    lr_metrics = {
        'accuracy': accuracy_score(y_test, y_pred_lr),
        'precision': precision_score(y_test, y_pred_lr),
        'recall': recall_score(y_test, y_pred_lr),
        'f1_score': f1_score(y_test, y_pred_lr)
    }
    
    print("\nTest Set Metrics:")
    for metric, value in lr_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Cross-validation on full dataset
    cv_scores = cross_val_score(best_lr, X, y, cv=5, scoring='f1')
    print(f"5-Fold CV F1-Scores: {[f'{score:.4f}' for score in cv_scores]}")
    print(f"Mean CV F1-Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Log to MLflow
    with mlflow.start_run(run_name="LogisticRegression_Tuned"):
        mlflow.log_params(lr_grid.best_params_)
        mlflow.log_metrics(lr_metrics)
        mlflow.log_metric("cv_mean_f1", cv_scores.mean())
        mlflow.log_metric("cv_std_f1", cv_scores.std())
        mlflow.log_metric("best_cv_f1", lr_grid.best_score_)
        mlflow.sklearn.log_model(best_lr, "model")
        mlflow.log_text(f"Grid Search Results:\n{pd.DataFrame(lr_grid.cv_results_).to_string()}", 
                       "grid_search_results.txt")
    
    # ==================== Model 2: Random Forest with GridSearch ====================
    print("\n" + "=" * 80)
    print("MODEL 2: Random Forest - Hyperparameter Tuning")
    print("=" * 80)
    
    rf_params = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15, None],
        'min_samples_leaf': [1, 2, 5],
        'max_features': ['sqrt', 'log2']
    }
    
    rf_model = RandomForestClassifier(random_state=42, n_jobs=-1)
    rf_grid = GridSearchCV(rf_model, rf_params, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    
    print("\nPerforming grid search...")
    rf_grid.fit(X_train, y_train)
    
    print(f"Best parameters: {rf_grid.best_params_}")
    print(f"Best CV F1-Score: {rf_grid.best_score_:.4f}")
    
    # Get best model
    best_rf = rf_grid.best_estimator_
    y_pred_rf = best_rf.predict(X_test)
    
    # Calculate metrics
    rf_metrics = {
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf),
        'recall': recall_score(y_test, y_pred_rf),
        'f1_score': f1_score(y_test, y_pred_rf)
    }
    
    print("\nTest Set Metrics:")
    for metric, value in rf_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Cross-validation
    cv_scores_rf = cross_val_score(best_rf, X, y, cv=5, scoring='f1')
    print(f"5-Fold CV F1-Scores: {[f'{score:.4f}' for score in cv_scores_rf]}")
    print(f"Mean CV F1-Score: {cv_scores_rf.mean():.4f} (+/- {cv_scores_rf.std():.4f})")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10).to_string(index=False))
    
    # Log to MLflow
    with mlflow.start_run(run_name="RandomForest_Tuned"):
        mlflow.log_params(rf_grid.best_params_)
        mlflow.log_metrics(rf_metrics)
        mlflow.log_metric("cv_mean_f1", cv_scores_rf.mean())
        mlflow.log_metric("cv_std_f1", cv_scores_rf.std())
        mlflow.log_metric("best_cv_f1", rf_grid.best_score_)
        mlflow.sklearn.log_model(best_rf, "model")
        
        # Log feature importance
        feature_importance_text = feature_importance.to_string(index=False)
        mlflow.log_text(feature_importance_text, "feature_importance.txt")
        mlflow.log_text(f"Grid Search Results:\n{pd.DataFrame(rf_grid.cv_results_).to_string()}", 
                       "grid_search_results.txt")
    
    # ==================== Summary ====================
    print("\n" + "=" * 80)
    print("SUMMARY: Model Comparison")
    print("=" * 80)
    
    comparison = pd.DataFrame({
        'Model': ['Logistic Regression', 'Random Forest'],
        'Accuracy': [lr_metrics['accuracy'], rf_metrics['accuracy']],
        'Precision': [lr_metrics['precision'], rf_metrics['precision']],
        'Recall': [lr_metrics['recall'], rf_metrics['recall']],
        'F1-Score': [lr_metrics['f1_score'], rf_metrics['f1_score']],
        'CV Mean F1': [cv_scores.mean(), cv_scores_rf.mean()]
    })
    
    print("\n" + comparison.to_string(index=False))
    
    best_model_name = 'Random Forest' if rf_metrics['f1_score'] > lr_metrics['f1_score'] else 'Logistic Regression'
    best_model = best_rf if rf_metrics['f1_score'] > lr_metrics['f1_score'] else best_lr
    best_metrics = rf_metrics if rf_metrics['f1_score'] > lr_metrics['f1_score'] else lr_metrics
    
    print(f"\n✅ Best Model: {best_model_name}")
    print(f"   F1-Score: {best_metrics['f1_score']:.4f}")
    
    return best_model, best_model_name

if __name__ == "__main__":
    train_with_tuning()
