import numpy as np
import cv2


def add_gaussian_noise_gray(image, mean=0, sigma=25):
    noise = np.random.normal(mean, sigma, image.shape[:2])
    noise = noise[:, :, np.newaxis]

    noisy = image.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_salt_pepper_noise(image, amount=0.02):
    noisy = image.copy()
    h, w = image.shape[:2]

    num_pixels = int(amount * h * w)

    salt_coords = (
        np.random.randint(0, h, num_pixels),
        np.random.randint(0, w, num_pixels)
    )
    noisy[salt_coords[0], salt_coords[1]] = [255, 255, 255]

    pepper_coords = (
        np.random.randint(0, h, num_pixels),
        np.random.randint(0, w, num_pixels)
    )
    noisy[pepper_coords[0], pepper_coords[1]] = [0, 0, 0]

    return noisy


def add_white_noise(image, strength=25):
    noise = np.random.randint(
        -strength,
        strength + 1,
        image.shape[:2]
    )
    noise = noise[:, :, np.newaxis]

    noisy = image.astype(np.int16) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def apply_denoising(image, method, kernel_size):
    if method == "Mean Blur":
        return cv2.blur(image, (kernel_size, kernel_size))

    if method == "Gaussian Blur":
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    if method == "Median Filter":
        return cv2.medianBlur(image, kernel_size)

    if method == "Bilateral Filter":
        return cv2.bilateralFilter(image, kernel_size, 75, 75)

    if method == "Non-local Means":
        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=10,
            hColor=10,
            templateWindowSize=7,
            searchWindowSize=21
        )

    return image

def compute_residual(image_a, image_b):
    """
    Absolute difference between two images.
    Example: original vs denoised, or noisy vs denoised.
    """
    return cv2.absdiff(image_a, image_b)


def amplify_residual(residual, factor=4):
    """
    Makes small residual differences easier to see.
    """
    amplified = residual.astype(np.float32) * factor
    return np.clip(amplified, 0, 255).astype(np.uint8)


def get_zoom_crop(image, crop_size=128):
    """
    Returns a centered crop from the image.
    """
    h, w = image.shape[:2]

    center_y = h // 2
    center_x = w // 2

    half = crop_size // 2

    y1 = max(center_y - half, 0)
    y2 = min(center_y + half, h)

    x1 = max(center_x - half, 0)
    x2 = min(center_x + half, w)

    return image[y1:y2, x1:x2]


def resize_crop_for_display(crop, scale=3):
    """
    Enlarges crop for easier comparison.
    """
    h, w = crop.shape[:2]

    return cv2.resize(
        crop,
        (w * scale, h * scale),
        interpolation=cv2.INTER_NEAREST
    )