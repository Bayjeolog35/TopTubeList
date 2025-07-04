import json
import os
import re

# Continent information with display names
CONTINENT_INFO = {
    "asia": {"display_name": "Asia"},
    "europe": {"display_name": "Europe"},
    "africa": {"display_name": "Africa"},
    "north_america": {"display_name": "North America"},
    "south_america": {"display_name": "South America"},
    "oceania": {"display_name": "Oceania"}
}

def generate_html_file(continent_name, videos_data, structured_data):
    """Belirtilen kıta için HTML dosyasını oluşturur."""

    # Klasör ve URL'lerde kullanılacak tireli isim
    sanitized_continent_name = continent_name.replace('_', '-')

    # Görüntülenecek kıta adı
    display_continent_name = CONTINENT_INFO.get(
        continent_name, {}
    ).get("display_name", continent_name.replace('-', ' ').replace('_', ' ').title())

    # Structured data JSON-LD bloğunu oluştur
    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2)
        structured_data_block = (
            '<script type="application/ld+json">\n' +
            structured_json +
            '\n</script>'
        )

    # Kıta navigasyonu için aktif sınıfı belirle
    continent_active_classes = {
        'asia_active': 'active' if continent_name == 'asia' else '',
        'europe_active': 'active' if continent_name == 'europe' else '',
        'africa_active': 'active' if continent_name == 'africa' else '',
        'north_america_active': 'active' if continent_name == 'north_america' else '',
        'south_america_active': 'active' if continent_name == 'south_america' else '',
        'oceania_active': 'active' if continent_name == 'oceania' else '',
    }

    # En çok izlenen video iframe'i (eğer video varsa)
    top_video_iframe = ""
    if videos_data and len(videos_data) > 0:
        top_video = videos_data[0]
        top_video_iframe = f"""
        <div class="featured-video">
            <h2>Most Viewed Video in {display_continent_name}</h2>
            <iframe 
                width="560" 
                height="315" 
                src="https://www.youtube.com/embed/{top_video['videoId']}" 
                title="{top_video['title']}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen>
            </iframe>
        </div>
        """

    # HTML şablonu
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

    <title>Trending YouTube Videos in {display_continent_name} - Updated Every 3 Hours | TopTubeList</title>
    <meta name="description" content="Watch the most popular YouTube videos trending across {display_continent_name}. Stay current with viral content.">
    <meta name="keywords" content="YouTube trends {display_continent_name}, popular videos {display_continent_name}, trending YouTube, viral content">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://toptubelist.com/continents/{sanitized_continent_name}/" />
    <link rel="stylesheet" href="../../style.css" />

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103"
        crossorigin="anonymous"></script>

{structured_data_block}
</head>
<body>
<header>
    <div class="container header-flex">
        <a href="../../index.html" id="logoLink"> <img src="../../TopTubeListLogo.webp" alt="TopTubeList Logo" width="100" style="margin-right: 12px; vertical-align: middle;">
        </a>
        <h1>Most Viewed in {display_continent_name}</h1>
        <button id="darkModeToggle" title="Toggle Dark Mode">🌙</button>
    </div>

    <nav id="continentNav">
        <a href="../../index.html">Worldwide</a>
        <a href="../../asia.html" class="{asia_active}">Asia</a>
        <a href="../../europe.html" class="{europe_active}">Europe</a>
        <a href="../../africa.html" class="{africa_active}">Africa</a>
        <a href="../../north_america.html" class="{north_america_active}">North America</a>
        <a href="../../south_america.html" class="{south_america_active}">South America</a>
        <a href="../../oceania.html" class="{oceania_active}">Oceania</a>
    </nav>
</header>

<main class="main-content">
    {top_video_iframe}
    
    <div class="video-list-wrapper">
        <div id="videoList" class="video-list"></div>
        <button id="loadMoreBtn" class="site-button">Load More</button>
    </div>
