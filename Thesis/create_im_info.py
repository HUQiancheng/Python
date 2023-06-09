import os
import csv

def save_image_info_to_csv(csv_file_path):
    """
    This function saves image information to a CSV file. It reads the Images folder and its subfolders to get the file paths of all the JPG images, and then saves the file paths and their corresponding categories to the CSV file.

    Args:
        csv_file_path (str): The file path of the CSV file to save the image information to.

    Returns:
        None
    """
    # Get the path to the Images folder
    images_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Images')

    # Create a list to store the image information
    image_info_list = []

    # Loop through each subfolder in the Images folder
    for entry in os.scandir(images_folder_path):
        if entry.is_dir():
            category_folder_name = entry.name
            category_folder_path = os.path.join(images_folder_path, category_folder_name)

            # Loop through each JPG file in the subfolder
            for file_name in os.listdir(category_folder_path):
                if file_name.endswith('.jpg'):
                    file_path = os.path.join(category_folder_path, file_name)

                    # Add the file path and category to the image information list
                    image_info_list.append([file_path, category_folder_name])

    # Write the image information list to the CSV file
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(image_info_list)