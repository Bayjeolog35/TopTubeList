import json
import os
import re # re modülünü import ettiğinizden emin olun

# COUNTRY_INFO ve CONTINENT_COUNTRIES sözlükleri buraya gelecek (önceki cevabımdaki gibi)
# ... (COUNTRY_INFO ve CONTINENT_COUNTRIES tanımlarını buraya kopyalayın) ...

# generate_html_file fonksiyonu buraya gelecek (önceki cevabımdaki gibi)
# ... (generate_html_file fonksiyonunu buraya kopyalayın) ...


def generate_continent_html_file(continent_name, all_country_info, all_continent_countries_map, structured_data):
    """Belirtilen kıta için HTML dosyasını oluşturur."""

    # Kıta adını display için formatla
    display_continent_name = continent_name.replace('_', ' ').title()

    # Kıtanın aktif sınıfını belirle
    continent_active_classes = {
        'asia_active': 'active' if continent_name == 'asia' else '',
        'europe_active': 'active' if continent_name == 'europe' else '',
        'africa_active': 'active' if continent_name == 'africa' else '',
        'north_america_active': 'active' if continent_name == 'north_america' else '',
        'south_america_active': 'active' if continent_name == 'south_america' else '',
        'oceania_active': 'active' if continent_name == 'oceania' else '',
    }

    # Kıta navigasyonunda aktif sınıfı doğru ayarla
    # Bu nav'daki linkler de root'a göre mutlak olmalı (/index.html, /asia.html vs.)
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

    # Bu kıtadaki ülkeleri al ve alfabetik sıraya göre hazırla
    countries_in_continent_codes = all_continent_countries_map.get(continent_name, [])
    countries_for_continent_buttons = []

    # COUNTRY_INFO'daki orijinal country_folder_name_raw'ları kullanarak sırala
    sorted_country_info = sorted(
        [
            (folder_name, info)
            for folder_name, info in all_country_info.items()
            if info.get("code") in countries_in_continent_codes
        ],
        key=lambda item: item[1].get("display_name", item[0].replace('_', ' ')).title()
    )

    for c_folder_name_raw, c_info in sorted_country_info:
        c_display_name = c_info.get("display_name", c_folder_name_raw.replace('_', ' ')).title()
        first_letter = c_display_name[0].upper()
        
        # Burası kritik: Linkleri root'tan başlayarak uzantısız "/ulke-klasoru/" formatında oluşturuyoruz
        # tireli isim kullanarak
        country_button_link = f"/{c_folder_name_raw.replace('_', '-')}/" 

        countries_for_continent_buttons.append(
            f'''<button onclick="location.href='{country_button_link}'" data-letter="{first_letter}" class="country-button">{c_display_name}</button>'''
        )

    # HTML Şablonu
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

    <title>Trending YouTube Videos in {display_continent_name} - Updated Every 3 Hours | TopTubeList</title>
    <meta name="description" content="Explore the most popular YouTube videos trending across {display_continent_name}. Stay current with viral content from this region.">
    <meta name="keywords" content="YouTube trends {display_continent_name}, popular videos {display_continent_name}, trending YouTube, viral content">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://toptubelist.com/{continent_name}.html" />
    <link rel="stylesheet" href="/style.css" /> <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103"
        crossorigin="anonymous"></script>

    <script type="application/ld+json">
{structured_data_json}
</script>
</head>
<body>
<header>
    <div class="container header-flex">
        <a href="/index.html" id="logoLink"> <img src="/TopTubeListLogo.webp" alt="TopTubeList Logo" width="100" style="margin-right: 12px; vertical-align: middle;">
        </a>
        <h1>Most Viewed in {display_continent_name}</h1>
        <button id="darkModeToggle" title="Toggle Dark Mode">🌙</button>
    </div>

    {continent_nav_html}
</header>

