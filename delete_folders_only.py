import os
import shutil

def delete_folders_in_repo(repo_path):
    for item in os.listdir(repo_path):
        item_path = os.path.join(repo_path, item)
        if os.path.isdir(item_path):
            print(f"Deleting folder: {item_path}")
            shutil.rmtree(item_path)

if __name__ == "__main__":
    repo_path = os.getcwd()  # Çalıştırıldığı klasör
    delete_folders_in_repo(repo_path)
    print("Tüm klasörler silindi.")
