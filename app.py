
import streamlit as st
from PIL import Image
from utils import predict_image

st.set_page_config(page_title="EcoVision AI", layout="wide")

st.title("♻️ EcoVision AI - Waste Classifier")

uploaded = st.file_uploader("Upload Waste Image", type=["jpg", "png", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze"):
        result = predict_image(img)
        label, confidence = result[0]

        st.success(f"Prediction: {label} ({confidence*100:.2f}%)")
