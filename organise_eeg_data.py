import os
import shutil

# Paths
EEG_DIR = "dataset/BIDS_dataset_EEG"
TRIALS_DIR = "training_data"
os.makedirs(TRIALS_DIR, exist_ok=True)

# Iterate over subjects
for i in range(1, 21):
    subject_id = f"sub-{i:03d}"  # sub-001 to sub-020
    trial_folder = os.path.join(TRIALS_DIR, f"trial_{i}")
    os.makedirs(trial_folder, exist_ok=True)

    eeg_sub_folder = os.path.join(EEG_DIR, subject_id, 'eeg')

    if not os.path.exists(eeg_sub_folder):
        print(f"EEG data folder does not exist for {subject_id}, skipping...")
        continue

    # List all EEG files in the subject's EEG folder
    eeg_files = os.listdir(eeg_sub_folder)

    # Find all resting EEG data files (both 'ec' and 'eo' if needed)
    resting_prefixes = []
    for prefix in ['fmrirestingec', 'fmrirestingeo']:
        # Construct the filename pattern
        pattern = f"{subject_id}_task-{prefix}_eeg."
        # Check if any files match this pattern
        matching_files = [f for f in eeg_files if f.startswith(pattern)]
        if matching_files:
            resting_prefixes.append(f"sub-{i:03d}_task-{prefix}_eeg")

    if not resting_prefixes:
        print(f"No resting EEG data found for {subject_id}, skipping...")
        continue

    # Copy the resting EEG data files to the trial folder
    for prefix in resting_prefixes:
        for extension in ['set', 'fdt', 'json', 'edf', 'vhdr', 'vmrk']:  # Add other extensions if needed
            filename = f"{prefix}.{extension}"
            src_file = os.path.join(eeg_sub_folder, filename)
            if os.path.exists(src_file):
                dst_file = os.path.join(trial_folder, filename)
                shutil.copy(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")

print("EEG data organization complete!")