import os
import numpy as np
import streamlit as st
from PIL import Image


DEFAULT_IMAGE = "sample_images/lena.png"


def load_image(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        return np.array(image), "Using uploaded image"

    if not os.path.exists(DEFAULT_IMAGE):
        st.error(f"Default image not found: {DEFAULT_IMAGE}")
        st.stop()

    image = Image.open(DEFAULT_IMAGE).convert("RGB")
    return np.array(image), "No image uploaded — using default Lena image"

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)