import types
import pytest

from src.register_model import register_best_model


class DummyRun:
    def __init__(self, run_id, f1):
        self.info = types.SimpleNamespace(run_id=run_id)
        self.data = types.SimpleNamespace(metrics={"f1_score": f1}, tags={"mlflow.runName": "DummyRun"})


class DummyClient:
    def __init__(self, experiment):
        self._experiment = experiment
        self.transition_called = False

    def get_experiment_by_name(self, name):
        return self._experiment

    def search_runs(self, experiment_ids):
        # Return different results based on experiment
        if self._experiment is None:
            return []
        if getattr(self._experiment, "_empty", False):
            return []
        return [DummyRun("run-1", 0.5), DummyRun("run-2", 0.8)]

    def transition_model_version_stage(self, name, version, stage):
        self.transition_called = True


def test_register_no_experiment():
    client = DummyClient(None)
    mv = register_best_model(client=client, experiment_name="NoExp")
    assert mv is None


def test_register_no_runs():
    exp = types.SimpleNamespace(experiment_id=1)
    exp._empty = True
    client = DummyClient(exp)
    mv = register_best_model(client=client, experiment_name="EmptyExp")
    assert mv is None


def test_register_success(monkeypatch):
    exp = types.SimpleNamespace(experiment_id=1)
    client = DummyClient(exp)

    class DummyMV:
        def __init__(self):
            self.version = "1"

    def fake_register_model(model_uri, name):
        assert model_uri.startswith("runs:/")
        assert name == "TelecomChurnBestModel"
        return DummyMV()

    monkeypatch.setattr("mlflow.register_model", fake_register_model)

    mv = register_best_model(client=client)
    assert mv is not None
    assert mv.version == "1"
    assert client.transition_called is True
