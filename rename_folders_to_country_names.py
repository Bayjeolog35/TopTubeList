import os
import shutil
from country_data import COUNTRY_INFO

def rename_folders():
    for country_folder, info in COUNTRY_INFO.items():
        display_name = info.get("display_name", country_folder.replace('_', ' '))
        
        # Eski ve yeni klasör yolları (küçük harf ve boşlukları tireye çevirme)
        old_path = os.path.join(os.getcwd(), country_folder)
        new_folder_name = display_name.lower().replace(' ', '-')
        new_path = os.path.join(os.getcwd(), new_folder_name)
        
        if os.path.exists(old_path):
            # Klasörü yeniden adlandır
            shutil.move(old_path, new_path)
            print(f"Renamed: {country_folder} → {new_folder_name}")
        else:
            print(f"Folder not found: {country_folder}, creating new...")
            os.makedirs(new_path, exist_ok=True)

if __name__ == "__main__":
    rename_folders()