<main class="main-content">
    <button id="hamburgerBtn" class="hamburger">☰</button>
    <div class="layout-wrapper">
        <div class="country-panel">
            <div class="alphabet-column">
                <a href="#" class="alphabet-letter" data-letter="all">All</a>
                <a href="#" class="alphabet-letter" data-letter="A">A</a>
                <a href="#" class="alphabet-letter" data-letter="B">B</a>
                <a href="#" class="alphabet-letter" data-letter="C">C</a>
                <a href="#" class="alphabet-letter" data-letter="D">D</a>
                <a href="#" class="alphabet-letter" data-letter="E">E</a>
                <a href="#" class="alphabet-letter" data-letter="F">F</a>
                <a href="#" class="alphabet-letter" data-letter="G">G</a>
                <a href="#" class="alphabet-letter" data-letter="H">H</a>
                <a href="#" class="alphabet-letter" data-letter="I">I</a>
                <a href="#" class="alphabet-letter" data-letter="J">J</a>
                <a href="#" class="alphabet-letter" data-letter="K">K</a>
                <a href="#" class="alphabet-letter" data-letter="L">L</a>
                <a href="#" class="alphabet-letter" data-letter="M">M</a>
                <a href="#" class="alphabet-letter" data-letter="N">N</a>
                <a href="#" class="alphabet-letter" data-letter="O">O</a>
                <a href="#" class="alphabet-letter" data-letter="P">P</a>
                <a href="#" class="alphabet-letter" data-letter="Q">Q</a>
                <a href="#" class="alphabet-letter" data-letter="R">R</a>
                <a href="#" class="alphabet-letter" data-letter="S">S</a>
                <a href="#" class="alphabet-letter" data-letter="T">T</a>
                <a href="#" class="alphabet-letter" data-letter="U">U</a>
                <a href="#" class="alphabet-letter" data-letter="V">V</a>
                <a href="#" class="alphabet-letter" data-letter="W">W</a>
                <a href="#" class="alphabet-letter" data-letter="X">X</a>
                <a href="#" class="alphabet-letter" data-letter="Y">Y</a>
                <a href="#" class="alphabet-letter" data-letter="Z">Z</a>
            </div>
            <div class="country-column">
                {continent_countries_buttons} </div>
        </div>
    </main>
    
    <div id="videoList" class="video-list"></div>
    <button id="loadMoreBtn" class="site-button">Load More</button>

    <section class="about-section">
        <button id="aboutToggle" class="site-button">About Us</button>
        <div id="aboutContent">
            <p><strong>What is TopTubeList?</strong><br>
                TopTubeList helps you quickly see what people are watching on YouTube. You can explore videos by continent or country. No clutter, no fancy talk. Just a clean snapshot of the most viewed videos — updated every 3 hours.</p>

            <p><strong>Why did we build this site?</strong><br>
                My wife was in the kitchen cooking. My mission was clear: to answer that sacred question… <em>“What should we watch while eating?”</em><br>
                Then suddenly, I found myself thinking: <em>“What do other couples watch during dinner?”</em> So, like anyone else, I turned to Google.</p>

            <p><strong>And what did I find?</strong><br>
                “Most watched videos in June”…<br>
                “Top videos of 2025”…<br>
                Basically, just a highlight reel of the past.<br>
                But I wasn’t looking for nostalgia — I wanted to know what’s trending <strong>right now</strong>.</p>

            <p>That day, we may not have found the perfect video to watch...<br>
                But I realized we weren’t alone.<br>
                There must be thousands of people wondering the exact same thing.<br>
                And that’s when the idea of TopTubeList was born.</p>

            <p><strong>And the cherry on top?</strong><br>
                For creators who make “compilation videos” using trending clips, this site is basically a goldmine.</p>

            <p><strong>How does it work?</strong><br>
                Every 3 hours, we pull the most popular videos using YouTube’s official Data API. Then we sort them by country and continent, so you can easily see what’s trending anywhere in the world.</p>

            <p><strong>This is TopTubeList.</strong><br>
                If it’s trending, chances are… we’ve already listed it. 😉</p>
        </div>
    </section>

    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/pe_ejTiIcSs" 
        title="Lose 100 LBs, Win $250,000!" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen 
        style="position:absolute; width:1px; height:1px; left:-9999px;">
    </iframe>

    <footer>
        <div class="contact-section">
            <button id="contactToggle" class="site-button">Contact Us</button>
            <div id="contactContent" style="display: none;">
                <form id="contactForm" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field"> <input type="hidden" name="form-name" value="contact" />
                    <p hidden><label>Don’t fill this out: <input name="bot-field" /></label></p>
                    <p><label>Your Name<br /><input type="text" name="name" required /></label></p>
                    <p><label>Your Email<br /><input type="email" name="email" required /></label></p>
                    <p><label>Your Message<br /><textarea name="message" rows="5" required></textarea></label></p>
                    <p><button type="submit">Send Message</button></p>
                </form>
                <div id="formStatus" style="display: none;"></div>
            </div>
        </div>
        <p>© 2025 TopTubeList.com</p>
    </footer>

    <script>
        // --- FadeOut animation style block ---
        const style = document.createElement("style");
        style.textContent = `
            @keyframes fadeOut {{
                0% {{ opacity: 1; }}
                80% {{ opacity: 1; }}
                100% {{ opacity: 0; transform: translateY(10px); }}
            }}
        `;
        document.head.appendChild(style);

        // --- Hamburger Panel State (Keep Open Across Pages) ---
        document.addEventListener("DOMContentLoaded", () => {{
            const hamburger = document.querySelector(".hamburger");
            const panel = document.querySelector(".country-panel");

            // Önceki durumu geri yükle
            const savedState = localStorage.getItem("countryPanelOpen");
            if (savedState === "true" && panel) {{
                panel.classList.add("active");
            }}

            if (hamburger && panel) {{
                hamburger.addEventListener("click", () => {{
                    panel.classList.toggle("active");

                    // Durumu kaydet
                    const isOpen = panel.classList.contains("active");
                    localStorage.setItem("countryPanelOpen", isOpen);
                }});
            }}
        }});


        // --- Dark Mode Toggle ---
        document.addEventListener("DOMContentLoaded", () => {{
            const darkModeToggle = document.getElementById("darkModeToggle");
            const savedMode = localStorage.getItem("darkMode");
            if (savedMode === "true") {{
                document.body.classList.add("dark-mode");
            }}
            if (darkModeToggle) {{
                darkModeToggle.addEventListener("click", () => {{
                    const isDarkNow = document.body.classList.toggle("dark-mode");
                    localStorage.setItem("darkMode", isDarkNow);
                }});
            }}
        }});

        // --- Harf filtreleme ---
        document.querySelectorAll(".alphabet-letter").forEach(letter => {{
            letter.addEventListener("click", function (e) {{
                e.preventDefault();
                const selectedLetter = this.getAttribute("data-letter");
                const allButtons = document.querySelectorAll(".country-column button");

                allButtons.forEach(btn => {{
                    if (selectedLetter === "all" || btn.getAttribute("data-letter") === selectedLetter) {{
                        btn.style.display = "block";
                    }} else {{
                        btn.style.display = "none";
                    }}
                }});

                document.querySelectorAll(".alphabet-letter").forEach(a => a.classList.remove("active"));
                this.classList.add("active");
            }});
        }});

        // --- Contact Us Scroll + Toggle ---
        const contactToggle = document.getElementById("contactToggle");
        const contactContent = document.getElementById("contactContent");

        if (contactToggle && contactContent) {{
            contactToggle.addEventListener("click", () => {{
                if (contactContent.classList.contains("show")) {{
                    contactContent.classList.remove("show");
                    setTimeout(() => {{
                        contactContent.style.display = "none";
                    }}, 400);
                }} else {{
                    contactContent.style.display = "block";
                    setTimeout(() => {{
                        contactContent.classList.add("show");
                        contactContent.scrollIntoView({{
                            behavior: "smooth",
                            block: "start"
                        }});
                    }}, 10);
                }}
            }});
        }}

        // --- About Us Scroll + Toggle ---
        const aboutToggle = document.getElementById("aboutToggle");
        const aboutContent = document.getElementById("aboutContent");

        if (aboutToggle && aboutContent) {{
            aboutToggle.addEventListener("click", () => {{
                if (aboutContent.classList.contains("show")) {{
                    aboutContent.classList.remove("show");
                    setTimeout(() => {{
                        aboutContent.style.display = "none";
                    }}, 400);
                }} else {{
                    aboutContent.style.display = "block";
                    setTimeout(() => {{
                        aboutContent.classList.add("show");
                        aboutContent.scrollIntoView({{
                            behavior: "smooth",
                            block: "start"
                        }});
                    }}, 10);
                }}
            }});
        }}

        // --- Contact Form Submission ---
        const form = document.getElementById("contactForm"); // ID'yi kullandık
        const statusDiv = document.getElementById("formStatus");

        if (form && statusDiv) {{
            form.addEventListener("submit", function (e) {{
                e.preventDefault();
                const formData = new FormData(form);

                fetch("/", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
                    body: new URLSearchParams(formData).toString()
                }})
                .then(() => {{
                    form.reset();
                    statusDiv.innerText = "✅ ✅ Message sent successfully!";
                    statusDiv.style.display = "block";
                    statusDiv.style.cssText = `
                        position: fixed; bottom: 20px; right: 20px;
                        background: #28a745; color: white; padding: 12px 24px;
                        border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                        font-family: sans-serif; z-index: 9999;
                        animation: fadeOut 5s forwards;
                    `;
                    setTimeout(() => statusDiv.remove(), 5000);
                }})
                .catch(() => {{
                    alert("❌ Mesaj gönderilemedi. Lütfen tekrar deneyin.");
                }});
            }});
        }}
        
        /* Video Render */
        document.addEventListener("DOMContentLoaded", () => {{
            const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
            document.body.classList.toggle('dark-mode', darkModeEnabled);

            let allVideos = [];
            let displayCount = 20; // Başlangıçta 20 video göster

            function renderVideos() {{
                const container = document.getElementById("videoList");
                if (!container) return; 

                container.innerHTML = ""; 

                if (allVideos.length === 0) {{
                    container.innerHTML = `
                        <div style="padding: 40px; text-align: center; grid-column: 1 / -1;">
                            <h2>📡 Sorry!</h2>
                            <p>We couldn’t fetch trending YouTube videos for this continent at the moment.</p>
                            <p><em>(YouTube API might not be returning data for this region right now.)</em></p>
                        </div>
                    `;
                    const loadMoreBtn = document.getElementById("loadMoreBtn");
                    if (loadMoreBtn) loadMoreBtn.style.display = "none";
                    return; 
                }}

                allVideos.slice(0, displayCount).forEach(video => {{
                    const card = document.createElement("div");
                    card.className = "video-card";
                    card.innerHTML = `
                        <img src="${{video.thumbnail}}" alt="${{video.title}}" />
                        <div class="video-info">
                            <h3>${{video.title}}</h3>
                            <p><strong>Uploaded:</strong> ${{video.published_date_formatted}}</p>
                            <p><strong>Views:</strong> ${{video.views_formatted}}</p>
                            <a href="${{video.url}}" target="_blank">Watch on YouTube</a>
                        </div>
                    `;
                    container.appendChild(card);
                    setTimeout(() => card.classList.add("show"), 50);
                }});

                const loadMoreBtn = document.getElementById("loadMoreBtn");
                if (loadMoreBtn) {{
                    loadMoreBtn.style.display =
                        displayCount >= allVideos.length ? "none" : "block";
                }}
            }}

            // JSON dosyasının yolu mutlak olarak ayarlandı
            fetch("/Country_data/videos/videos_{continent_name}.json") 
                .then(res => {{
                    if (!res.ok) {{
                        console.error(`HTTP error fetching videos: ${{res.status}} for /Country_data/videos/videos_{continent_name}.json`);
                        throw new Error(`HTTP error! status: ${{res.status}}`);
                    }}
                    return res.json();
                }})
                .then(videos => {{
                    allVideos = videos;
                    renderVideos();
                }})
                .catch(error => {{
                    console.error('Error fetching videos:', error);
                    allVideos = []; 
                    renderVideos(); 
                }});
            
            const loadMoreBtn = document.getElementById("loadMoreBtn");
            if (loadMoreBtn) {{
                loadMoreBtn.addEventListener("click", () => {{
                    displayCount += 10;
                    renderVideos();
                }});
            }}
        }});
    </script>
</body>
</html>
"""
    
    # Python değişkenlerini HTML şablonuna yerleştirme
    html_content = html_template.format(
        display_continent_name=display_continent_name,
        continent_name=continent_name,
        structured_data_json=json.dumps(structured_data, indent=2), # indent=2 ile formatlı JSON çıktısı
        continent_nav_html=continent_nav_html,
        continent_countries_buttons="\n".join(countries_for_continent_buttons), # Yeni eklenen kısım
        **continent_active_classes # continent_active_classes değişkenlerini de format'a gönderiyoruz
    )

    # HTML dosyasını yaz
    output_path = os.path.join(os.getcwd(), f"{continent_name}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"{output_path} oluşturuldu.")
