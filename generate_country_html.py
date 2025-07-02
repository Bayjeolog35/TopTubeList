import json
import os
from country_data import COUNTRY_INFO
from country_data import CONTINENT_COUNTRIES

def generate_html_file(country_folder_name, videos_data, structured_data):
    """Belirtilen ülke için HTML dosyasını oluşturur."""

    display_country_name = COUNTRY_INFO.get(country_folder_name, {}).get("display_name", country_folder_name.replace('_', ' '))

    country_dir = os.path.join(os.getcwd(), country_folder_name)
    os.makedirs(country_dir, exist_ok=True)

    # HTML şablonu (Yollar güncellendi)
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

  <title>Trending YouTube Videos in {display_country_name} - Updated Every 3 Hours | TopTubeList</title>
  <meta name="description" content="Watch the most popular YouTube videos trending across {display_country_name}. Stay current with viral content.">
  <meta name="keywords" content="YouTube trends {display_country_name}, popular videos {display_country_name}, trending YouTube, viral content">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://toptubelist.com/{country_folder_name}.html" />
  <link rel="stylesheet" href="../style.css" />

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103"
    crossorigin="anonymous"></script>

  <script type="application/ld+json">
{structured_data_json}
</script>
</head>
  
<body>
  
<header>
  <div class="container header-flex">
    <a href="../index.html" id="logoLink">
      <img src="../TopTubeListLogo.webp" alt="TopTubeList Logo" width="100" style="margin-right: 12px; vertical-align: middle;">
    </a>
    <h1>Most Viewed in {display_country_name}</h1>
    <button id="darkModeToggle" title="Toggle Dark Mode">🌙</button>
  </div>

  <nav id="continentNav">
    <a href="../index.html">Worldwide</a>
    <a href="../asia.html" class="{asia_active}">Asia</a>
    <a href="../europe.html" class="{europe_active}">Europe</a>
    <a href="../africa.html" class="{africa_active}">Africa</a>
    <a href="../north_america.html" class="{north_america_active}">North America</a>
    <a href="../south_america.html" class="{south_america_active}">South America</a>
    <a href="../oceania.html" class="{oceania_active}">Oceania</a>
  </nav>
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
    <a href="#" class="alphabet-letter" data-letter="E">E">E</a>
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
  {country_buttons}
</div>
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
      <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="contact" />
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

  
 // hamburger menü
  document.addEventListener("DOMContentLoaded", () => {{
    const hamburger = document.querySelector(".hamburger");
    const panel = document.querySelector(".country-panel");

    if (hamburger && panel) {{
      hamburger.addEventListener("click", () => {{
        panel.classList.toggle("active");
      }});
    }}
  }});


// --- Dark Mode Toggle ---
document.addEventListener("DOMContentLoaded", () => {{
  const darkModeToggle = document.getElementById("darkModeToggle");

  // Sayfa yüklendiğinde dark mode'u uygula
  const savedMode = localStorage.getItem("darkMode");
  if (savedMode === "true") {{
    document.body.classList.add("dark-mode");
  }}

  // Tıklanınca dark mode'u toggle et
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
    const form = document.getElementById("contactForm");
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

    
                      
  /* Video Render*/
  
  document.addEventListener("DOMContentLoaded", () => {{
    const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
    document.body.classList.toggle('dark-mode', darkModeEnabled);

    let allVideos = [];
    let displayCount = 10;

   function renderVideos() {{
  const container = document.getElementById("videoList");
  container.innerHTML = "";

  allVideos.slice(0, displayCount).forEach(video => {{
    const card = document.createElement("div");
    card.className = "video-card";
    card.innerHTML = `
      <img src="${{video.thumbnail}}" alt="${{video.title}}" />
      <div class="video-info">
        <h2>${{video.title}}</h2>
        <p><strong>Uploaded:</strong> ${{new Date(video.uploadDate).toLocaleDateString()}}</p>
        <p><strong>Views:</strong> ${{video.views_str}}</p>
        <a href="${{video.url}}" target="_blank">Watch on YouTube</a>
      </div>
    `;
    container.appendChild(card);
    setTimeout(() => card.classList.add("show"), 50);
  }});

  document.getElementById("loadMoreBtn").style.display =
    displayCount >= allVideos.length ? "none" : "block";
}}


    // JSON dosyasının yolu güncellendi: "../Country_data/videos/videos_{country_folder_name}.json"
    fetch("../Country_data/videos/videos_{country_folder_name}.json") 
      .then(res => res.json())
      .then(videos => {{
        allVideos = videos;
        renderVideos();
      }})
      .catch(error => console.error('Error fetching videos:', error));
 
    document.getElementById("loadMoreBtn").addEventListener("click", () => {{
      displayCount += 10;
      renderVideos();
    }});

  }});
</script>

</body>
</html>
"""
    
    continent_of_country = ""
    for continent, countries in CONTINENT_COUNTRIES.items():
        if country_folder_name in countries:
            continent_of_country = continent
            break

    asia_active = 'active' if continent_of_country == 'asia' else ''
    europe_active = 'active' if continent_of_country == 'europe' else ''
    africa_active = 'active' if continent_of_country == 'africa' else ''
    north_america_active = 'active' if continent_of_country == 'north_america' else ''
    south_america_active = 'active' if continent_of_country == 'south_america' else ''
    oceania_active = 'active' if continent_of_country == 'oceania' else ''

    country_buttons_html = []
    for c_folder_name, c_info in COUNTRY_INFO.items():
        c_display_name = c_info.get("display_name", c_folder_name.replace('_', ' '))
        first_letter = c_display_name[0].upper()
        country_buttons_html.append(f'<button onclick="location.href=\'../{c_folder_name}/index.html\'" data-letter="{first_letter}">{c_display_name}</button>')
    country_buttons_html = "\n".join(country_buttons_html)


    html_content = html_template.format(
        display_country_name=display_country_name,
        country_folder_name=country_folder_name,
        structured_data_json=json.dumps(structured_data, indent=2),
        asia_active=asia_active,
        europe_active=europe_active,
        africa_active=africa_active,
        north_america_active=north_america_active,
        south_america_active=south_america_active,
        oceania_active=oceania_active,
        country_buttons=country_buttons_html
    )

    output_path = os.path.join(country_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"{output_path} oluşturuldu.")

def main():
    # JSON dosyalarını yeni yoldan oku
    base_data_dir = "Country_data"
    videos_base_dir = os.path.join(base_data_dir, "videos")
    structured_data_base_dir = os.path.join(base_data_dir, "structured_data")

    for country_folder_name, info in COUNTRY_INFO.items():
        videos_file = os.path.join(videos_base_dir, f"videos_{country_folder_name}.json")
        structured_data_file = os.path.join(structured_data_base_dir, f"structured_data_{country_folder_name}.json")

        videos_data = []
        structured_data = {}

        if os.path.exists(videos_file):
            with open(videos_file, "r", encoding="utf-8") as f:
                videos_data = json.load(f)
        else:
            print(f"Uyarı: {videos_file} bulunamadı. Bu ülke için video verisi olmayacak.")

        if os.path.exists(structured_data_file):
            with open(structured_data_file, "r", encoding="utf-8") as f:
                structured_data = json.load(f)
        else:
            print(f"Uyarı: {structured_data_file} bulunamadı. Bu ülke için yapılandırılmış veri olmayacak.")

        generate_html_file(country_folder_name, videos_data, structured_data)

if __name__ == "__main__":
    main()
