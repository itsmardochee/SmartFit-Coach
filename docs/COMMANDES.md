# 🔧 Commandes Utiles - SmartFit Coach

## 📦 Installation et Configuration

### Créer l'environnement virtuel
```bash
python -m venv venv
```

### Activer l'environnement
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Fish shell (Linux/Mac)
source venv/bin/activate.fish
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Mettre à jour requirements.txt
```bash
pip freeze > requirements.txt
```

---

## 🚀 Exécution

### Lancer la démonstration de détection
```bash
python demo_detection.py
```

### Lancer l'application complète (à venir)
```bash
streamlit run interface/app.py
```

---

## 🧪 Tests

### Exécuter tous les tests
```bash
pytest tests/ -v
```

### Tests avec couverture
```bash
pytest tests/ --cov=src --cov-report=html
```

### Ouvrir le rapport de couverture
```bash
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Tests d'un fichier spécifique
```bash
pytest tests/test_detection.py -v
```

### Tests avec marqueurs
```bash
pytest tests/ -v -m "not slow"
```

---

## 📓 Notebooks

### Lancer Jupyter
```bash
jupyter notebook notebooks/
```

### Lancer JupyterLab
```bash
jupyter lab notebooks/
```

---

## 🔍 Qualité du Code

### Formater le code avec Black
```bash
black src/ tests/ interface/
```

### Vérifier le style avec Flake8
```bash
flake8 src/ tests/ interface/ --max-line-length=100
```

### Type checking avec MyPy
```bash
mypy src/
```

### Linter avec Pylint
```bash
pylint src/
```

---

## 🐛 Débogage

### Afficher les logs
```bash
tail -f logs/smartfit.log
```

### Mode verbose pour la détection
```bash
python demo_detection.py --verbose
```

### Profiling des performances
```bash
python -m cProfile -o profile.stats demo_detection.py
```

### Analyser le profiling
```bash
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime'); p.print_stats(20)"
```

---

## 📊 Analyse des Données

### Compter les sessions enregistrées
```bash
ls -la data/sessions/ | wc -l
```

### Afficher le contenu d'une session
```bash
cat data/sessions/session_*.json | python -m json.tool
```

### Analyser les keypoints
```bash
python -c "import json; data = json.load(open('data/keypoints_sample.json')); print(f'Keypoints: {len(data[\"keypoints\"])}')"
```

---

## 🧹 Nettoyage

### Supprimer les fichiers cache Python
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Nettoyer les notebooks
```bash
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

### Supprimer les données de test
```bash
rm -rf data/sessions/*.json
rm -rf data/*.jpg data/*.png
```

### Nettoyer les logs
```bash
rm -rf logs/*.log
```

---

## 🔄 Git

### Vérifier le statut
```bash
git status
```

### Ajouter tous les changements
```bash
git add .
```

### Commit avec message
```bash
git commit -m "Étape 1: Détection de pose terminée"
```

### Push vers le dépôt
```bash
git push origin main
```

### Créer une nouvelle branche
```bash
git checkout -b feature/comptage-repetitions
```

### Voir l'historique
```bash
git log --oneline --graph --all
```

---

## 📦 Dépendances

### Installer une nouvelle dépendance
```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Mettre à jour une dépendance
```bash
pip install --upgrade <package-name>
```

### Vérifier les dépendances obsolètes
```bash
pip list --outdated
```

---

## 🎥 Capture de Démo

### Enregistrer une vidéo de la démo
```bash
# Utiliser ffmpeg (Linux)
ffmpeg -f v4l2 -i /dev/video0 -t 30 demo_video.mp4
```

### Créer un GIF de démonstration
```bash
ffmpeg -i demo_video.mp4 -vf "fps=10,scale=640:-1:flags=lanczos" demo.gif
```

---

## 📚 Documentation

### Générer la documentation API
```bash
pdoc --html --output-dir docs/api src/
```

### Serveur de documentation local
```bash
python -m http.server 8000 -d docs/
```

---

## 🔐 Sécurité

### Vérifier les vulnérabilités
```bash
pip-audit
```

### Scanner le code avec Bandit
```bash
bandit -r src/
```

---

## 💻 Développement

### Installer les outils de développement
```bash
pip install black flake8 mypy pylint pytest pytest-cov
```

### Pre-commit hooks (recommandé)
```bash
pip install pre-commit
pre-commit install
```

---

## 🚨 Résolution de Problèmes

### Caméra non détectée
```bash
# Lister les caméras disponibles (Linux)
ls -l /dev/video*

# Tester avec v4l2
v4l2-ctl --list-devices
```

### Problèmes de permissions
```bash
# Ajouter l'utilisateur au groupe video (Linux)
sudo usermod -a -G video $USER
```

### Réinstaller les dépendances
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Reset de l'environnement
```bash
deactivate
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**Astuce :** Ajoutez ces commandes à vos alias shell pour un accès rapide !

```bash
# Exemple pour .bashrc ou .zshrc
alias sfc-test='pytest tests/ -v'
alias sfc-demo='python demo_detection.py'
alias sfc-format='black src/ tests/ interface/'
```

Pour Fish shell :
```fish
# Ajouter à ~/.config/fish/config.fish
alias sfc-test='pytest tests/ -v'
alias sfc-demo='python demo_detection.py'
alias sfc-format='black src/ tests/ interface/'
```
