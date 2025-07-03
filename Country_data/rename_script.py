import os
import re

def standardize_filename(filename):
    """
    Verilen dosya adını 'videos_Ulke_Adi.json' veya 'structured_data_Ulke_Adi.json' gibi bir formatdan,
    'videos-ulke-adi.json' veya 'structured-data-ulke-adi.json' formatına dönüştürür.
    """
    # Bilinen önekleri ve ardından ülke adını (veya dosyanın geri kalanını) ve .json uzantısını yakalayan regex.
    # Büyük/küçük harf duyarlılığı için re.IGNORECASE kullanılır.
    # Örn: "videos_United_States.json" -> "videos", "United_States.json"
    # Örn: "structured_data_Afghanistan.json" -> "structured_data", "Afghanistan.json"
    match = re.match(r"(videos|structured_data)_(.*\.json)$", filename, re.IGNORECASE)

    if not match:
        # Eğer dosya adı beklenen desenle eşleşmiyorsa, yeniden adlandırmayız.
        return None

    prefix_base = match.group(1).lower() # "videos" veya "structured_data" (küçük harfe çevrildi)
    # İlk alt çizgiden sonraki tüm kısmı yakalar, .json uzantısı dahil.
    rest_of_filename = match.group(2) # Örn: "United_States.json" veya "Afghanistan.json"

    # Dosya adının geri kalanını küçük harfe çevir ve alt çizgileri tireye dönüştür.
    sanitized_rest = rest_of_filename.lower().replace("_", "-")

    # "structured_data" öneki için özel durum: "structured-data" olmalı.
    if prefix_base == "structured_data":
        new_prefix = "structured-data"
    else: # Bu, "videos" önekini kapsar
        new_prefix = prefix_base

    # Yeni dosya adını oluştur
    new_filename = f"{new_prefix}-{sanitized_rest}"

    return new_filename

def rename_files_to_standard_format(directory):
    """
    Belirtilen dizindeki JSON dosyalarını standartlaştırılmış formata yeniden adlandırır:
    'videos_UlkeAdi.json' -> 'videos-ulkeadi.json'
    'structured_data_UlkeAdi.json' -> 'structured-data-ulkeadi.json'
    Dosya adındaki ülke kısmındaki büyük harfleri küçük harfe çevirir ve alt çizgileri tireye dönüştürür.
    """
    print(f"'{directory}' dizini taranıyor ve dosyalar yeniden adlandırılıyor...")
    renamed_count = 0
    skipped_count = 0

    for filename in os.listdir(directory):
        old_filepath = os.path.join(directory, filename)

        # Sadece dosyaları işle, dizinleri atla
        if not os.path.isfile(old_filepath):
            continue

        # Yeni dosya adını al
        new_filename = standardize_filename(filename)

        if new_filename and new_filename != filename:
            # Eğer yeni bir isim varsa ve eski isimden farklıysa yeniden adlandır
            new_filepath = os.path.join(directory, new_filename)
            try:
                os.rename(old_filepath, new_filepath)
                print(f"Yeniden adlandırıldı: '{filename}' -> '{new_filename}'")
                renamed_count += 1
            except OSError as e:
                print(f"Hata: '{filename}' yeniden adlandırılamadı -> '{new_filename}'. Hata: {e}")
        elif new_filename is None:
            # Desenle eşleşmeyen dosyaları atla
            skipped_count += 1
            # print(f"Atlandı (beklenen desenle eşleşmedi): '{filename}'") # Hata ayıklama için açılabilir
        else:
            # Dosya zaten doğru formatta ise atla
            skipped_count += 1
            # print(f"Atlandı (zaten doğru formatta): '{filename}'") # Hata ayıklama için açılabilir

    print(f"\nİşlem tamamlandı. Yeniden adlandırılan dosya sayısı: {renamed_count}, Atlanan dosya sayısı: {skipped_count}")

if __name__ == "__main__":
    # Hedef dizini burada belirtin.
    # Eğer bu betik, 'Country_data' ile aynı seviyede çalışıyorsa, yol doğru olacaktır.
    target_directory = "Country_data/videos"

    # Dizin mevcut değilse kullanıcıyı bilgilendir
    if not os.path.isdir(target_directory):
        print(f"Hata: '{target_directory}' dizini bulunamadı.")
        print("Lütfen script'i çalıştırmadan önce bu dizini oluşturduğunuzdan veya doğru yolu ayarladığınızdan emin olun.")
    else:
        rename_files_to_standard_format(target_directory)
