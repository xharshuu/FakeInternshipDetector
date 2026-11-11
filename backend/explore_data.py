import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Dataset 1
print("=== DATASET 1 ===")
with open(r'd:\Harshit\FakeInternshipDetector\backend\dataset1.csv', encoding='utf-8', errors='replace') as f:
    r = csv.DictReader(f)
    total = 0
    scam = 0
    scam_types = {}
    for row in r:
        total += 1
        if row.get('is_scam', '0') == '1':
            scam += 1
            st = row.get('scam_type', '')
            scam_types[st] = scam_types.get(st, 0) + 1
    print(f"Total: {total}, Scam: {scam}, Legit: {total - scam}")
    print(f"Scam types: {scam_types}")

# Dataset 2
print("\n=== DATASET 2 ===")
with open(r'd:\Harshit\FakeInternshipDetector\backend\dataset2.csv', encoding='utf-8', errors='replace') as f:
    r = csv.DictReader(f)
    total = 0
    labels = {}
    sample_scam = None
    sample_legit = None
    for row in r:
        total += 1
        lab = row.get('label', '')
        labels[lab] = labels.get(lab, 0) + 1
        if lab == '1' and sample_scam is None:
            sample_scam = row.get('text', '')[:200]
        if lab == '0' and sample_legit is None:
            sample_legit = row.get('text', '')[:200]
    print(f"Total: {total}")
    print(f"Label distribution: {labels}")
    print(f"\nSample scam text: {sample_scam}")
    print(f"\nSample legit text: {sample_legit}")
