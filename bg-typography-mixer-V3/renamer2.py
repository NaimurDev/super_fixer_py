import os
import shutil
from natsort import natsorted

def move_and_rename_files(source_dir, dest_dir):
    try:
        # Ensure the destination directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        subdirs = natsorted([d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))])
        current_num = 1

        for subdir in subdirs:
            subdir_path = os.path.join(source_dir, subdir)
            files = natsorted([f for f in os.listdir(subdir_path) if f.lower().endswith('.png')])

            for file in files:
                src_path = os.path.join(subdir_path, file)
                dest_path = os.path.join(dest_dir, f"{current_num}.png")
                shutil.move(src_path, dest_path)
                current_num += 1

        print(f"Successfully moved and renamed files to {dest_dir}.")
    except FileNotFoundError:
        print("The specified source directory or one of the subdirectories does not exist.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_directory = 'downloaded-typos'
    destination_directory = 'all-combines'
    move_and_rename_files(source_directory, destination_directory)
