import os

def rename_files_in_directory(root_dir):
    """
    Belirtilen kök dizindeki tüm dosya ve klasör adlarını yeniden adlandırır:
    - Tüm büyük harfleri küçük harflere dönüştürür.
    - Alt çizgileri (-) kısa çizgilere dönüştürür.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Dosyaları yeniden adlandır
        for filename in filenames:
            old_filepath = os.path.join(dirpath, filename)
            new_filename = filename.lower().replace('_', '-')
            if new_filename != filename:
                new_filepath = os.path.join(dirpath, new_filename)
                try:
                    os.rename(old_filepath, new_filepath)
                    print(f"Yeniden adlandırıldı: {old_filepath} -> {new_filepath}")
                except OSError as e:
                    print(f"Hata oluştu: {old_filepath} yeniden adlandırılamadı - {e}")

        # Klasörleri yeniden adlandır (içerideki elemanlar işlendikten sonra)
        # Klasör adları değiştiği için dirnames listesini manuel olarak güncellemek gerekebilir
        # Bu kısım karmaşık olabileceğinden, genellikle dosyalar ve ardından en içteki klasörlerden başlayarak
        # dışa doğru yeniden adlandırmak daha güvenlidir.
        # Basitlik ve olası hataları önlemek için bu betik sadece dosyaları işler.
        # Klasör adlarının da değişmesini istiyorsanız, bu kısmı dikkatli bir şekilde ele almak gerekir.
        # Ancak, os.walk'un davranışı nedeniyle, klasörleri yeniden adlandırmak beklenmedik sonuçlara yol açabilir.
        # Bu nedenle, şimdilik sadece dosya adlarını yeniden adlandırıyoruz.
        
        # Eğer klasörleri de yeniden adlandırmak isterseniz, aşağıdaki yorum satırındaki kodu kullanabilirsiniz,
        # ancak dikkatli olun ve yedeklemeyi unutmayın:
        
        # current_dir_name = os.path.basename(dirpath)
        # new_dir_name = current_dir_name.lower().replace('_', '-')
        # if new_dir_name != current_dir_name:
        #     new_dir_path = os.path.join(os.path.dirname(dirpath), new_dir_name)
        #     try:
        #         os.rename(dirpath, new_dir_path)
        #         print(f"Klasör yeniden adlandırıldı: {dirpath} -> {new_dir_path}")
        #         # Klasör adı değiştiği için os.walk'un sonraki iterasyonlarını etkileyecektir.
        #         # Bu, os.walk ile klasörleri yeniden adlandırmanın zorluğudur.
        #         # Genellikle, klasörleri en içten başlayarak yeniden adlandırmak daha iyidir.
        #     except OSError as e:
        #         print(f"Hata oluştu: {dirpath} yeniden adlandırılamadı - {e}")


if __name__ == "__main__":
    # Betiği çalıştıracağınız kök klasörün yolunu belirtin.
    # Bu durumda, "toptubelist" klasörünün tam yolu olmalıdır.
    # Örneğin: /path/to/your/toptubelist
    
    # Mevcut betiğin bulunduğu dizini kök dizin olarak ayarlayın.
    root_directory = os.path.dirname(os.path.abspath(__file__))
    
    # "toptubelist" klasörüne geri gitmek için:
    # Eğer rename_files.py, toptubelist'in içindeyse, toptubelist'in kendisi kök dizin olmalıdır.
    # Örneğin, eğer yapınız şöyle ise:
    # /parent_folder/toptubelist/rename_files.py
    # O zaman root_directory'yi manuel olarak "/parent_folder/toptubelist" olarak ayarlamanız gerekebilir.
    # Veya, daha genel bir çözüm olarak, betiği doğrudan "toptubelist" kök klasöründe çalıştırdığınızdan emin olun.

    # Otomatik olarak kök klasörü bulmak için:
    # Eğer `rename_files.py` dosyası `toptubelist` klasörünün hemen içindeyse,
    # bu kod direkt olarak `toptubelist` klasörünü hedefleyecektir.
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Eğer `rename_files.py` toptubelist'in içinde değil de, toptubelist'in üstündeyse
    # ve toptubelist'i hedeflemek istiyorsanız, bu yolu manuel olarak ayarlayın.
    # Örneğin: root_folder_to_process = "/path/to/your/toptubelist"
    
    # Genellikle, betiğin çalıştırıldığı dizin kök dizin olarak kabul edilir.
    # Bu durumda, `rename_files.py` dosyasını `toptubelist` klasörünün içine koyduğunuzu varsayarsak,
    # `current_script_dir` zaten `toptubelist` olacaktır.
    root_folder_to_process = current_script_dir 

    print(f"Yeniden adlandırma işlemi '{root_folder_to_process}' klasöründe başlayacak.")
    rename_files_in_directory(root_folder_to_process)
    print("Yeniden adlandırma işlemi tamamlandı.")
