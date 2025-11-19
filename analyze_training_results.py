"""
Script d'analyse des résultats d'entraînement du modèle LSTM.
À exécuter après l'entraînement pour comparer les performances.
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_training_results():
    """
    Analyse et compare les résultats des deux modèles.
    """
    print("=" * 70)
    print("ANALYSE DES RÉSULTATS D'ENTRAÎNEMENT")
    print("=" * 70)

    # Chemins des métadonnées
    old_metadata_path = Path("models/exercise_classifier_metadata.json")
    new_metadata_path = Path("models/exercise_classifier_metadata.json")

    # Charger les métadonnées
    results = {}

    if old_metadata_path.exists():
        with open(old_metadata_path, "r") as f:
            old_meta = json.load(f)

        print("\n📊 MODÈLE PRÉCÉDENT (85 vidéos)")
        print("-" * 70)
        print(f"  Date d'entraînement: {old_meta.get('training_date', 'N/A')}")
        print(f"  Accuracy test: {old_meta.get('test_accuracy', 0):.2%}")
        print(f"  Loss test: {old_meta.get('test_loss', 0):.4f}")
        print(f"  Dataset size: {old_meta.get('max_sequence_length', 0)} frames max")
        print(f"  Features: {old_meta.get('n_features', 0)}")

        results["old"] = old_meta

    if new_metadata_path.exists():
        with open(new_metadata_path, "r") as f:
            new_meta = json.load(f)

        print("\n📊 NOUVEAU MODÈLE (1404 éléments)")
        print("-" * 70)
        print(f"  Date d'entraînement: {new_meta.get('training_date', 'N/A')}")
        print(f"  Accuracy test: {new_meta.get('test_accuracy', 0):.2%}")
        print(f"  Loss test: {new_meta.get('test_loss', 0):.4f}")
        print(f"  Dataset size: {new_meta.get('max_sequence_length', 0)} frames max")
        print(f"  Features: {new_meta.get('n_features', 0)}")

        results["new"] = new_meta

    # Comparaison
    if "old" in results and "new" in results:
        print("\n📈 AMÉLIORATION")
        print("-" * 70)

        acc_diff = results["new"]["test_accuracy"] - results["old"]["test_accuracy"]
        loss_diff = results["old"]["test_loss"] - results["new"]["test_loss"]

        print(f"  Accuracy: {acc_diff:+.2%}")
        print(f"  Loss: {loss_diff:+.4f}")

        if acc_diff > 0:
            print(f"\n  ✅ Amélioration de l'accuracy de {acc_diff:.2%}")
        elif acc_diff < 0:
            print(f"\n  ⚠️ Dégradation de l'accuracy de {abs(acc_diff):.2%}")
        else:
            print(f"\n  ➡️ Accuracy stable")

        if loss_diff > 0:
            print(f"  ✅ Réduction de la loss de {loss_diff:.4f}")
        elif loss_diff < 0:
            print(f"  ⚠️ Augmentation de la loss de {abs(loss_diff):.4f}")
        else:
            print(f"  ➡️ Loss stable")

    # Recommandations
    print("\n💡 RECOMMANDATIONS")
    print("-" * 70)

    if "new" in results:
        acc = results["new"]["test_accuracy"]
        loss = results["new"]["test_loss"]

        if acc >= 0.95 and loss < 0.1:
            print("  ✅ Excellent modèle ! Prêt pour la production.")
        elif acc >= 0.90 and loss < 0.2:
            print("  ✅ Bon modèle. Peut être amélioré avec:")
            print("     - Plus d'epochs")
            print("     - Data augmentation")
            print("     - Ajustement learning rate")
        elif acc >= 0.80:
            print("  ⚠️ Modèle correct mais perfectible:")
            print("     - Vérifier la distribution des classes")
            print("     - Augmenter la complexité du modèle")
            print("     - Ajouter plus de données")
        else:
            print("  ❌ Modèle à retravailler:")
            print("     - Revoir l'architecture")
            print("     - Vérifier la qualité des données")
            print("     - Augmenter drastiquement le dataset")

    print("\n" + "=" * 70)
    print("ANALYSE TERMINÉE")
    print("=" * 70)

    return results


def compare_confusion_matrices():
    """
    Compare les matrices de confusion si disponibles.
    """
    print("\n📊 ANALYSE DES MATRICES DE CONFUSION")
    print("-" * 70)
    print("  (À compléter après avoir sauvegardé les matrices)")


if __name__ == "__main__":
    results = analyze_training_results()

    print("\n\n📋 PROCHAINES ÉTAPES")
    print("-" * 70)
    print("1. Vérifier les courbes d'entraînement dans le notebook")
    print("2. Tester le modèle en temps réel avec l'interface")
    print("3. Si nécessaire, ajuster les hyperparamètres")
    print("4. Déployer le nouveau modèle dans l'application")
