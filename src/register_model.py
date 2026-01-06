import mlflow
from mlflow.tracking import MlflowClient


def register_best_model(client: MlflowClient = None, experiment_name: str = "Telecom_Churn_Prediction", registered_model_name: str = "TelecomChurnBestModel"):
    """Register the best model by F1 score and promote it to Production.

    Parameters:
        client (MlflowClient): If provided, use this client (helps testing); otherwise a new one is created.
        experiment_name (str): Name of the MLflow experiment to query.
        registered_model_name (str): Name to use in the MLflow Model Registry.
    """
    if client is None:
        client = MlflowClient()

    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"No experiment found with name '{experiment_name}'. Aborting registration.")
        return None

    # Get all runs in the experiment
    runs = client.search_runs(experiment_ids=[experiment.experiment_id])
    if not runs:
        print(f"No runs found in experiment '{experiment_name}'. Nothing to register.")
        return None

    # Sort runs by F1-score descending (missing scores treated as 0)
    best_run = sorted(runs, key=lambda x: x.data.metrics.get("f1_score", 0), reverse=True)[0]

    run_id = best_run.info.run_id
    f1_score = best_run.data.metrics.get("f1_score", 0)
    model_name = best_run.data.tags.get("mlflow.runName", "BestModel")

    print(f"Best run ID: {run_id} with F1-score: {f1_score:.4f} ({model_name})")

    # Register the model
    model_uri = f"runs:/{run_id}/model"
    try:
        mv = mlflow.register_model(model_uri, registered_model_name)
    except Exception as e:
        print(f"Failed to register model: {e}")
        return None

    try:
        # Promote to Production
        client.transition_model_version_stage(
            name=registered_model_name,
            version=mv.version,
            stage="Production"
        )
    except Exception as e:
        print(f"Failed to transition model stage: {e}")
        # Don't re-raise; registration succeeded but stage promotion failed

    print(f"Model version {mv.version} registered (attempted promotion to Production).")
    return mv


if __name__ == "__main__":
    register_best_model()
