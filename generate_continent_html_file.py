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

    # Navigasyon HTML'i (temiz URL'ler kullanıldı)
    continent_nav_html = f"""
        <nav id="continentNav">
            <a href="/index.html">Worldwide</a>
            <a href="/asia/" class="{continent_active_classes['asia_active']}">Asia</a>
            <a href="/europe/" class="{continent_active_classes['europe_active']}">Europe</a>
            <a href="/africa/" class="{continent_active_classes['africa_active']}">Africa</a>
            <a href="/north_america/" class="{continent_active_classes['north_america_active']}">North America</a>
            <a href="/south_america/" class="{continent_active_classes['south_america_active']}">South America</a>
            <a href="/oceania/" class="{continent_active_classes['oceania_active']}">Oceania</a>
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
        
        # Kıta sayfasında aktif ülke butonu olmaz, bu yüzden 'active' sınıfı eklenmez.
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
        <button id="hamburgerBtn" class="hamburger">☰</button> <div class="country-panel">
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

    <script src="/script.js"></script> <script>
        // Kıta sayfasına özel JS kodu
        document.addEventListener("DOMContentLoaded", () => {{
            fetch(`/Country_data/videos/videos_{continent_name}.json`)
                .then(response => response.json())
                .then(videos => {{
                    const videoList = document.getElementById("videoList");
                    videos.slice(0, 20).forEach(video => {{
                        videoList.innerHTML += `
                            <div class="video-card">
                                <img src="${{video.thumbnail}}" alt="${{video.title}}" loading="lazy" />
                                <div class="video-info">
                                    <h3><a href="${{video.url}}" target="_blank">${{video.title}}</a></h3>
                                    <p>Views: ${{video.views_formatted}}</p>
                                </div>
                            </div>
                        `;
                    }});

                    let videosShown = 20;
                    const loadMoreBtn = document.getElementById('loadMoreBtn');
                    loadMoreBtn.addEventListener('click', () => {{
                        const nextVideos = videos.slice(videosShown, videosShown + 20);
                        if (nextVideos.length > 0) {{
                            nextVideos.forEach(video => {{
                                videoList.innerHTML += `
                                    <div class="video-card">
                                        <img src="${{video.thumbnail}}" alt="${{video.title}}" loading="lazy" />
                                        <div class="video-info">
                                            <h3><a href="${{video.url}}" target="_blank">${{video.title}}</a></h3>
                                            <p>Views: ${{video.views_formatted}}</p>
                                        </div>
                                    </div>
                                `;
                            }});
                            videosShown += 20;
                        }} else {{
                            loadMoreBtn.style.display = 'none'; // Daha fazla video yoksa butonu gizle
                        }}
                    }});
                    // Başlangıçta daha az video varsa loadMoreBtn gizle
                    if (videos.length <= videosShown) {{
                        loadMoreBtn.style.display = 'none';
                    }}
                }})
                .catch(error => console.error('Error loading videos:', error));

            // Alphabet Filter Logic
            document.querySelectorAll('.alphabet-letter').forEach(link => {{
                link.addEventListener('click', function(event) {{
                    event.preventDefault();
                    const selectedLetter = this.dataset.letter;
                    document.querySelectorAll('.country-button').forEach(button => {{
                        if (selectedLetter === 'all' || button.dataset.letter === selectedLetter) {{
                            button.style.display = 'inline-block';
                        }} else {{
                            button.style.display = 'none';
                        }}
                    }});
                }});
            }});

            // Hamburger menü logic
            const hamburger = document.getElementById("hamburgerBtn");
            const panel = document.querySelector(".country-panel");

            if (hamburger && panel) {{
                hamburger.addEventListener("click", () => {{
                    panel.classList.toggle("active");
                    localStorage.setItem("countryPanelOpen", panel.classList.contains("active"));
                }});
                // Sayfa yüklendiğinde panelin durumunu geri yükle
                const savedPanelState = localStorage.getItem("countryPanelOpen");
                if (savedPanelState === "true" && panel) {{
                    panel.classList.add("active");
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    # HTML dosyasını oluşturmak için dizin yapısı
    output_dir = continent_name.replace('_', '-') # örn: asia -> asia
    output_path_full = os.path.join(output_dir, "index.html") # örn: asia/index.html

    os.makedirs(output_dir, exist_ok=True) # Klasörü yoksa oluştur

    with open(output_path_full, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ {output_path_full} oluşturuldu.")

def main(config_file="config.yml"):
    """YAML config dosyasını okuyup tüm kıta HTML'lerini oluşturur."""
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        # Eğer config'de bu bilgiler yoksa, uygun hataları yakalayın veya varsayılan değerler atayın
        all_country_info = config.get("countries", {})
        all_continent_countries_map = config.get("continent_countries", {})

        print("⏳ Kıta HTML dosyaları oluşturuluyor...")
        # 'continents' listesi üzerinden döneceğiz
        for continent_data in config["continents"]:
            generate_continent_html_file(
                continent_name=continent_data["id"],
                all_country_info=all_country_info,
                all_continent_countries_map=all_continent_countries_map,
                structured_data=continent_data.get("structured_data", {}) # Kıta özelinde structured_data
            )
        print("🎉 Tüm Kıta HTML'leri başarıyla oluşturuldu!")
    
    except FileNotFoundError:
        print(f"❌ Hata: '{config_file}' dosyası bulunamadı. Lütfen doğru yolu belirttiğinizden emin olun.")
    except yaml.YAMLError as e:
        print(f"❌ Hata: YAML dosyasını okurken bir sorun oluştu: {str(e)}")
    except Exception as e:
        print(f"❌ Beklenmeyen bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
