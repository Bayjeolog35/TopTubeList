import os

def replace_underscores_with_hyphens(root_dir):
    """
    Belirtilen kök dizindeki tüm dosya ve klasör adlarındaki
    alt çizgileri (_) kısa çizgilere (-) dönüştürür.
    """
    print(f"'{root_dir}' dizinindeki dosya ve klasör adlarında alt çizgiler kısa çizgilere dönüştürülüyor...")

    # Klasörleri yeniden adlandırmak için ters sıralamada gezmek daha güvenlidir
    # çünkü üst klasörler yeniden adlandırılırsa alt klasörlerin yolu değişir.
    # Ancak burada sadece dosya adlarını hedeflediğimiz ve os.walk'un davranışı nedeniyle
    # en basit yolu kullanacağız: dosyaları ve sonra klasörleri (içeridekileri gezmeden önce).

    # İlk olarak klasörleri yeniden adlandır (içeriğine girmeden önce)
    # Bu adım kritik, çünkü os.walk'un çalışmasını etkileyecektir.
    # En güvenli yol, os.walk'un oluşturduğu listeleri kopyalayıp işlemektir.
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False): # topdown=False ile en içten başla
        # Dosyaları yeniden adlandır
        for filename in filenames:
            if '_' in filename:
                old_filepath = os.path.join(dirpath, filename)
                new_filename = filename.replace('_', '-')
                new_filepath = os.path.join(dirpath, new_filename)
                try:
                    os.rename(old_filepath, new_filepath)
                    print(f"Dosya yeniden adlandırıldı: '{old_filepath}' -> '{new_filepath}'")
                except OSError as e:
                    print(f"Hata: '{old_filepath}' yeniden adlandırılamadı. Hata: {e}")

        # Klasörleri yeniden adlandır
        # dirnames listesi, o anki dirpath'in alt klasörlerini içerir.
        # Bu listeyi doğrudan değiştirmemiz gerekiyor, yoksa os.walk bir sonraki adımda yanlış yere gider.
        for i in range(len(dirnames)):
            dirname = dirnames[i]
            if '_' in dirname:
                old_dirpath = os.path.join(dirpath, dirname)
                new_dirname = dirname.replace('_', '-')
                new_dirpath = os.path.join(dirpath, new_dirname)
                
                try:
                    os.rename(old_dirpath, new_dirpath)
                    print(f"Klasör yeniden adlandırıldı: '{old_dirpath}' -> '{new_dirpath}'")
                    # os.walk'un sonraki adımlarını doğru yöne çekmek için dirnames listesini güncelle
                    dirnames[i] = new_dirname
                except OSError as e:
                    print(f"Hata: '{old_dirpath}' yeniden adlandırılamadı. Hata: {e}")

    print("\nAlt çizgi (_) dönüştürme işlemi tamamlandı.")


if __name__ == "__main__":
    # Bu betik, çalıştırıldığı dizini kök dizin olarak kabul edecektir.
    # Yani, eğer rename-files.py dosyasını 'toptubelist' klasörünün içine koyduysanız,
    # 'toptubelist' klasörü ve içindeki her şey işlenecektir.
    target_root_directory = os.path.dirname(os.path.abspath(__file__))

    print(f"\n--- '{target_root_directory}' dizini ve altındaki öğeler işleniyor ---")
    replace_underscores_with_hyphens(target_root_directory)
    print("\n--- İşlem tamamlandı ---")
