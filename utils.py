import os
import io
import streamlit as st
from PIL import Image


MODEL_PATH = "best.pt"


@st.cache_resource(show_spinner="Loading EcoVision model…")
def load_model():
    """Load YOLO model once and cache it for the entire session."""
    if not os.path.exists(MODEL_PATH):
        st.error(
            "❌ Model file `best.pt` not found. "
            "Please upload it to the root of your repository."
        )
        st.stop()
    from ultralytics import YOLO  # imported here so Streamlit Cloud doesn't pre-import on cold start
    model = YOLO(MODEL_PATH)
    return model


def predict_image(image: Image.Image):
    """
    Run classification inference on a PIL image.
    Returns list of (label, confidence) tuples — top 3.
    """
    model = load_model()

    # Convert PIL → bytes buffer → avoid writing temp files to disk
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    img_pil = Image.open(buf)

    results = model.predict(img_pil, verbose=False)

    probs = results[0].probs.data.tolist()
    names = results[0].names

    top3 = sorted(zip(names.values(), probs), key=lambda x: x[1], reverse=True)[:3]
    return top3
