import os

def rename_files_and_folders(root_dir="."):  # Varsayılan olarak kök dizini kullan
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Dosyaları işle
        for name in files:
            old_path = os.path.join(root, name)
            new_name = name.lower().replace("_", "-")
            new_path = os.path.join(root, new_name)
            
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"✅ Renamed: {old_path} → {new_path}")
                except Exception as e:
                    print(f"❌ Error renaming {old_path}: {e}")

        # Klasörleri işle
        for name in dirs:
            old_path = os.path.join(root, name)
            new_name = name.lower().replace("_", "-")
            new_path = os.path.join(root, new_name)
            
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"✅ Renamed: {old_path} → {new_path}")
                except Exception as e:
                    print(f"❌ Error renaming {old_path}: {e}")

if __name__ == "__main__":
    print("🚀 Starting renaming process...")
    rename_files_and_folders()  # Kök dizini otomatik olarak "." alır
    print("✔️ Process completed.")
