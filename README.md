# 🎬 CineMatch — Film Recommendation System

Sistem rekomendasi film berbasis **SVD (Singular Value Decomposition)** menggunakan dataset MovieLens Latest Small.

---

## 📁 Struktur File

```
cinematch/
├── app.py              # Aplikasi Streamlit (UI)
├── train_model.py      # Script training model SVD
├── svd_model.pkl       # Model SVD terlatih
├── movies_data.csv     # Data film
├── ratings_data.csv    # Data rating user
├── requirements.txt    # Dependensi Python
└── README.md
```

---

## ⚙️ Setup & Instalasi

### 1. Install dependensi
```bash
pip install -r requirements.txt
```

### 2. (Opsional) Re-train model
Jika ingin melatih ulang model dari awal:
```bash
python train_model.py
```

### 3. Jalankan aplikasi
```bash
streamlit run app.py
```

Buka browser ke `http://localhost:8501`

---

## 🚀 Cara Pakai

1. Masukkan **User ID** (1 hingga 610)
2. Klik tombol **GET RECOMMENDATIONS**
3. Sistem menampilkan **10 rekomendasi film** dengan prediksi rating

---

## 📊 Performa Model

| Metrik | Nilai | Target |
|---|---|---|
| RMSE | **0.879** | < 1.0 ✅ |
| Precision@10 | **96.2%** | > 60% ✅ |
| Sparsity data | ~98.3% | — |

---

## 🧠 Cara Kerja

Model SVD (Singular Value Decomposition) memdekomposisi matriks user-item rating menjadi representasi laten berdimensi rendah:

```
R ≈ U × Σ × Vᵀ
```

- **U** = representasi laten setiap user
- **Σ** = nilai singular (bobot faktor laten)
- **V** = representasi laten setiap film

Hyperparameter yang digunakan:
- `n_factors = 50` (dimensi laten)
- `n_epochs = 30` (iterasi training)
- `lr_all = 0.005` (learning rate)
- `reg_all = 0.02` (regularisasi)

---

## 📦 Dataset

**MovieLens Latest Small** — [grouplens.org](https://grouplens.org/datasets/movielens/)
- 100,836 ratings
- 610 users
- 9,742 films
- Rating scale: 0.5 – 5.0

---

## 👥 Tim

Capstone Project — Pijak × IBM SkillsBuild  
Tema: Machine Learning / AI — Sistem Rekomendasi
