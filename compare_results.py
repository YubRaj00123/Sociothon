import numpy as np
    from skimage.metrics import adapted_rand_error
    from scipy.spatial.distance import directed_hausdorff
    import matplotlib.pyplot as plt
    from sklearn.metrics import jaccard_score

    def dice_coefficient(predicted_mask, ground_truth):
        intersection = np.sum(predicted_mask[ground_truth == 1])
        return (2 * intersection) / (np.sum(predicted_mask) + np.sum(ground_truth))

    def jaccard_index(predicted_mask, ground_truth):
        intersection = np.logical_and(predicted_mask, ground_truth)
        union = np.logical_or(predicted_mask, ground_truth)
        return np.sum(intersection) / np.sum(union) if np.sum(union) != 0 else 0

    def hausdorff_distance(predicted_mask, ground_truth):
        u = np.argwhere(predicted_mask)
        v = np.argwhere(ground_truth)
        forward_hd = directed_hausdorff(u, v)[0]
        backward_hd = directed_hausdorff(v, u)[0]
        return max(forward_hd, backward_hd)

    def plot_segmentation_results(predicted_mask, ground_truth, image, slice_idx):
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        ax[0].imshow(image[:, :, slice_idx], cmap='gray')
        ax[0].set_title('Original MRI Slice')
        ax[0].axis('off')

        ax[1].imshow(predicted_mask[:, :, slice_idx], cmap='Reds', alpha=0.5)
        ax[1].set_title('Predicted Mask')
        ax[1].axis('off')

        ax[2].imshow(ground_truth[:, :, slice_idx], cmap='Blues', alpha=0.5)
        ax[2].set_title('Ground Truth Mask')
        ax[2].axis('off')

        plt.show()

    def compare_results(predicted_mask, ground_truth, image):
        if predicted_mask.shape != ground_truth.shape:
            raise ValueError("Predicted mask and ground truth must have the same shape.")

        dice = dice_coefficient(predicted_mask, ground_truth)
        jaccard = jaccard_index(predicted_mask, ground_truth)
        hausdorff = hausdorff_distance(predicted_mask, ground_truth)

        print(f"Dice Coefficient: {dice:.4f}")
        print(f"Jaccard Index (IoU): {jaccard:.4f}")
        print(f"Hausdorff Distance: {hausdorff:.4f}")

        slice_idx = predicted_mask.shape[2] // 2
        plot_segmentation_results(predicted_mask, ground_truth, image, slice_idx)

        return dice, jaccard, hausdorff