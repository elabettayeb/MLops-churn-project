# GitHub Actions & CI/CD for MLOps-churn-project ✅

Ce document décrit comment configurer GitHub Actions pour exécuter la pipeline DVC/MLflow à chaque push, comment vérifier les exécutions, et comment tracer et comparer les runs MLflow.

---

## Objectifs du workflow
- S'exécuter sur chaque push
- Installer Python et dépendances
- Exécuter `dvc repro` (étapes: nettoyage, feature engineering, entraînement, enregistrement)
- Exécuter les tests (`pytest`)
- Récupérer et archiver les résultats MLflow (`mlruns`) comme artefacts

---

## Fichier ajouté
- `.github/workflows/ml-pipeline.yml`
  - Installe Python 3.10
  - Installe `requirements.txt` et `dvc`
  - Tente `dvc pull` puis `dvc repro`
  - Exécute `pytest`
  - Exporte un résumé des métriques MLflow (`mlflow_metrics_summary.json`)
  - Upload `mlruns` et `dvc-cache.tgz` comme artefacts

---

## Configuration recommandée (sur GitHub)
1. Allez dans votre repo GitHub -> Settings -> Secrets and variables -> Actions -> New repository secret
2. Ajoutez au moins les secrets nécessaires si vous utilisez un remote DVC stocké sur S3/GCS:
   - `DVC_REMOTE_URL` (ex: `s3://my-dvc-bucket`) — facultatif si vos données sont déjà accessibles
   - `AWS_ACCESS_KEY_ID` et `AWS_SECRET_ACCESS_KEY` (si votre backend est S3)
   - `MLFLOW_TRACKING_URI` (optionnel) si vous avez un serveur MLflow centralisé (ex: `http://my-mlflow-server:5000`)

Note: si vous utilisez un serveur MLflow distant avec Model Registry, mettez aussi les variables d'auth correspondantes.

---

## Vérification du pipeline (et étapes de test)
1. Faites une petite modification du code ou du dataset (ex: changez un hyperparamètre dans `src/train.py` ou modifiez une ligne dans `data/raw/`), commit & push.
2. Ouvrez l'onglet `Actions` dans GitHub; sélectionnez le workflow "MLOps Pipeline" et surveillez l'exécution.
3. À la fin, téléchargez l'artefact `mlflow-runs` (ou `mlflow_metrics_summary.json`) depuis la page de l'exécution pour inspecter les runs et les métriques.

---

## Inspecter et comparer les runs MLflow localement
1. Téléchargez l'artefact `mlflow-runs` depuis la page Actions et extrayez-le dans un dossier `mlruns/`.
2. Lancez l'UI MLflow localement:

```bash
pip install mlflow
mlflow ui --backend-store-uri mlruns
# Ouvrir http://127.0.0.1:5000
```

3. Dans l'UI, vous pouvez visualiser tous les runs et comparer métriques (accuracy, precision, recall, f1_score).

---

## Notes sur l'enregistrement du modèle (Model Registry)
- `src/register_model.py` tente d'enregistrer le meilleur modèle dans le Model Registry MLflow.
- Pour que l'enregistrement fonctionne en CI, `MLFLOW_TRACKING_URI` doit pointer vers un serveur MLflow qui supporte la Model Registry.
- Si vous utilisez uniquement le dossier `mlruns` local, l'enregistrement peut échouer (Model Registry non disponible) — le script gère ces erreurs en affichant des messages.

---

## Conseils pratiques
- Pour garder l'historique des données et modèles au même endroit, mettez en place un remote DVC (S3/GCS/SSH) et configurez les secrets GitHub en conséquence.
- Si vous voulez que les artefacts MLflow soient consultables automatiquement, configurez un serveur MLflow central et mettez `MLFLOW_TRACKING_URI` comme secret.

---

## Exemple rapide de test local (simuler ce que fait l'Action)

```bash
# depuis la racine du repo
python -m pip install -r requirements.txt
pip install "dvc[s3]" mlflow
# récupérer data si votre remote est configuré
dvc pull
# reproduire le pipeline
dvc repro
# lancer UI mlflow
mlflow ui --backend-store-uri mlruns
```

---

Si vous voulez, je peux :
- ajuster le workflow pour supporter un remote DVC précis (S3/GCS/SSH),
- configurer la sauvegarde des métriques dans un fichier CSV pour un suivi plus simple, ou
- ajouter un job GitHub Actions qui publie un résumé des métriques en tant que check/commentaire PR.

Dites-moi quelle option vous préférez et je l'implémente. ✨