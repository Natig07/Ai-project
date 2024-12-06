import os
from PIL import Image

# Paths to your dataset and the new resized dataset
data_path = "house_plant_species_split"  # Path containing train, val, test folders
new_data_path = "new_house_plant_species_split"

# List of splits: train, val, test
split_list = ["train", "val", "test"]

# Create the new dataset folder if it doesn't exist
if not os.path.exists(new_data_path):
    os.mkdir(new_data_path)

# Iterate over each split
for split in split_list:
    split_path = os.path.join(data_path, split)
    new_split_path = os.path.join(new_data_path, split)

    # Ensure the split folder exists in the new dataset
    if not os.path.exists(new_split_path):
        os.mkdir(new_split_path)

    # Process each class folder in the split
    folder_list = os.listdir(split_path)
    for folder in folder_list:
        class_path = os.path.join(split_path, folder)
        new_class_path = os.path.join(new_split_path, folder)

        # Ensure the class folder exists in the new dataset
        if not os.path.exists(new_class_path):
            os.mkdir(new_class_path)

        # Process each image in the class folder
        image_list = os.listdir(class_path)
        for image in image_list:
            img_path = os.path.join(class_path, image)
            new_img_path = os.path.join(new_class_path, image)

            try:
                # Open and resize the image
                img = Image.open(img_path)
                img = img.resize([224, 224])
                img.save(new_img_path)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

print("Preprocessing complete. Resized images saved in", new_data_path)
