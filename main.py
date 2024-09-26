import nibabel as nib
import numpy as np
from skimage import exposure, filters, morphology
import matplotlib.pyplot as plt
from compare_result import compare_results
from mlmodel import get_segmentation

def load_mri_image(image_path):
    mri_image = nib.load(image_path)
    return mri_image.get_fdata()

def normalize_image(image):
    return exposure.rescale_intensity(image, in_range='image', out_range=(0, 1))

def denoise_image(image, sigma=1):
    return filters.gaussian(image, sigma=sigma)

def skull_strip(image):
    binary_mask = image > np.mean(image)
    cleaned_mask = morphology.binary_closing(binary_mask, selem=morphology.ball(3))
    return image * cleaned_mask

def augment_image(image):
    rotated_image = transform.rotate(image, angle=np.random.uniform(-30, 30), mode='wrap')
    flipped_image = np.fliplr(rotated_image)
    return flipped_image

def preprocess_mri_image(image_path):
    mri_data = load_mri_image(image_path)
    normalized_mri = normalize_image(mri_data)
    denoised_mri = denoise_image(normalized_mri)
    skull_stripped_mri = skull_strip(denoised_mri)
    return skull_stripped_mri, mri_data

def main(image_path):
    skull_stripped_mri, original_mri = preprocess_mri_image(image_path)
    predicted_mask, ground_truth_mask = get_segmentation(skull_stripped_mri)
    compare_results(predicted_mask, ground_truth_mask, original_mri)

if __name__ == "__main__":
    image_path = 'path/to/mymri.nii'
    main(image_path)
