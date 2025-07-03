import os
import re

def standardize_filename(filename):
    """
    'structured_data_Ulke_Adi.json' formatındaki dosya adını
    'structured-data-ulke-adi.json' formatına dönüştürür.
    """
    match = re.match(r"(structured_data)_(.*\.json)$", filename, re.IGNORECASE)

    if not match:
        return None

    prefix_base = match.group(1).lower()  # "structured_data"
    rest_of_filename = match.group(2)     # "Afghanistan.json" gibi

    sanitized_rest = rest_of_filename.lower().replace("_", "-")
    new_prefix = "structured-data"

    new_filename = f"{new_prefix}-{sanitized_rest}"
    return new_filename

def rename_files_to_standard_format(directory):
    """
    Belirtilen dizindeki structured_data_*.json dosyalarını yeniden adlandırır.
    """
    print(f"'{directory}' dizini taranıyor ve dosyalar yeniden adlandırılıyor...")
    renamed_count = 0
    skipped_count = 0

    for filename in os.listdir(directory):
        old_filepath = os.path.join(directory, filename)

        if not os.path.isfile(old_filepath):
            continue

        new_filename = standardize_filename(filename)

        if new_filename and new_filename != filename:
            new_filepath = os.path.join(directory, new_filename)
            try:
                os.rename(old_filepath, new_filepath)
                print(f"Yeniden adlandırıldı: '{filename}' -> '{new_filename}'")
                renamed_count += 1
            except OSError as e:
                print(f"Hata: '{filename}' yeniden adlandırılamadı -> '{new_filename}'. Hata: {e}")
        else:
            skipped_count += 1

    print(f"\nİşlem tamamlandı. Yeniden adlandırılan dosya sayısı: {renamed_count}, Atlanan dosya sayısı: {skipped_count}")

if __name__ == "__main__":
    target_directory = "Country_data/structured_data"

    print(f"\n--- '{target_directory}' dizini işleniyor ---")
    if not os.path.isdir(target_directory):
        print(f"Hata: '{target_directory}' dizini bulunamadı.")
        print("Lütfen script'i çalıştırmadan önce bu dizini oluşturduğunuzdan emin olun.")
    else:
        rename_files_to_standard_format(target_directory)

    print("\n--- structured_data dizinindeki dosya adı standardizasyonu tamamlandı ---")
