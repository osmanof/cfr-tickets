import joblib
import sklearn_crfsuite

from sklearn.model_selection import train_test_split
from sklearn_crfsuite import metrics

from dataset import load_sentences
from features import sent2features, sent2labels


DATA_PATH = "../data/sentences.csv"
MODEL_PATH = "../models/model.pkl"

LABELS = [
    "B-FROM", "I-FROM",
    "B-TO", "I-TO",
    "B-DATE_FROM", "I-DATE_FROM",
    "B-DATE_TO", "I-DATE_TO",
]


def main():
    sentences = load_sentences(DATA_PATH)

    X = [sent2features(sent) for sent in sentences]
    y = [sent2labels(sent) for sent in sentences]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )

    crf.fit(X_train, y_train)

    y_pred = crf.predict(X_test)

    report = metrics.flat_classification_report(
        y_test,
        y_pred,
        labels=LABELS
    )

    print(report)

    joblib.dump(crf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
