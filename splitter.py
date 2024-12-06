import os
import shutil
from sklearn.model_selection import train_test_split

def split_dataset(root, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    # Ensure ratios sum to 1
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1."

    # Clear and recreate output directories
    for split in ["train", "val", "test"]:
        split_dir = os.path.join(output_dir, split)
        if os.path.exists(split_dir):
            shutil.rmtree(split_dir)  # Delete existing folder
        os.makedirs(split_dir)

    # Iterate over each class folder in the root directory
    for class_name in sorted(os.listdir(root)):
        class_path = os.path.join(root, class_name)
        if not os.path.isdir(class_path):
            continue  # Skip non-directory files

        # List all images in the class folder
        images = [os.path.join(class_path, img) for img in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, img))]

        # Split into train, val, and test sets
        train_imgs, temp_imgs = train_test_split(images, test_size=(val_ratio + test_ratio), random_state=seed, shuffle=True)
        val_imgs, test_imgs = train_test_split(temp_imgs, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=seed, shuffle=True)

        # Create subdirectories for the current class in train, val, and test folders
        for split_name, split_imgs in zip(["train", "val", "test"], [train_imgs, val_imgs, test_imgs]):
            split_class_dir = os.path.join(output_dir, split_name, class_name)
            os.makedirs(split_class_dir, exist_ok=True)
            for img_path in split_imgs:
                shutil.copy(img_path, split_class_dir)

    print(f"Dataset successfully split and saved to {output_dir}.")


root = "house_plant_species"  # Path to your unsplit dataset
output_dir = "house_plant_species_split"  # Path to save the split dataset
split_dataset(root, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)

def verify_split(output_dir):
    splits = ["train", "val", "test"]
    file_sets = {split: set() for split in splits}

    # Collect file names from each split
    for split in splits:
        split_dir = os.path.join(output_dir, split)
        for class_name in os.listdir(split_dir):
            class_dir = os.path.join(split_dir, class_name)
            if os.path.isdir(class_dir):
                file_sets[split].update([os.path.join(class_name, fname) for fname in os.listdir(class_dir)])

    # Check for overlaps
    for i, split_a in enumerate(splits):
        for split_b in splits[i+1:]:
            intersection = file_sets[split_a] & file_sets[split_b]
            if intersection:
                print(f"Overlapping data found between {split_a} and {split_b}: {intersection}")
                return False

    print("No overlap detected between train, val, and test splits.")
    return True


verify_split(output_dir)