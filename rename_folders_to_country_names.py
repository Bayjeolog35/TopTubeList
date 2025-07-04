import os

def safe_rename(old_path, new_path):
    """Hedef yol yoksa yeniden adlandırma yapar."""
    if old_path != new_path and not os.path.exists(new_path):
        os.rename(old_path, new_path)

def rename_all(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Dosyaları yeniden adlandır
        for filename in files:
            old_path = os.path.join(root, filename)
            new_filename = filename.lower().replace("_", "-")
            new_path = os.path.join(root, new_filename)
            safe_rename(old_path, new_path)

        # Klasörleri yeniden adlandır
        for dirname in dirs:
            old_dir = os.path.join(root, dirname)
            new_dirname = dirname.lower().replace("_", "-")
            new_dir = os.path.join(root, new_dirname)
            safe_rename(old_dir, new_dir)

if __name__ == "__main__":
    base_folder = "."  # Tüm repo içinde çalışır
    rename_all(base_folder)
    print("✔️ Dosya ve klasör isimleri dönüştürüldü.")
