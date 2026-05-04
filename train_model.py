"""
train_model.py
Jalankan script ini untuk melatih ulang model SVD dari dataset MovieLens.

Usage:
    python train_model.py
"""

import pandas as pd
import pickle
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split, cross_validate

print("=" * 50)
print("CineMatch — SVD Model Training")
print("=" * 50)

# ── Load data ──────────────────────────────────────────────
print("\n[1/4] Memuat dataset...")
ratings = pd.read_csv("ratings_data.csv")
movies = pd.read_csv("movies_data.csv")
print(f"      {len(ratings):,} ratings | {ratings['userId'].nunique()} users | {movies['movieId'].nunique():,} films")

# ── Prepare Surprise dataset ───────────────────────────────
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[["userId", "movieId", "rating"]], reader)

# ── Train/test split ───────────────────────────────────────
print("\n[2/4] Split data (80% train / 20% test)...")
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# ── Train SVD ──────────────────────────────────────────────
print("\n[3/4] Melatih model SVD...")
print("      n_factors=50 | n_epochs=30 | lr=0.005 | reg=0.02")
model = SVD(
    n_factors=50,
    n_epochs=30,
    lr_all=0.005,
    reg_all=0.02,
    random_state=42,
    verbose=True
)
model.fit(trainset)

# ── Evaluate ───────────────────────────────────────────────
print("\n[4/4] Evaluasi model...")
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

# Precision@10
import numpy as np
def precision_at_k(predictions, k=10, threshold=3.5):
    user_est_true = {}
    for uid, _, true_r, est, _ in predictions:
        user_est_true.setdefault(uid, []).append((est, true_r))
    precisions = []
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        n_rel_and_rec_k = sum((true_r >= threshold) for (_, true_r) in user_ratings[:k])
        precisions.append(n_rel_and_rec_k / k)
    return np.mean(precisions)

p10 = precision_at_k(predictions, k=10)
print(f"\n{'='*50}")
print(f"  RMSE        : {rmse:.4f}  (target: < 1.0)")
print(f"  MAE         : {mae:.4f}")
print(f"  Precision@10: {p10*100:.2f}%  (target: > 60%)")
print(f"{'='*50}")

# ── Save model ─────────────────────────────────────────────
with open("svd_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("\n✅ Model disimpan ke svd_model.pkl")
print("   Jalankan: streamlit run app.py")
