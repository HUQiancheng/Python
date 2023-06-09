import os
import create_im_info as cii

def main():
    # Get the file path of the current script and the root folder path
    current_file_path = os.path.abspath(__file__)
    root_folder_path = os.path.dirname(os.path.dirname(current_file_path))
    
    # Get the path to the Images folder and the CSV file
    images_folder_path = os.path.join(root_folder_path, 'Thesis', 'Images')
    csv_file_path = os.path.join(images_folder_path, 'file.csv')
    
    # Create the CSV file if it doesn't exist and save image information to it
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w') as f:
            f.write('Header1,Header2,Header3\n')
    cii.save_image_info_to_csv(csv_file_path)

if __name__ == '__main__':
    main()