"""
Train a scam detection model using ALL four CSV datasets.
- Dataset 1: Structured job listings with is_scam label
- Dataset 2: Text + label (scam/legit)
- Dataset 3: internship_job_course_dataset_30000.csv  — 30K rows (text/label)
- Dataset 4: mixed_dataset_50000.csv — 50K rows (text/label)

Combines all into text + label, trains TF-IDF + Logistic Regression,
and saves the model + vectorizer to disk via joblib.
"""

import csv
import os
import sys
import io
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

texts = []
labels = []

# ── Dataset 1: structured job listings ──────────────────────────────
print("Loading dataset 1 ...")
with open(os.path.join(BASE, 'dataset1.csv'), encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Build a combined text from multiple informative columns
        parts = [
            row.get('title', ''),
            row.get('company', ''),
            row.get('description', ''),
            row.get('salary', ''),
            row.get('contact_email', ''),
            row.get('job_type', ''),
            row.get('experience', ''),
            row.get('industry', ''),
            row.get('location', ''),
            row.get('scam_type', ''),
        ]
        combined = ' '.join(p for p in parts if p)
        if combined.strip():
            texts.append(combined)
            labels.append(1 if row.get('is_scam', '0') == '1' else 0)

print(f"  Loaded {len(texts)} rows from dataset 1")

# ── Helper: load a text+label CSV ───────────────────────────────────
def load_text_label_csv(filename, dataset_name):
    """Load a CSV with 'text' and 'label' (scam/legit) columns."""
    count_before = len(texts)
    print(f"Loading {dataset_name} ...")
    path = os.path.join(BASE, filename)
    if not os.path.exists(path):
        print(f"  WARNING: File not found: {filename}, skipping.")
        return
    with open(path, encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('text', '').strip()
            label_str = row.get('label', '').strip().lower()
            if text and label_str in ('scam', 'legit'):
                texts.append(text)
                labels.append(1 if label_str == 'scam' else 0)
    print(f"  Loaded {len(texts) - count_before} rows from {dataset_name}")


# ── Dataset 2: text + label ─────────────────────────────────────────
load_text_label_csv('dataset2.csv', 'dataset 2')

# ── Dataset 3: 30K internship/job/course listings ──────────────────
load_text_label_csv('internship_job_course_dataset_30000.csv', 'dataset 3 (30K internship/job/course)')

# ── Dataset 4: 50K mixed listings ──────────────────────────────────
load_text_label_csv('mixed_dataset_50000.csv', 'dataset 4 (50K mixed)')

print(f"\n  Total combined: {len(texts)} samples")
print(f"  Scam: {sum(labels)}, Legit: {len(labels) - sum(labels)}")

# ── Train / Test Split ──────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# ── TF-IDF Vectorisation ───────────────────────────────────────────
print("\nTraining TF-IDF vectorizer ...")
vectorizer = TfidfVectorizer(
    max_features=25000,
    ngram_range=(1, 2),
    stop_words='english',
    sublinear_tf=True,
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# ── Logistic Regression ────────────────────────────────────────────
print("Training Logistic Regression classifier ...")
clf = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
clf.fit(X_train_tfidf, y_train)

# ── Evaluation ──────────────────────────────────────────────────────
print("\n--- Classification Report (Test Set) ---")
y_pred = clf.predict(X_test_tfidf)
print(classification_report(y_test, y_pred, target_names=['Legit', 'Scam']))

# ── Save model artifacts ────────────────────────────────────────────
model_dir = os.path.join(BASE, 'model')
os.makedirs(model_dir, exist_ok=True)

joblib.dump(vectorizer, os.path.join(model_dir, 'tfidf_vectorizer.joblib'))
joblib.dump(clf, os.path.join(model_dir, 'scam_classifier.joblib'))

print(f"\nModel saved to {model_dir}")
print("Done!")
