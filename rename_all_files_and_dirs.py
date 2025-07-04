import os

def rename_all(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Dosyaları yeniden adlandır
        for filename in files:
            old_path = os.path.join(root, filename)
            new_filename = filename.lower().replace("_", "-")
            new_path = os.path.join(root, new_filename)
            if old_path != new_path:
                os.rename(old_path, new_path)

        # Klasörleri yeniden adlandır
        for dirname in dirs:
            old_dir = os.path.join(root, dirname)
            new_dirname = dirname.lower().replace("_", "-")
            new_dir = os.path.join(root, new_dirname)
            if old_dir != new_dir:
                os.rename(old_dir, new_dir)

if __name__ == "__main__":
    base_folder = "."  # Mevcut klasör, istersen değiştir: örn: "Country_data"
    rename_all(base_folder)
    print("Tüm dosya ve klasör isimleri küçük harfe dönüştürüldü ve _ → - değiştirildi.")
