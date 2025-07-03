import json
import os
import yaml
from datetime import datetime

def generate_continent_html_file(continent_name, all_country_info, all_continent_countries_map, structured_data):
    """Belirtilen kıta için HTML dosyasını oluşturur."""

    # Kıta adını görüntüleme formatına çevir (Örnek: "north_america" → "North America")
    display_continent_name = continent_name.replace('_', ' ').title()

    # Kıta navigasyonu için aktif sınıfları belirle
    continent_active_classes = {
        'asia_active': 'active' if continent_name == 'asia' else '',
        'europe_active': 'active' if continent_name == 'europe' else '',
        'africa_active': 'active' if continent_name == 'africa' else '',
        'north_america_active': 'active' if continent_name == 'north_america' else '',
        'south_america_active': 'active' if continent_name == 'south_america' else '',
        'oceania_active': 'active' if continent_name == 'oceania' else '',
    }

    # Navigasyon HTML'i
    continent_nav_html = f"""
        <nav id="continentNav">
            <a href="/index.html">Worldwide</a>
            <a href="/asia.html" class="{continent_active_classes['asia_active']}">Asia</a>
            <a href="/europe.html" class="{continent_active_classes['europe_active']}">Europe</a>
            <a href="/africa.html" class="{continent_active_classes['africa_active']}">Africa</a>
            <a href="/north_america.html" class="{continent_active_classes['north_america_active']}">North America</a>
            <a href="/south_america.html" class="{continent_active_classes['south_america_active']}">South America</a>
            <a href="/oceania.html" class="{continent_active_classes['oceania_active']}">Oceania</a>
        </nav>
    """

    # Kıtadaki ülkeleri al ve alfabetik sırala
    countries_in_continent_codes = all_continent_countries_map.get(continent_name, [])
    countries_for_continent_buttons = []

    # Ülkeleri orijinal isimlerine göre sırala
    sorted_country_info = sorted(
        [
            (folder_name, info)
            for folder_name, info in all_country_info.items()
            if info.get("code") in countries_in_continent_codes
        ],
        key=lambda item: item[1].get("display_name", item[0].replace('_', ' ')).title()
    )

    # Ülke butonlarını oluştur
    for c_folder_name_raw, c_info in sorted_country_info:
        c_display_name = c_info.get("display_name", c_folder_name_raw.replace('_', ' ')).title()
        first_letter = c_display_name[0].upper()
        country_button_link = f"/{c_folder_name_raw.replace('_', '-')}/"
        
        countries_for_continent_buttons.append(
            f'''<button onclick="location.href='{country_button_link}'" data-letter="{first_letter}" class="country-button">{c_display_name}</button>'''
        )

    # HTML Şablonu
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Trending YouTube Videos in {display_continent_name} | TopTubeList</title>
    <meta name="description" content="Most viewed YouTube videos in {display_continent_name}. Updated every 3 hours.">
    <link rel="stylesheet" href="/style.css" />
    <script type="application/ld+json">
{json.dumps(structured_data, indent=2)}
    </script>
</head>
<body>
    <header>
        <div class="container header-flex">
            <a href="/index.html" id="logoLink"><img src="/TopTubeListLogo.webp" alt="Logo" width="100"></a>
            <h1>Trending in {display_continent_name}</h1>
            <button id="darkModeToggle">🌙</button>
        </div>
        {continent_nav_html}
    </header>

    <main class="main-content">
        <div class="country-panel">
            <div class="alphabet-column">
                <a href="#" class="alphabet-letter" data-letter="all">All</a>
                {' '.join([f'<a href="#" class="alphabet-letter" data-letter="{chr(65+i)}">{chr(65+i)}</a>' for i in range(26)])}
            </div>
            <div class="country-column">
                {' '.join(countries_for_continent_buttons)}
            </div>
        </div>
    </main>

    <div id="videoList" class="video-list"></div>
    <button id="loadMoreBtn" class="site-button">Load More</button>

    <script>
        // Kıta sayfasına özel JS kodu
        document.addEventListener("DOMContentLoaded", () => {{
            fetch(`/Country_data/videos/videos_{continent_name}.json`)
                .then(response => response.json())
                .then(videos => {{
                    const videoList = document.getElementById("videoList");
                    videos.slice(0, 20).forEach(video => {{
                        videoList.innerHTML += `
                            <div class="video-card">
                                <img src="${{video.thumbnail}}" alt="${{video.title}}" />
                                <div class="video-info">
                                    <h3>${{video.title}}</h3>
                                    <p>Views: ${{video.views_formatted}}</p>
                                    <a href="${{video.url}}" target="_blank">Watch</a>
                                </div>
                            </div>
                        `;
                    }});
                }});
        }});
    </script>
</body>
</html>
"""

    # HTML dosyasını oluştur
    output_path = f"{continent_name}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ {output_path} oluşturuldu.")

def main(config_file="config.yml"):
    """YAML config dosyasını okuyup tüm kıta HTML'lerini oluşturur."""
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        print("⏳ HTML dosyaları oluşturuluyor...")
        for continent in config["continents"]:
            generate_continent_html_file(
                continent_name=continent["id"],
                all_country_info=config["countries"],
                all_continent_countries_map=config["continent_countries"],
                structured_data=continent["structured_data"]
            )
        print("🎉 Tüm HTML'ler başarıyla oluşturuldu!")
    
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

if __name__ == "__main__":
    main()
