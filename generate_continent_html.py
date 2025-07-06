#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TopTubeList - Kıta Sayfaları Oluşturucu
Bu script continents/[kıta_adi]/index.html dosyalarını oluşturur.
"""

import os
import json
from datetime import datetime

# Kıta bilgileri
CONTINENT_INFO = {
    "asia": {
        "display_name": "Asia",
        "meta_description": "Trending YouTube videos in Asia - Most viewed content across Asian countries"
    },
    "europe": {
        "display_name": "Europe", 
        "meta_description": "Popular YouTube videos trending in European countries - Updated hourly"
    },
    "africa": {
        "display_name": "Africa",
        "meta_description": "Top viewed YouTube videos across African nations - Daily updated charts"
    },
    "north_america": {
        "display_name": "North America",
        "meta_description": "Viral YouTube content in USA, Canada and Mexico - Real-time trending videos"
    },
    "south_america": {
        "display_name": "South America",
        "meta_description": "Most watched YouTube videos in South American countries - Updated constantly"
    },
    "oceania": {
        "display_name": "Oceania",
        "meta_description": "Trending YouTube videos from Australia, New Zealand and Pacific Islands"
    }
}

def load_json_data(file_path):
    """JSON dosyasını yükler ve veriyi döndürür."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Uyarı: {file_path} bulunamadı. Boş veri kullanılıyor.")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️ Uyarı: {file_path} okunurken hata oluştu: {str(e)}")
        return []

def create_continent_directory(continent_name):
    """Kıta klasörünü oluşturur ve yolunu döndürür."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    continent_dir = os.path.join(script_dir, "continents", continent_name.replace("_", "-"))
    
    try:
        os.makedirs(continent_dir, exist_ok=True)
        print(f"📁 Klasör oluşturuldu: {continent_dir}")
        return continent_dir
    except OSError as e:
        print(f"❌ Klasör oluşturulamadı: {str(e)}")
        raise

def generate_top_video_iframe(videos_data):
    """En çok izlenen video için iframe kodu oluşturur."""
    if not videos_data or len(videos_data) == 0:
        return ""
    
    top_video = videos_data[0]
    return f"""
    <div class="featured-video">
        <h2>🔥 Most Viewed Video</h2>
        <div class="video-container">
            <iframe 
                width="560" 
                height="315" 
                src="https://www.youtube.com/embed/{top_video['videoId']}" 
                title="{top_video['title']}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>
        <div class="video-info">
            <h3>{top_video['title']}</h3>
            <p>👀 {top_video['views_str']} views | ⏱️ {top_video['duration']}</p>
        </div>
    </div>
    """

def generate_html_content(continent_name, videos_data, structured_data):
    """HTML içeriğini oluşturur."""
    continent_info = CONTINENT_INFO.get(continent_name, {})
    display_name = continent_info.get("display_name", continent_name.replace("_", " ").title())
    sanitized_name = continent_name.replace("_", "-")
    
    # Aktif menü öğeleri
    nav_active = {f"{k}_active": "active" if k == continent_name else "" for k in CONTINENT_INFO}
    
    # En çok izlenen video
    top_video_iframe = generate_top_video_iframe(videos_data)
    
    # Yapılandırılmış veri
    structured_block = ""
    if structured_data:
        structured_block = f'<script type="application/ld+json">\n{json.dumps(structured_data, indent=2)}\n</script>'
    
    # Güncel tarih
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trending YouTube Videos in {display_name} | TopTubeList</title>
    <meta name="description" content="{continent_info.get('meta_description', '')}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://toptubelist.com/continents/{sanitized_name}/">
    <link rel="stylesheet" href="../../assets/css/style.css">
    {structured_block}
</head>
<body>
    <header>
        <div class="container">
            <a href="../../index.html" class="logo">
                <img src="../../assets/images/logo.webp" alt="TopTubeList" width="120">
            </a>
            <h1>Trending in {display_name}</h1>
        </div>
        
        <nav class="continent-nav">
            <a href="../../index.html">Worldwide</a>
            <a href="../../continents/asia/" class="{nav_active['asia_active']}">Asia</a>
            <a href="../../continents/europe/" class="{nav_active['europe_active']}">Europe</a>
            <a href="../../continents/africa/" class="{nav_active['africa_active']}">Africa</a>
            <a href="../../continents/north-america/" class="{nav_active['north_america_active']}">North America</a>
            <a href="../../continents/south-america/" class="{nav_active['south_america_active']}">South America</a>
            <a href="../../continents/oceania/" class="{nav_active['oceania_active']}">Oceania</a>
        </nav>
    </header>

    <main class="container">
        {top_video_iframe}
        
        <section class="video-list-section">
            <h2>📺 Trending Videos</h2>
            <div id="videoList" class="video-grid"></div>
            <button id="loadMoreBtn" class="load-more">Load More Videos</button>
        </section>
    </main>

    <footer>
        <p>Last updated: {current_date}</p>
        <p>© {datetime.now().year} TopTubeList.com - All rights reserved</p>
    </footer>

    <script src="../../assets/js/main.js"></script>
    <script>
        // Video verilerini yükle
        const continentName = "{continent_name}";
        
        async function loadVideos() {{
            try {{
                const response = await fetch(`../../data/videos_${{continentName}}.json`);
                if (!response.ok) throw new Error('Network response was not ok');
                return await response.json();
            }} catch (error) {{
                console.error('Error loading videos:', error);
                return [];
            }}
        }}

        // Diğer JS fonksiyonları...
    </script>
</body>
</html>
"""

def generate_continent_page(continent_name):
    """Bir kıta için tüm sayfayı oluşturur."""
    print(f"\n🔨 {continent_name} için sayfa oluşturuluyor...")
    
    # Verileri yükle
    videos_data = load_json_data(f"videos_{continent_name}.json")
    structured_data = load_json_data(f"structured_data_{continent_name}.json")
    
    # Klasörü oluştur
    continent_dir = create_continent_directory(continent_name)
    
    # HTML içeriğini oluştur
    html_content = generate_html_content(continent_name, videos_data, structured_data)
    
    # Dosyaya yaz
    output_path = os.path.join(continent_dir, "index.html")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Başarılı: {output_path} oluşturuldu")
        return True
    except IOError as e:
        print(f"❌ Hata: Dosya yazılamadı - {str(e)}")
        return False

def main():
    print("""
    #######################################
    # TopTubeList - Kıta Sayfaları Oluşturucu
    # Tüm kıta sayfalarını oluşturuyor...
    #######################################
    """)
    
    success_count = 0
    total_continents = len(CONTINENT_INFO)
    
    for continent_name in CONTINENT_INFO:
        if generate_continent_page(continent_name):
            success_count += 1
    
    print(f"\n🏁 İşlem tamamlandı: {success_count}/{total_continents} kıta başarıyla oluşturuldu")
    
    if success_count < total_continents:
        print("⚠️ Bazı kıta sayfaları oluşturulamadı. Hata mesajlarını kontrol edin.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"\n💥 Kritik hata: {str(e)}")
