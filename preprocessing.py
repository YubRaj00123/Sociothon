import nibabel as nib
import numpy as np
from skimage import exposure, filters, morphology, transform
import matplotlib.pyplot as plt
import SimpleITK as sitk
from PIL import Image
import cv2

# --- LOADING FUNCTIONS ---

def load_image(image_path):
    if image_path.endswith('.nii') or image_path.endswith('.nii.gz'):
        return load_mri_image(image_path)
    elif image_path.endswith('.jpg') or image_path.endswith('.png') or image_path.endswith('.jpeg'):
        return load_jpg_image(image_path)
    else:
        raise ValueError("Unsupported file format. Only .nii, .jpg, .png, and .jpeg are supported.")

def load_mri_image(image_path):
    mri_image = nib.load(image_path)
    return mri_image.get_fdata()

def load_jpg_image(image_path):
    # Open the image with PIL and convert to grayscale (assuming it's color)
    img = Image.open(image_path).convert('L')  # 'L' mode is for grayscale
    img_array = np.array(img)
    return img_array

# --- IMAGE PREPROCESSING FUNCTIONS ---

def normalize_image(image):
    normalized_image = exposure.rescale_intensity(image, in_range='image', out_range=(0, 1))
    return normalized_image

def denoise_image(image, sigma=1):
    denoised_image = filters.gaussian(image, sigma=sigma)
    return denoised_image

def skull_strip(image):
    binary_mask = image > np.mean(image)
    cleaned_mask = morphology.binary_closing(binary_mask, selem=morphology.ball(3))
    skull_stripped_image = image * cleaned_mask
    return skull_stripped_image

def resize_image(image, target_size):
    return transform.resize(image, target_size, mode='constant', anti_aliasing=True)

def augment_image(image):
    rotated_image = transform.rotate(image, angle=np.random.uniform(-30, 30), mode='wrap')
    flipped_image = np.fliplr(rotated_image)
    return flipped_image

# --- IMAGE VISUALIZATION FUNCTIONS ---

def visualize_image(image, title="Image Slice"):
    plt.figure(figsize=(8, 8))
    if image.ndim == 3:  # If it's a 3D MRI image
        plt.imshow(image[:, :, image.shape[2] // 2], cmap='gray')
    else:  # If it's a 2D image like .jpg/.png
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def compute_histogram(image):
    plt.hist(image.ravel(), bins=256, histtype='step', color='black')
    plt.title('Intensity Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.show()

# --- MAIN PREPROCESSING FUNCTION ---

def preprocess_image(image_path, target_size=(128, 128, 128)):
    image_data = load_image(image_path)
    
    normalized_image = normalize_image(image_data)
    denoised_image = denoise_image(normalized_image)
    
    if image_data.ndim == 3:  # If MRI (3D)
        skull_stripped_image = skull_strip(denoised_image)
    else:  # If 2D image like .jpg/.png
        skull_stripped_image = denoised_image  # No skull stripping for 2D images
    
    resized_image = resize_image(skull_stripped_image, target_size)
    augmented_image = augment_image(resized_image)
    
    # Visualize the results
    visualize_image(image_data, title="Original Image")
    visualize_image(augmented_image, title="Augmented Image")
    compute_histogram(skull_stripped_image)

    return augmented_image

# Example usage (comment out for the main Flask app):
# image_path = 'C:/path/to/image.jpg'  # Example for jpg
# preprocess_image(image_path)