</main>

    <section class="about-section">
        <button id="aboutToggle" class="site-button">About Us</button>
        <div id="aboutContent">
            <p><strong>What is TopTubeList?</strong><br>
                TopTubeList helps you quickly see what people are watching on YouTube. You can explore videos by continent or country. No clutter, no fancy talk. Just a clean snapshot of the most viewed videos — updated every 3 hours.</p>

            <p><strong>Why did we build this site?</strong><br>
                My wife was in the kitchen cooking. My mission was clear: to answer that sacred question… <em>"What should we watch while eating?"</em><br>
                Then suddenly, I found myself thinking: <em>"What do other couples watch during dinner?"</em> So, like anyone else, I turned to Google.</p>

            <p><strong>And what did I find?</strong><br>
                "Most watched videos in June"...<br>
                "Top videos of 2025"...<br>
                Basically, just a highlight reel of the past.<br>
                But I wasn't looking for nostalgia — I wanted to know what's trending <strong>right now</strong>.</p>

            <p>That day, we may not have found the perfect video to watch...<br>
                But I realized we weren't alone.<br>
                There must be thousands of people wondering the exact same thing.<br>
                And that's when the idea of TopTubeList was born.</p>

            <p><strong>And the cherry on top?</strong><br>
                For creators who make "compilation videos" using trending clips, this site is basically a goldmine.</p>

            <p><strong>How does it work?</strong><br>
                Every 3 hours, we pull the most popular videos using YouTube's official Data API. Then we sort them by country and continent, so you can easily see what's trending anywhere in the world.</p>

            <p><strong>This is TopTubeList.</strong><br>
                If it's trending, chances are... we've already listed it. 😉</p>
        </div>
    </section>

    <footer>
        <div class="contact-section">
            <button id="contactToggle" class="site-button">Contact Us</button>
            <div id="contactContent" style="display: none;">
                <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
                    <input type="hidden" name="form-name" value="contact" />
                    <p hidden><label>Don't fill this out: <input name="bot-field" /></label></p>
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
        const form = document.querySelector("form[name='contact']");
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
                if (!container) return; // container yoksa çık

                container.innerHTML = ""; // İçeriği temizle

                if (allVideos.length === 0) {{
                    // Video yoksa özel mesaj göster
                    container.innerHTML = `
                        <div style="padding: 40px; text-align: center; grid-column: 1 / -1;">
                            <h2>📡 Sorry!</h2>
                            <p>We couldn't fetch trending YouTube videos for this continent at the moment.</p>
                            <p><em>(YouTube API might not be returning data for this region right now.)</em></p>
                        </div>
                    `;
                    const loadMoreBtn = document.getElementById("loadMoreBtn");
                    if (loadMoreBtn) loadMoreBtn.style.display = "none";
                    return; // Fonksiyondan çık
                }}

                allVideos.slice(0, displayCount).forEach(video => {{
                    const card = document.createElement("div");
                    card.className = "video-card";
                    card.innerHTML = `
                        <img src="${{video.thumbnail}}" alt="${{video.title}}" />
                        <div class="video-info">
                            <h3>${{video.title}}</h3>
                            <p><strong>Uploaded:</strong> ${{new Date(video.uploadDate).toLocaleDateString()}}</p>
                            <p><strong>Views:</strong> ${{video.views_str}}</p>
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

            // JSON dosyasının yolu dinamik olarak Python'dan geliyor
            fetch("/videos_{continent_name}.json") 
                .then(res => {{
                    if (!res.ok) {{
                        // Eğer dosya bulunamazsa (404) veya başka bir HTTP hatası olursa
                        console.error(`HTTP error fetching videos: ${{res.status}} for /videos_{continent_name}.json`);
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
                    allVideos = []; // Hata durumunda videoları boşalt
                    renderVideos(); // Boş liste ile tekrar render et (hata mesajını gösterir)
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
    
    # HTML içeriğini formatla
    html_content = html_template.format(
        display_continent_name=display_continent_name,
        sanitized_continent_name=sanitized_continent_name,
        continent_name=continent_name,
        structured_data_block=structured_data_block,
        top_video_iframe=top_video_iframe,
        **continent_active_classes
    )

    # Kıta klasörünü oluştur ve HTML dosyasını yaz
    continent_dir = os.path.join("continents", sanitized_continent_name)
    os.makedirs(continent_dir, exist_ok=True)

    output_path = os.path.join(continent_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ {output_path} oluşturuldu.")


def main():
    videos_base_dir = "."
    structured_data_base_dir = "."

    for continent_name in CONTINENT_INFO.keys():
        videos_file = os.path.join(videos_base_dir, f"videos_{continent_name}.json")
        structured_data_file = os.path.join(structured_data_base_dir, f"structured_data_{continent_name}.json")

        videos_data = []
        structured_data = {}

        # Video verilerini oku
        if os.path.exists(videos_file):
            try:
                with open(videos_file, "r", encoding="utf-8") as f:
                    videos_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"HATA: {videos_file} dosyasını okurken JSON hatası: {e}")
                videos_data = [] # Hata durumunda boş liste olarak ayarla
            except FileNotFoundError:
                print(f"UYARI: {videos_file} bulunamadı.")
                videos_data = []
        else:
            print(f"UYARI: {videos_file} bulunamadı. Boş video verisi ile devam ediliyor.")
            
        # Yapılandırılmış verileri oku
        if os.path.exists(structured_data_file):
            try:
                with open(structured_data_file, "r", encoding="utf-8") as f:
                    structured_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"HATA: {structured_data_file} dosyasını okurken JSON hatası: {e}")
                structured_data = {}
            except FileNotFoundError:
                print(f"UYARI: {structured_data_file} bulunamadı.")
                structured_data = {}
        else:
            print(f"UYARI: {structured_data_file} bulunamadı. Boş yapılandırılmış veri ile devam ediliyor.")

        # HTML dosyasını oluştur
        generate_html_file(continent_name, videos_data, structured_data)

if __name__ == "__main__":
    main()
