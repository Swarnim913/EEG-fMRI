import os
import shutil

# Set up paths
MRI_DIR = "dataset/BIDS_dataset_MRI"
OUTPUT_DIR = "anatomical_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of subject IDs (assuming they range from 1 to 20)
subject_ids = [f"sub-{i:03d}" for i in range(1, 21)]

# Iterate over subjects
for subject_id in subject_ids:
    anat_file = os.path.join(
        MRI_DIR, subject_id, 'ses-002', 'anat', f"{subject_id}_ses-002_acq-highres_T1w.nii.gz"
    )

    # Handle .nii extension if .nii.gz is not available
    if not os.path.exists(anat_file):
        anat_file = anat_file.replace(".nii.gz", ".nii")

    if not os.path.exists(anat_file):
        print(f"Anatomical MRI file not found for {subject_id}, skipping...")
        continue

    # Create a subfolder for the subject
    subject_output_dir = os.path.join(OUTPUT_DIR, subject_id)
    os.makedirs(subject_output_dir, exist_ok=True)

    # Copy the anatomical MRI file to the subject's folder
    destination_file = os.path.join(subject_output_dir, f"{subject_id}_T1w.nii.gz")
    shutil.copy(anat_file, destination_file)
    print(f"Copied {anat_file} to {destination_file}")

print("Anatomical MRI data organization complete!")