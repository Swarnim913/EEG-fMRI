import os
import nibabel as nib
import numpy as np
from nilearn.image import resample_to_img, mean_img
from skimage.filters import threshold_otsu

# Set up paths
BIDS_DIR = "dataset/BIDS_dataset_MRI"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of subject IDs (Assuming subject IDs range from 1 to 20)
subject_ids = [f"sub-{i:03d}" for i in range(1, 21)]

# Scaling factor to adjust the OTSU threshold
threshold_scaling_factor = 2.5  # Increase this value to make the threshold stricter

# Preprocessing Loop for Each Subject
for subject_id in subject_ids:
    anat_file = os.path.join(BIDS_DIR, subject_id, 'ses-002', 'anat', f"{subject_id}_ses-002_acq-highres_T1w.nii.gz")
    func_file = os.path.join(BIDS_DIR, subject_id, 'ses-002', 'func', f"{subject_id}_ses-002_task-rest_bold.nii.gz")

    # Handle .nii extension if .nii.gz is not available
    if not os.path.exists(anat_file):
        anat_file = anat_file.replace(".nii.gz", ".nii")
    if not os.path.exists(func_file):
        func_file = func_file.replace(".nii.gz", ".nii")

    if not os.path.exists(anat_file) or not os.path.exists(func_file):
        print(f"Missing files for {subject_id}, skipping...")
        continue

    # Load anatomical and functional images
    anat_img = nib.load(anat_file)
    func_img = nib.load(func_file)

    # Calculate the mean functional image to use for identifying activation regions
    mean_func_img = mean_img(func_img)

    # Resample functional image to anatomical image space for better alignment
    resampled_func_img = resample_to_img(mean_func_img, anat_img, interpolation='linear')

    # Apply OTSU thresholding to the resampled functional image to identify high-activity areas
    resampled_func_data = resampled_func_img.get_fdata()
    otsu_threshold = threshold_otsu(resampled_func_data[resampled_func_data > 0])  # Calculate OTSU threshold
    adjusted_threshold = otsu_threshold * threshold_scaling_factor  # Adjust the threshold using scaling factor
    high_activity_mask = resampled_func_data > adjusted_threshold

    # Create a copy of the anatomical data to overlay with activation regions
    anat_data = anat_img.get_fdata()
    colored_anat_data = np.copy(anat_data)

    # Color the anatomical image with red (represented by setting high values) for high-activity regions
    colored_anat_data[high_activity_mask] = anat_data.max() * 1.5  # Highlight regions in red

    # Create a new NIfTI image with the colored anatomical data
    colored_anat_img = nib.Nifti1Image(colored_anat_data, anat_img.affine, anat_img.header)
    colored_anat_path = os.path.join(OUTPUT_DIR, f"{subject_id}_colored_anat.nii.gz")
    nib.save(colored_anat_img, colored_anat_path)

    # Save colored anatomical image
    print(f"Colored anatomical image saved for {subject_id} at {colored_anat_path}")

print("Processing Complete!")
