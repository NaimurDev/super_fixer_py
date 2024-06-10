import os
import shutil
from natsort import natsorted

def create_and_move_files(source_dir, dest_dir, files_per_group=30, total_groups=300):
    try:
        # Ensure the destination directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Get all .png files sorted naturally by name
        files = natsorted([f for f in os.listdir(source_dir) if f.lower().endswith('.png')])
        
        if len(files) < total_groups * files_per_group:
            print(f"Not enough files to fill {total_groups} groups with {files_per_group} files each.")
            return
        
        for group_num in range(1, total_groups + 1):
            group_folder = os.path.join(dest_dir, str(group_num))
            if not os.path.exists(group_folder):
                os.makedirs(group_folder)
            
            start_index = (group_num - 1) * files_per_group
            end_index = start_index + files_per_group
            group_files = files[start_index:end_index]
            
            for file in group_files:
                src_path = os.path.join(source_dir, file)
                dest_path = os.path.join(group_folder, file)
                shutil.move(src_path, dest_path)
        
        print(f"Successfully divided files into {total_groups} groups.")
    except FileNotFoundError:
        print("The specified source directory does not exist.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_directory = 'all-combines'
    destination_directory = 'typo-groups'
    create_and_move_files(source_directory, destination_directory)
