import json
import os
import yaml
from datetime import datetime

def generate_country_html_file(country_folder_name, country_info, all_country_info, all_continent_countries_map, structured_data):
    """Belirtilen ülke için HTML dosyasını oluşturur."""

    # Ülke adını görüntüleme formatına çevir (Örnek: "united_states" → "United States")
    display_country_name = country_info.get("display_name", country_folder_name.replace('_', ' ')).title()
    country_code = country_info.get("code")
    country_continent_id = country_info.get("continent_id")

    # Kıta navigasyonu için aktif sınıfları belirle
    # Bu kısım kıta dosyasındakiyle aynı kalmalı
    continent_active_classes = {
        'asia_active': 'active' if country_continent_id == 'asia' else '',
        'europe_active': 'active' if country_continent_id == 'europe' else '',
        'africa_active': 'active' if country_continent_id == 'africa' else '',
        'north_america_active': 'active' if country_continent_id == 'north_america' else '',
        'south_america_active': 'active' if country_continent_id == 'south_america' else '',
        'oceania_active': 'active' if country_continent_id == 'oceania' else '',
    }

    # Navigasyon HTML'i (kıta sayfalarıyla tutarlı, temiz URL'ler kullanıldı)
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

    # Ülkenin ait olduğu kıtadaki diğer ülkeleri al ve alfabetik sırala
    countries_in_current_continent_codes = all_continent_countries_map.get(country_continent_id, [])
    countries_for_country_page_buttons = []

    # Sadece mevcut kıtadaki ülkeleri al ve alfabetik sırala
    sorted_country_info_for_continent = sorted(
        [
            (f_name, info)
            for f_name, info in all_country_info.items()
            if info.get("code") in countries_in_current_continent_codes
        ],
        key=lambda item: item[1].get("display_name", item[0].replace('_', ' ')).title()
    )

    # Ülke butonlarını oluştur (bu kısım kıta sayfasındakine benzer)
    for c_folder_name_raw, c_info in sorted_country_info_for_continent:
        c_display_name = c_info.get("display_name", c_folder_name_raw.replace('_', ' ')).title()
        first_letter = c_display_name[0].upper()
        country_button_link = f"/{c_folder_name_raw.replace('_', '-')}/"
        
        # Aktif ülke butonu için stil (isteğe bağlı)
        button_class = "country-button"
        if c_folder_name_raw == country_folder_name: # Eğer buton o anki ülkeyi temsil ediyorsa
            button_class += " active" 
        
        countries_for_country_page_buttons.append(
            f'''<button onclick="location.href='{country_button_link}'" data-letter="{first_letter}" class="{button_class}">{c_display_name}</button>'''
        )

    # HTML Şablonu
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Trending YouTube Videos in {display_country_name} | TopTubeList</title>
    <meta name="description" content="Most viewed YouTube videos in {display_country_name}. Updated every 3 hours.">
    <link rel="stylesheet" href="/style.css" />
    <script type="application/ld+json">
{json.dumps(structured_data, indent=2)}
    </script>
</head>
<body>
    <header>
        <div class="container header-flex">
            <a href="/index.html" id="logoLink"><img src="/TopTubeListLogo.webp" alt="Logo" width="100"></a>
            <h1>Trending in {display_country_name}</h1>
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
                {' '.join(countries_for_country_page_buttons)}
            </div>
        </div>
    </main>

    <div id="videoList" class="video-list"></div>
    <button id="loadMoreBtn" class="site-button">Load More</button>

    <script src="/script.js"></script> <script>
        // Ülke sayfasına özel JS kodu
        document.addEventListener("DOMContentLoaded", () => {{
            fetch(`/Country_data/videos/videos_{country_folder_name}.json`)
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
    output_dir = country_folder_name.replace('_', '-') # örn: united-states
    output_path_full = os.path.join(output_dir, "index.html") # örn: united-states/index.html

    os.makedirs(output_dir, exist_ok=True) # Klasörü yoksa oluştur

    with open(output_path_full, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ {output_path_full} oluşturuldu.")

def main(config_file="config.yml"):
    """YAML config dosyasını okuyup tüm ülke HTML'lerini oluşturur."""
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        # Eğer config'de bu bilgiler yoksa, uygun hataları yakalayın veya varsayılan değerler atayın
        all_country_info = config.get("countries", {})
        all_continent_countries_map = config.get("continent_countries", {})

        print("⏳ Ülke HTML dosyaları oluşturuluyor...")
        for country_folder_name, country_data in all_country_info.items():
            generate_country_html_file(
                country_folder_name=country_folder_name,
                country_info=country_data,
                all_country_info=all_country_info,
                all_continent_countries_map=all_continent_countries_map,
                structured_data=country_data.get("structured_data", {}) # Ülke özelinde structured_data
            )
        print("🎉 Tüm Ülke HTML'leri başarıyla oluşturuldu!")
    
    except FileNotFoundError:
        print(f"❌ Hata: '{config_file}' dosyası bulunamadı. Lütfen doğru yolu belirttiğinizden emin olun.")
    except yaml.YAMLError as e:
        print(f"❌ Hata: YAML dosyasını okurken bir sorun oluştu: {str(e)}")
    except Exception as e:
        print(f"❌ Beklenmeyen bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
