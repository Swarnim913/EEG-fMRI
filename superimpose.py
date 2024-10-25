import os
import nibabel as nib
from nilearn.image import resample_to_img, mean_img, threshold_img
from nilearn.plotting import plot_anat, plot_stat_map

# Set up paths
BIDS_DIR = "dataset/BIDS_dataset_MRI"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of subject IDs (Assuming subject IDs range from 1 to 20)
subject_ids = [f"sub-{i:03d}" for i in range(1, 21)]

# Preprocessing Loop for Each Subject
for subject_id in subject_ids:
    anat_file = os.path.join(BIDS_DIR, subject_id, 'ses-001', 'anat', f"{subject_id}_ses-001_acq-highres_T1w.nii.gz")
    func_file = os.path.join(BIDS_DIR, subject_id, 'ses-001', 'func', f"{subject_id}_ses-001_task-eoec_bold.nii.gz")

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

    # Calculate the mean functional image to use for coregistration
    mean_func_img = mean_img(func_img)

    # Threshold the functional image to keep only the red regions (positive activation)
    thresholded_func_img = threshold_img(mean_func_img, threshold=2.0)  # Increased threshold value to reduce whitened areas

    # Resample functional image to anatomical image space
    resampled_func_img = resample_to_img(thresholded_func_img, anat_img, interpolation='linear')
    resampled_func_path = os.path.join(OUTPUT_DIR, f"{subject_id}_resampled_func.nii.gz")
    resampled_func_img.to_filename(resampled_func_path)

    # Save resampled functional image
    print(f"Resampled functional image saved for {subject_id} at {resampled_func_path}")

    # Visualization of only the red parts (positive activation)
    print(f"Visualizing {subject_id} data...")
    plot_anat(anat_img, title=f"{subject_id} Anatomical Image")
    plot_stat_map(resampled_func_img, bg_img=anat_img, title=f"{subject_id} Functional (Red Regions) on Anatomical", threshold=2.0)

print("Processing Complete!")
