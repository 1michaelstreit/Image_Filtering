import streamlit as st

# Importing functions from other modules
from processing import (
    add_gaussian_noise_gray,
    add_salt_pepper_noise,
    add_white_noise,
    apply_denoising,
    compute_residual,
    amplify_residual,
    get_zoom_crop,
    resize_crop_for_display,
)

from utils import (
    load_image,
    load_css
    )

from metrics import mse, psnr

load_css("styles.css")

# Page configuration
st.set_page_config(
    page_title="Image Noise and Denoising Demo",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
         'About': "Designed by Michael Streit for MIA course demo. Upload your own image or use the default Lena image to explore different noise types and denoising methods."
    }
)

# ---------------- HEADER ---------------- #
st.title("Image Noise and Denoising Demo",
         text_alignment="center")

with st.sidebar:

    uploaded_file = st.file_uploader(
        "Upload an image (optional — otherwise Lena is used)",
        type=["jpg", "jpeg", "png"]
    )

    image_np, source_message = load_image(uploaded_file)
    st.info(source_message,)


# ---------------- CONTROLS ---------------- #

noise_col, denoise_col_1, denoise_col_2 = st.columns(3, gap="small")


with noise_col:
    st.subheader("Noise Settings")

    noise_type = st.radio(
        "Select noise type",
        [
            "Gaussian grayscale noise",
            "Salt & pepper noise",
            "White grayscale noise"
        ]
    )

    if noise_type == "Gaussian grayscale noise":
        sigma = st.slider("Gaussian noise strength", 0, 100, 25)
        noisy_image = add_gaussian_noise_gray(image_np, sigma=sigma)

    elif noise_type == "Salt & pepper noise":
        amount = st.slider("Salt & pepper amount", 0.0, 0.20, 0.02, 0.01)
        noisy_image = add_salt_pepper_noise(image_np, amount=amount)

    else:
        strength = st.slider("White noise strength", 0, 100, 25)
        noisy_image = add_white_noise(image_np, strength=strength)


with denoise_col_1:
    st.subheader("Denoising Settings")

    method = st.radio(
        "Select denoising method",
        [
            "Mean Blur",
            "Gaussian Blur",
            "Median Filter",
            "Bilateral Filter",
            "Non-local Means"
        ]
    )


with denoise_col_2:
    st.subheader("Kernel Settings")

    if method == "Non-local Means":
        kernel_size = 3
        st.info("Non-local Means does not use kernel size.")
    else:
        kernel_size = st.radio(
            "Kernel size",
            [3, 5, 7, 9]
        )


# ---------------- PROCESS ---------------- #

denoised_image = apply_denoising(
    noisy_image,
    method,
    kernel_size
)

mse_value = mse(image_np, denoised_image)
psnr_value = psnr(image_np, denoised_image)

residual = compute_residual(image_np, denoised_image)
residual_view = amplify_residual(residual, factor=4)


# ---------------- MAIN COMPARISON ---------------- #

st.divider()
st.subheader("Comparison")

img1, img2, img3, metric_col = st.columns(
    [2.5, 2.5, 2.5, 1],
    gap="small"
)

with img1:
    st.markdown("### Original")
    st.write("No noise")
    st.image(image_np, use_container_width=True)

with img2:
    st.markdown("### Noisy")
    st.write(noise_type)
    st.image(noisy_image, use_container_width=True)

with img3:
    st.markdown("### Denoised")
    st.write(f"{method} ({kernel_size}x{kernel_size})")
    st.image(denoised_image, use_container_width=True)

with metric_col:
    st.markdown("### Metrics")

    st.metric("MSE", f"{mse_value:.2f}")
    st.metric("PSNR", f"{psnr_value:.2f} dB")

st.markdown("### Residual")

res_left, res_center, res_right = st.columns([1, 2, 1])

with res_left:
    st.image(
        residual_view,
        caption="Residual = Original - Denoised",
        use_container_width=True
    )

# ---------------- ZOOM CROP ---------------- #

st.divider()

crop_size = st.slider("Zoom crop size", 16, 256, 128, 8)

original_crop = resize_crop_for_display(
    get_zoom_crop(image_np, crop_size)
)

noisy_crop = resize_crop_for_display(
    get_zoom_crop(noisy_image, crop_size)
)

denoised_crop = resize_crop_for_display(
    get_zoom_crop(denoised_image, crop_size)
)

st.subheader("Zoom Crop Comparison")

crop1, crop2, crop3 = st.columns(3, gap="large")

with crop1:
    st.markdown("### Original Crop")
    st.image(original_crop, use_container_width=True)

with crop2:
    st.markdown("### Noisy Crop")
    st.image(noisy_crop, use_container_width=True)

with crop3:
    st.markdown("### Denoised Crop")
    st.image(denoised_crop, use_container_width=True)