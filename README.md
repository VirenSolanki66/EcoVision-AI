# ♻️ EcoVision AI — Waste Classification App

Smart waste detection and classification powered by **YOLOv8** + **Streamlit**.

---

## 📁 Project Structure

```
EcoVision-AI/
├── app.py                  # Main Streamlit UI
├── utils.py                # Model loading & prediction
├── best.pt                 # YOLOv8 classification model (upload manually)
├── requirements.txt        # Python dependencies (pinned versions)
├── runtime.txt             # Python version for Streamlit Cloud
├── packages.txt            # System packages for Streamlit Cloud
├── .streamlit/
│   └── config.toml         # Streamlit server config
└── README.md
```

---

## ⚙️ Local Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Make sure `best.pt` is in the **root folder** before running.

---

## 🚀 Deploy on Streamlit Cloud — Step by Step

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial EcoVision AI deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/EcoVision-AI.git
git push -u origin main
```

> ⚠️ **best.pt** must be committed too. If it's larger than 100 MB, use Git LFS (see below).

#### If best.pt > 100 MB — use Git LFS

```bash
git lfs install
git lfs track "*.pt"
git add .gitattributes
git add best.pt
git commit -m "Add model via Git LFS"
git push
```

---

### Step 2 — Deploy on Streamlit Cloud

1. Go to → **https://share.streamlit.io**
2. Click **"New app"**
3. Connect your **GitHub account** if not already done
4. Select:
   - **Repository:** `YOUR_USERNAME/EcoVision-AI`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy"**

Streamlit Cloud will automatically read:
- `runtime.txt` → Python 3.10.14
- `requirements.txt` → all pinned packages
- `packages.txt` → system libs (libgl, libglib)

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `ImportError: cv2` | Use `opencv-python-headless` (already in requirements.txt) |
| Python 3.14 used instead of 3.10 | Ensure `runtime.txt` says exactly `python-3.10.14` |
| `best.pt not found` | Commit the file to repo or use Git LFS for large files |
| App shows "does not exist" | Wait 2–3 min after deploy; check logs in Streamlit Cloud dashboard |
| Memory crash on free tier | Model is cached via `@st.cache_resource` — only loads once |

---

## 🔢 Pinned Dependency Versions

| Package | Version |
|---|---|
| Python | 3.10.14 |
| streamlit | 1.35.0 |
| ultralytics | 8.2.18 |
| torch | 2.2.2 |
| torchvision | 0.17.2 |
| opencv-python-headless | 4.9.0.80 |
| pillow | 10.3.0 |
| numpy | 1.26.4 |
