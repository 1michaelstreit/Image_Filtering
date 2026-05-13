
import numpy as np

# Metrics for image quality assessment
# Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR)
def mse(image_a, image_b):
    diff = image_a.astype(np.float32) - image_b.astype(np.float32)
    return np.mean(diff ** 2)

# PSNR is derived from MSE and gives a more interpretable measure of image quality
def psnr(image_a, image_b):
    mse_value = mse(image_a, image_b)

    if mse_value == 0:
        return float("inf")

    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse_value))