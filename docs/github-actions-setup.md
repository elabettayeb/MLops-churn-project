# Guide de Configuration GitHub et GitHub Actions pour MLOps Pipeline

## Partie 1 : Préparer le dépôt GitHub

### Étape 1.1 : Initialiser le dépôt local (si ce n'est pas déjà fait)

```bash
cd c:\Users\abettaieb\Desktop\MLops-churn-project
git init
git config user.email "votre.email@example.com"
git config user.name "Votre Nom"
```

### Étape 1.2 : Créer un dépôt GitHub

1. Allez sur [GitHub](https://github.com)
2. Connectez-vous à votre compte
3. Cliquez sur "+" en haut à droite → "New repository"
4. Donnez un nom au dépôt (ex: `MLops-churn-project`)
5. Choisissez Public ou Private
6. **NE sélectionnez PAS** "Initialize this repository with README"
7. Cliquez sur "Create repository"

### Étape 1.3 : Ajouter le dépôt distant et pousser le code

```bash
# Ajouter l'URL du dépôt distant (remplacez USERNAME et REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Renommer la branche principale si nécessaire
git branch -M main

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Initial commit: MLOps pipeline with DVC and MLflow"

# Pousser vers GitHub
git push -u origin main
```

### Étape 1.4 : Vérifier que tous les fichiers sont présents

Le dépôt GitHub doit contenir :
- ✅ `src/` - Scripts Python (clean_data.py, feature_engineering.py, train.py, register_model.py)
- ✅ `data/` - Données (raw, interim, processed)
- ✅ `tests/` - Tests unitaires
- ✅ `dvc.yaml` - Configuration DVC pipeline
- ✅ `.dvc/` - Configuration DVC (dossier caché)
- ✅ `.github/workflows/ml-pipeline.yml` - Workflow CI/CD
- ✅ `requirements.txt` - Dépendances Python
- ✅ `README.md` - Documentation
- ✅ Les fichiers `.dvc` pour tracking des données (*.dvc)

**IMPORTANT** : Poussez également les fichiers `.dvc` qui trackent les données volumineuses.

---

## Partie 2 : Créer et configurer le workflow GitHub Actions

### Étape 2.1 : Structure du fichier de workflow

Le fichier `.github/workflows/ml-pipeline.yml` a été créé avec la structure suivante :

```
.github/
└── workflows/
    └── ml-pipeline.yml
```

### Étape 2.2 : Contenu du workflow

Le workflow `ml-pipeline.yml` exécute les étapes suivantes à chaque `push` :

**Déclencheurs** :
- S'exécute sur chaque push sur les branches `main` et `master`

**Étapes principales** :

1. **Checkout du code** - Récupère les derniers commits
2. **Configuration de Python** - Installe Python 3.10
3. **Cache pip** - Optimise le temps de build en cachant les dépendances
4. **Installation des dépendances** :
   - pip install -r requirements.txt
   - pip install dvc[s3] (pour le support S3 si nécessaire)

5. **Configuration DVC (optionnel)** :
   - Configure l'URL du dépôt distant DVC via les secrets GitHub
   - Exemple : S3, Google Cloud Storage, etc.

6. **Pull des données DVC** :
   ```bash
   dvc pull
   ```
   Récupère les fichiers trackés par DVC depuis le dépôt distant

7. **Reproduction du pipeline DVC** :
   ```bash
   dvc repro
   ```
   Exécute les étapes définies dans `dvc.yaml` :
   - `clean_data` : Nettoyage des données
   - `feature_engineering` : Extraction des features
   - `training` : Entraînement du modèle

8. **Entraînement du modèle** :
   ```bash
   python src/train.py
   ```
   Lance l'entraînement avec MLflow tracking

9. **Enregistrement du modèle** :
   ```bash
   python src/register_model.py
   ```
   Enregistre le modèle dans le registre MLflow

10. **Exécution des tests** :
    ```bash
    pytest -q
    ```
    Lance les tests unitaires

11. **Export des métriques MLflow** :
    - Génère un résumé JSON des métriques
    - Permet de comparer les runs entre exécutions

12. **Upload des artefacts** :
    - Sauvegarde `mlruns/` (résultats MLflow)
    - Sauvegarde `mlflow_metrics_summary.json`
    - Permet de télécharger les résultats depuis le UI GitHub

---

## Partie 3 : Configuration des secrets GitHub

### Étape 3.1 : Ajouter les secrets nécessaires

Pour que le workflow fonctionne correctement, ajoutez les secrets suivants :

1. Allez sur votre dépôt GitHub → **Settings** → **Secrets and variables** → **Actions**

2. Cliquez sur **New repository secret**

3. Ajoutez les secrets suivants :

| Secret Name | Valeur | Description |
|---|---|---|
| `MLFLOW_TRACKING_URI` | `http://localhost:5000` ou votre serveur MLflow | URL du serveur MLflow |
| `DVC_REMOTE_URL` | `s3://bucket-name/path` | URL du stockage distant DVC (optionnel) |
| `AWS_ACCESS_KEY_ID` | Votre clé d'accès AWS | Si vous utilisez S3 pour DVC (optionnel) |
| `AWS_SECRET_ACCESS_KEY` | Votre clé secrète AWS | Si vous utilisez S3 pour DVC (optionnel) |

### Exemple de configuration :

```bash
# Si vous utilisez un serveur MLflow local, vous pouvez configurer :
# MLFLOW_TRACKING_URI = file:///home/runner/mlflow

# Si vous utilisez DagsHub (recommended) :
# MLFLOW_TRACKING_URI = https://dagshub.com/USERNAME/REPO_NAME.mlflow
# DVC_REMOTE_URL = /tmp/dvc-storage (ou votre S3 bucket)
```

---

## Partie 4 : Vérification du pipeline CI/CD

### Étape 4.1 : Première exécution

1. Poussez vos changements sur GitHub :
   ```bash
   git add .
   git commit -m "Add GitHub Actions workflow"
   git push origin main
   ```

2. Allez sur votre dépôt GitHub et cliquez sur l'onglet **Actions**

3. Vous verrez le workflow en cours d'exécution

4. Attendez que le workflow se termine (généralement 5-15 minutes selon la taille des données)

### Étape 4.2 : Vérifier l'exécution

Indicateurs de succès :
- ✅ Tous les steps passent (pas de croix rouge)
- ✅ Pas de messages d'erreur dans les logs
- ✅ Les artefacts sont uploadés (visible dans la section "Artifacts")

Pour vérifier les logs :
1. Cliquez sur le workflow exécuté
2. Cliquez sur le job "build"
3. Déroulez chaque étape pour voir les logs

### Étape 4.3 : Modifier et tester

Pour déclencher une nouvelle exécution du pipeline :

1. **Modifier un fichier Python** :
   ```bash
   # Exemple : modifiez src/train.py
   git add src/train.py
   git commit -m "Update training parameters"
   git push origin main
   ```

2. **Ou modifier les données** :
   ```bash
   # Poussez les nouvelles données via DVC
   dvc add data/raw/new_dataset.csv
   git add data/raw/new_dataset.csv.dvc
   git commit -m "Update dataset"
   git push origin main
   ```

Le workflow se redéclenchera automatiquement sur chaque push !

---

## Partie 5 : Traçabilité avec MLflow

### Étape 5.1 : Vérifier les runs MLflow

Après chaque exécution du pipeline, un nouveau run MLflow est créé automatiquement.

#### Option A : UI MLflow locale

1. Lancez le serveur MLflow :
   ```bash
   mlflow ui
   ```

2. Allez sur `http://localhost:5000`

3. Explorez les runs créés :
   - Visualisez les métriques (accuracy, f1_score, etc.)
   - Comparez les performances entre runs
   - Vérifiez les paramètres utilisés

#### Option B : Consulter les artefacts depuis GitHub

1. Allez sur **Actions** → Dernier workflow exécuté
2. Scrollez jusqu'à la section "Artifacts"
3. Téléchargez `mlflow-runs` et ouvrez `mlflow_metrics_summary.json`
4. Vous y verrez les métriques de chaque exécution

### Étape 5.2 : Comparer les métriques entre runs

#### Via MLflow UI :

1. Allez dans l'onglet de votre expérience
2. Sélectionnez 2 ou plusieurs runs
3. Cliquez sur "Compare"
4. Visualisez les différences :
   - Paramètres utilisés
   - Métriques (accuracy, precision, recall, f1)
   - Durée d'exécution
   - Artifacts générés

#### Exemple de comparaison :

```
Run 1 (Dataset original)
- Accuracy: 0.82
- F1-Score: 0.79
- Durée: 2min 30s

Run 2 (Dataset augmenté)
- Accuracy: 0.85
- F1-Score: 0.82
- Durée: 3min 15s

✅ Améliorations : +3% accuracy, +3% f1-score
```

### Étape 5.3 : Automatiser le suivi des métriques

Le workflow génère automatiquement un fichier `mlflow_metrics_summary.json` qui contient :

```json
[
  {
    "exp": "0",
    "run": "run_id_123",
    "metrics": {
      "accuracy": [0.82],
      "f1_score": [0.79],
      "precision": [0.81],
      "recall": [0.78]
    }
  }
]
```

Vous pouvez utiliser ce fichier pour :
- Créer des graphiques de performance
- Générer des rapports automatiques
- Déclencher des alertes si les métriques diminuent

---

## Partie 6 : Bonnes pratiques et dépannage

### Étape 6.1 : Bonnes pratiques

1. **Versionnez vos données avec DVC** :
   ```bash
   dvc add data/raw/telecom_churn.csv
   git add data/raw/telecom_churn.csv.dvc
   git commit -m "Update churn dataset"
   git push origin main
   ```

2. **Utilisez des branches feature** :
   ```bash
   git checkout -b feature/improve-model
   # ... Faites vos modifications
   git push origin feature/improve-model
   # Créez une Pull Request sur GitHub
   ```

3. **Attendez que le CI/CD passe** avant de merger en main

4. **Consultez les logs du workflow** pour débugguer les problèmes

5. **Utilisez les secrets GitHub** pour les données sensibles (API keys, tokens)

### Étape 6.2 : Dépannage courant

#### Problème : Le workflow échoue sur "dvc pull"
- **Cause** : Le dépôt distant DVC n'est pas configuré
- **Solution** : 
  - Configurez un secret `DVC_REMOTE_URL`
  - Ou commentez le step "Pull DVC data" dans le workflow

#### Problème : Les tests échouent
- **Cause** : Les tests ne passent pas sur l'environnement CI
- **Solution** :
  - Vérifiez les logs avec `pytest -v`
  - Ajoutez des fixtures ou mocks dans `tests/conftest.py`

#### Problème : MLflow tracking ne fonctionne pas
- **Cause** : `MLFLOW_TRACKING_URI` non défini
- **Solution** :
  - Ajoutez le secret `MLFLOW_TRACKING_URI` dans GitHub Settings
  - Ou utilisez le tracking local : `MLFLOW_TRACKING_URI=file:///tmp/mlflow`

#### Problème : Les dépendances Python ne s'installent pas
- **Cause** : Version de Python incompatible
- **Solution** :
  - Vérifiez `python-version` dans le workflow
  - Mettez à jour `requirements.txt`

---

## Résumé des fichiers créés/modifiés

| Fichier | Description |
|---|---|
| `.github/workflows/ml-pipeline.yml` | Workflow GitHub Actions pour CI/CD |
| `dvc.yaml` | Configuration du pipeline DVC (déjà existant) |
| `requirements.txt` | Dépendances Python (déjà existant) |
| `.gitignore` | À vérifier pour exclure les fichiers non nécessaires |

---

## Prochaines étapes

1. ✅ Poussez le code sur GitHub
2. ✅ Vérifiez que le workflow s'exécute correctement
3. ✅ Consultez les métriques MLflow
4. ✅ Comparez les performances entre exécutions
5. ✅ Utilisez les branches feature pour développer
6. ✅ Mergez sur `main` après que le CI/CD passe

---

## Ressources utiles

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [DVC Pipeline Documentation](https://dvc.org/doc/user-guide/pipeline)
- [MLflow Tracking Documentation](https://mlflow.org/docs/latest/tracking.html)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

---

## Support

Si vous rencontrez des problèmes :
1. Consultez les logs du workflow dans l'onglet "Actions"
2. Vérifiez les secrets GitHub sont correctement configurés
3. Testez localement avec `dvc repro` et `python src/train.py`
4. Consultez la documentation officielle de DVC, MLflow et GitHub Actions

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