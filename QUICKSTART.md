# 🚀 Guide de Démarrage Rapide - SmartFit Coach

Bienvenue dans SmartFit Coach ! Ce guide vous permettra de démarrer votre première session d'entraînement en moins de 5 minutes.

---

## ⚡ Installation Express

### Étape 1 : Prérequis

Assurez-vous d'avoir :
- ✅ Python 3.8 ou supérieur installé
- ✅ Une webcam fonctionnelle
- ✅ Git installé

### Étape 2 : Installation

```powershell
# Cloner le projet
git clone https://github.com/itsmardochee/SmartFit-Coach.git
cd SmartFit-Coach

# Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

---

## 🎯 Lancer l'Application

```powershell
streamlit run interface/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`.

---

## 💪 Utiliser SmartFit Coach

### 1️⃣ Sélectionner un exercice

Dans le **menu latéral gauche**, choisissez :
- 🏋️ **Squats**
- 💪 **Pompes**

### 2️⃣ Configurer les paramètres (optionnel)

Dans **"Paramètres avancés"** :
- Ajuster la confiance de détection (0.5 par défaut)
- Activer/désactiver l'affichage du squelette

### 3️⃣ Démarrer la session

1. Cliquez sur **"▶️ Démarrer"**
2. Autorisez l'accès à votre webcam si demandé
3. Positionnez-vous devant la caméra :
   - **Corps entièrement visible**
   - **Distance : 1,5 à 2 mètres**
   - **Éclairage suffisant**

### 4️⃣ Effectuer les exercices

#### Pour les SQUATS 🏋️

**Position de départ :**
- Pieds écartés à largeur d'épaules
- Dos droit, regard devant

**Exécution :**
1. Descends en pliant les genoux
2. Garde le dos droit
3. Descends jusqu'à ce que les genoux soient à ~90°
4. Remonte en position debout

**Feedback en temps réel :**
- ✅ "Bonne profondeur !" → Parfait, continue !
- ⬇️ "Continue de descendre" → Descends un peu plus
- ⬆️ "Bonne remontée" → Phase de montée détectée
- ⚠️ "Descends plus bas" → Pas assez profond

#### Pour les POMPES 💪

**Position de départ :**
- Mains au sol, largeur d'épaules
- Corps aligné (planche)
- Regard vers le sol

**Exécution :**
1. Descends en pliant les coudes
2. Garde le corps aligné (gainage)
3. Coudes à ~90° en position basse
4. Pousse pour remonter

**Feedback en temps réel :**
- ✅ "Parfait ! Remonte maintenant" → Bonne profondeur
- ⬇️ "Bonne descente" → Phase descendante OK
- ⬆️ "Bonne poussée !" → Remontée détectée
- ⚠️ "Descends encore un peu" → Pas assez bas

### 5️⃣ Consulter les statistiques

**Pendant l'exercice :**
- **Compteur de répétitions** en gros
- **Phase actuelle** (debout, descente, position basse, montée)
- **Chronomètre** de la session
- **Feedback visuel** avec code couleur :
  - 🟢 Vert = Excellent
  - 🟠 Orange = Attention
  - 🔵 Bleu = Information

**En fin de session :**
- Total de répétitions
- Répétitions valides
- Taux de réussite (%)

### 6️⃣ Arrêter la session

- Cliquez sur **"⏹️ Arrêter"** pour terminer
- Cliquez sur **"🔄 Réinitialiser"** pour remettre le compteur à zéro

---

## 🎥 Conseils pour une bonne détection

### Positionnement optimal

```
         [WEBCAM]
             |
             | 1,5-2m
             |
             v
         [VOUS] 👤
```

### ✅ À FAIRE

- Se positionner **face à la caméra** (de préférence) ou **de profil**
- Assurer un **éclairage frontal** (pas de contre-jour)
- Porter des **vêtements contrastés** avec l'arrière-plan
- Dégager **tout le corps** dans le cadre
- Éviter les **arrière-plans chargés**

### ❌ À ÉVITER

- Être trop près ou trop loin de la caméra
- Porter des vêtements de la même couleur que le fond
- Faire les exercices dans l'obscurité
- Avoir des personnes/objets qui obstruent la vue
- Se positionner de dos à la caméra

---

## 🐛 Problèmes Courants

### "⚠️ Aucune personne détectée"

**Solutions :**
- Reculez-vous de la caméra
- Vérifiez que tout votre corps est visible
- Améliorez l'éclairage
- Réduisez le seuil de confiance dans les paramètres

### "⚠️ Position toi de façon à être entièrement visible"

**Solutions :**
- Assurez-vous que les épaules, hanches, genoux et chevilles sont visibles
- Changez d'angle de caméra
- Éloignez-vous un peu

### Le compteur ne s'incrémente pas

**Solutions :**
- Vérifiez que vous effectuez le mouvement complet
- Pour les squats : descendez jusqu'à ~90° (genoux)
- Pour les pompes : descendez jusqu'à ~90° (coudes)
- Ralentissez le mouvement

### L'application ne démarre pas

**Solutions :**
```powershell
# Vérifier l'installation de Streamlit
pip list | Select-String streamlit

# Réinstaller si nécessaire
pip install --upgrade streamlit

# Relancer
streamlit run interface/app.py
```

---

## 🧪 Tester la Détection (Mode Développeur)

Pour tester uniquement la détection de pose sans l'interface :

```powershell
python demo_detection.py
```

Appuyez sur `q` pour quitter.

---

## 📊 Statistiques et Métriques

### Répétitions Valides

Une répétition est considérée **valide** si :

**Squats :**
- Angle du genou ≤ 90°
- Angle de la hanche ≤ 90°
- Cycle complet détecté

**Pompes :**
- Angle du coude ≤ 90°
- Cycle complet détecté

### Taux de Réussite

```
Taux de réussite (%) = (Répétitions valides / Total répétitions) × 100
```

Un bon taux de réussite est **≥ 80%**.

---

## 🎓 Prochaines Étapes

Une fois à l'aise avec les exercices de base :

1. **Expérimenter** avec différents angles de caméra
2. **Analyser** vos statistiques pour progresser
3. **Ajouter** de la difficulté (poids, tempo, etc.)
4. **Consulter** la documentation complète dans `/docs`

---

## 🆘 Besoin d'Aide ?

- 📖 [Documentation complète](docs/)
- 🐛 [Signaler un bug](https://github.com/itsmardochee/SmartFit-Coach/issues)
- 💬 [Discussions](https://github.com/itsmardochee/SmartFit-Coach/discussions)

---

## 🎉 Prêt à Commencer !

Vous êtes maintenant prêt à utiliser SmartFit Coach !

```powershell
streamlit run interface/app.py
```

**Bon entraînement ! 💪🔥**

---

*SmartFit Coach - Votre coach sportif intelligent*
