import os
import re

def rename_files_and_folders(root_dir):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Önce dosyaları işle
        for name in files:
            old_path = os.path.join(root, name)
            new_name = name.lower().replace('_', '-')
            new_path = os.path.join(root, new_name)
            
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming file {old_path}: {e}")
        
        # Sonra klasörleri işle
        for name in dirs:
            old_path = os.path.join(root, name)
            new_name = name.lower().replace('_', '-')
            new_path = os.path.join(root, new_name)
            
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed folder: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming folder {old_path}: {e}")

if __name__ == "__main__":
    root_directory = input("Enter the root directory path: ").strip()
    
    if os.path.isdir(root_directory):
        rename_files_and_folders(root_directory)
        print("Renaming process completed.")
    else:
        print("Invalid directory path. Please provide a valid directory.")
