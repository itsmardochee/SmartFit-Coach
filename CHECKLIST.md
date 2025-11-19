# 🎯 Checklist de Vérification - SmartFit Coach MVP

## ✅ Avant de Lancer l'Application

Utilisez cette checklist pour vous assurer que tout est prêt.

---

## 📋 Installation

- [ ] Python 3.8+ installé
  ```powershell
  python --version  # Devrait afficher 3.8 ou plus
  ```

- [ ] Dépôt cloné
  ```powershell
  cd SmartFit-Coach
  pwd  # Devrait afficher le chemin du projet
  ```

- [ ] Environnement virtuel créé et activé
  ```powershell
  venv\Scripts\Activate.ps1
  # Le terminal devrait afficher (venv) au début
  ```

- [ ] Dépendances installées
  ```powershell
  pip list | Select-String streamlit
  # Devrait afficher streamlit et sa version
  ```

---

## 🔍 Vérification des Fichiers Clés

- [ ] `interface/app.py` existe
- [ ] `src/counting/angle_calculator.py` existe
- [ ] `src/counting/exercise_detectors/squat_counter.py` existe
- [ ] `src/counting/exercise_detectors/pushup_counter.py` existe
- [ ] `tests/test_counting.py` existe

---

## 🧪 Tests

- [ ] Tests unitaires exécutés
  ```powershell
  pytest tests/test_counting.py -v
  # Devrait afficher: 17/18 tests passed
  ```

- [ ] Aucune erreur de compilation
  ```powershell
  python -c "from src.counting.angle_calculator import calculate_angle; print('✅ OK')"
  ```

---

## 📹 Matériel

- [ ] Webcam branchée et fonctionnelle
- [ ] Espace dégagé devant la caméra (2m x 2m minimum)
- [ ] Bon éclairage (pas de contre-jour)
- [ ] Arrière-plan dégagé (pas trop chargé)

---

## 🚀 Premier Lancement

### 1. Lancer l'application

```powershell
streamlit run interface/app.py
```

**Attendu :** 
- Une fenêtre de navigateur s'ouvre automatiquement
- L'application charge en ~5 secondes
- Pas d'erreur dans le terminal

### 2. Autoriser la webcam

**Attendu :**
- Le navigateur demande l'autorisation d'accès à la webcam
- Cliquez sur "Autoriser"

### 3. Test de détection

**Étapes :**
1. Sélectionner "Squats" dans le menu latéral
2. Cliquer sur "▶️ Démarrer"
3. Se positionner devant la caméra (corps entièrement visible)

**Attendu :**
- La vidéo s'affiche
- Le squelette (traits blancs) est visible sur votre corps
- Les compteurs sont à 0

### 4. Test de comptage

**Étapes :**
1. Faire 3 squats complets (descendre jusqu'à ~90° de genou)
2. Observer le compteur

**Attendu :**
- Le compteur s'incrémente à chaque répétition complète
- Le feedback change selon la phase
- Les statistiques se mettent à jour

---

## ✅ Critères de Réussite

### Interface

- [ ] Vidéo s'affiche en temps réel
- [ ] Squelette visible sur le corps
- [ ] Compteur fonctionne (s'incrémente)
- [ ] Feedback s'affiche et change
- [ ] Chronomètre fonctionne
- [ ] Statistiques se mettent à jour
- [ ] Boutons "Démarrer/Arrêter/Reset" fonctionnent

### Performance

- [ ] FPS ≥ 20 (visible en haut à gauche si implémenté)
- [ ] Pas de lag majeur
- [ ] Réactivité < 1 seconde

### Comptage

- [ ] **Squats :** 
  - [ ] Compte quand on descend et remonte
  - [ ] Ne compte pas si on ne descend pas assez
  - [ ] Feedback "Descends plus bas" si nécessaire

- [ ] **Pompes :**
  - [ ] Compte quand on descend et remonte
  - [ ] Ne compte pas si on ne descend pas assez
  - [ ] Feedback "Descends encore un peu" si nécessaire

### Feedback

- [ ] Messages changent selon la phase du mouvement
- [ ] Couleurs différentes (vert/orange/bleu)
- [ ] Messages clairs et compréhensibles

---

## 🐛 Résolution de Problèmes

### L'application ne démarre pas

**Erreur : "No module named 'streamlit'"**
```powershell
pip install streamlit
```

**Erreur : "No module named 'src'"**
```powershell
# Vérifier que vous êtes dans le bon répertoire
pwd  # Devrait afficher D:\SmartFit-Coach

# Ajouter le chemin au PYTHONPATH
$env:PYTHONPATH = "."
```

### La webcam ne fonctionne pas

**Erreur : "Impossible d'accéder à la webcam"**
- Vérifier qu'aucune autre application n'utilise la webcam
- Fermer Zoom, Teams, Skype, etc.
- Redémarrer l'application

### Le squelette ne s'affiche pas

**Possible :**
- Vous êtes trop près ou trop loin de la caméra
- L'éclairage est insuffisant
- Le corps n'est pas entièrement visible
- Reculez-vous d'1-2 mètres

### Le compteur ne s'incrémente pas

**Vérifier :**
- Vous effectuez le mouvement complet
- Pour les squats : descendez jusqu'à ~90° (genoux pliés)
- Pour les pompes : descendez jusqu'à ~90° (coudes pliés)
- Ralentissez le mouvement

### Performance lente (FPS < 15)

**Solutions :**
- Réduire la résolution de la webcam (modifier `video_capture.py`)
- Fermer les applications gourmandes
- Désactiver l'affichage du squelette dans les paramètres

---

## 📊 Validation Finale

Cochez quand vous avez réussi à :

- [ ] Lancer l'application sans erreur
- [ ] Voir votre corps détecté avec le squelette
- [ ] Effectuer 5 squats comptés correctement
- [ ] Effectuer 5 pompes comptées correctement
- [ ] Lire et comprendre le feedback en temps réel
- [ ] Consulter les statistiques de session
- [ ] Arrêter et redémarrer une session

---

## 🎉 Félicitations !

Si tous les points sont cochés, **votre installation est parfaite** ! 🚀

Vous pouvez maintenant :
1. Utiliser l'application pour vos entraînements
2. Tester avec différents exercices
3. Expérimenter avec les paramètres
4. Consulter la documentation pour aller plus loin

---

## 📚 Pour Aller Plus Loin

- **Guide complet :** `QUICKSTART.md`
- **Documentation technique :** `docs/MVP_COMPLETE.md`
- **Synthèse :** `SYNTHESE.md`
- **Célébration :** `SUCCESS.md`

---

## 🆘 Support

**En cas de problème :**
1. Consultez `QUICKSTART.md` section "Problèmes Courants"
2. Vérifiez les logs dans le terminal
3. Ouvrez une issue sur GitHub
4. Consultez la documentation

---

**Bon entraînement avec SmartFit Coach ! 💪🔥**

*Checklist Version 1.0.0 - 14 Novembre 2025*
