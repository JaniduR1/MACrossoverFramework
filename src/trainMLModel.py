from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def trainAndEvaluateModel(X_train, X_test, y_train, y_test):
    """
    Trains a random forest model and evaluates it.

    Returns:
        model: Trained model
        metrics: Dict of accuracy and classification report
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)

    metrics = {
        "Accuracy": round(accuracy * 100, 2),
        "Precision (Up)": round(report["1"]["precision"], 2),
        "Recall (Up)": round(report["1"]["recall"], 2),
        "F1 (Up)": round(report["1"]["f1-score"], 2),
        "Precision (Down)": round(report["0"]["precision"], 2),
        "Recall (Down)": round(report["0"]["recall"], 2),
        "F1 (Down)": round(report["0"]["f1-score"], 2),
    }

    return model, metrics, predictions

def plotConfusionMatrix(y_true, y_pred, saveTo="images/"):
    """
    Plots and saves a confusion matrix for ML classification results.
    """
    cm = confusion_matrix(y_true, y_pred)
    labels = ["Down", "Up"]

    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=labels, yticklabels=labels, cmap="Blues")
    plt.title("ML Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f"{saveTo}mlConfusionMatrix.png")
    plt.close()