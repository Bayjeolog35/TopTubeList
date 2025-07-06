import os
import json

# Sabitler
# VIDEO_DATA_DIR: Video JSON dosyalarının bulunduğu dizin.
# OUTPUT_DIR: Oluşturulan HTML dosyalarının kaydedileceği dizin.
# Genellikle aynı dizin olduğu için '.' olarak ayarlanır.
VIDEO_DATA_DIR = "."
OUTPUT_DIR = "."

# Helper fonksiyonları

def load_video_data(name):
    """
    Belirtilen isimdeki video veri JSON dosyasını yükler.
    Dosya bulunamazsa boş liste döndürür.
    """
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.vid.data.json")
    if not os.path.exists(path):
        print(f"⛔ Video verisi bulunamadı: {name}.vid.data.json")
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON okuma hatası '{path}': {e}")
        return []

def load_structured_data(name):
    """
    Belirtilen isimdeki yapılandırılmış veri JSON dosyasını yükler.
    Dosya bulunamazsa None döndürür.
    """
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.str.data.json")
    if not os.path.exists(path):
        print(f"⚠️ Yapılandırılmış veri bulunamadı: {name}.str.data.json")
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON okuma hatası '{path}': {e}")
        return None

def build_html(name, videos, structured_data, page_type="country"):
    """
    Verilen verileri kullanarak tam bir HTML sayfası oluşturur.
    Sayfa türüne (ülke, kıta, dünya geneli) göre farklı içerikler oluşturur.
    """
    readable_name = name.replace("-", " ").title()

    # Sayfa başlığı ve meta açıklaması için dinamik içerik oluşturma
    if name == "index" or name == "worldwide":
        title_suffix = "- Updated Every 3 Hours | TopTubeList"
        description_prefix = "Explore the most trending YouTube videos worldwide."
        canonical_link = "https://www.toptubelist.com/"
    else:
        title_suffix = f"in {readable_name} - Updated Every 3 Hours | TopTubeList"
        description_prefix = f"Discover the most trending YouTube videos in {readable_name}."
        canonical_link = f"https://www.toptubelist.com/{name.lower()}.html"

    # HTML body sınıfı ve panel/hamburger görünürlük ayarları
    body_class = ""
    hamburger_display = "block" # Varsayılan olarak hamburger göster
    country_panel_display = "block" # Varsayılan olarak ülke paneli göster

    # Navigasyon aktiflik sınıfları
    worldwide_active = ""
    asia_active = ""
    europe_active = ""
    africa_active = ""
    north_america_active = ""
    south_america_active = ""
    oceania_active = ""

    # Sayfa türüne göre dinamik ayarlamalar
    if page_type == "continent":
        body_class = "continent-page"
        hamburger_display = "none" # Kıta sayfasında gizle
        country_panel_display = "none" # Kıta sayfasında gizle
        # Kıta sayfasına göre aktiflik sınıfı atama
        if name == "asia": asia_active = "active"
        elif name == "europe": europe_active = "active"
        elif name == "africa": africa_active = "active"
        elif name == "north_america": north_america_active = "active"
        elif name == "south_america": south_america_active = "active"
        elif name == "oceania": oceania_active = "active"
    elif page_type == "worldwide":
        body_class = "worldwide-page"
        hamburger_display = "none" # Dünya sayfasında gizle
        country_panel_display = "none" # Dünya sayfasında gizle
        worldwide_active = "active"
    else: # page_type == "country" (varsayılan)
        body_class = "country-page"
        # Ülke sayfaları için hamburger ve ülke paneli varsayılan olarak görünür kalır.

    # Yapılandırılmış veri (Structured Data) bloğu
    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2, ensure_ascii=False)
        # Düzeltme: Structured data script etiketi doğru kapatıldı
        structured_data_block = f'<script type="application/ld+json">\n{structured_json}\n</script>'

    # Reklam (iframe) bloğu - sadece belirli sayfalarda göster
    iframe_block = ""
    if name in ["index", "worldwide", "europe", "asia"]: # Hangi sayfalarda reklam gösterileceği
        iframe_block = """
<section class="ad-section">
  <p>REKLAM ALANI</p>
</section>
"""

    # Ülke paneli HTML'i - sadece ülke sayfaları için oluşturulur
    country_panel_html = ""
    if page_type == "country":
        country_list_data = {}
        # VIDEO_DATA_DIR içindeki tüm ülke bazlı JSON dosyalarını tara
        for filename in os.listdir(VIDEO_DATA_DIR):
            if filename.endswith(".vid.data.json") and \
               filename not in [f"{n}.vid.data.json" for n in ["index", "worldwide"] + continent_names]:
                country_slug = filename.replace(".vid.data.json", "")
                country_name = country_slug.replace("-", " ").title()
                first_letter = country_name[0].upper()
                if first_letter not in country_list_data:
                    country_list_data[first_letter] = []
                country_list_data[first_letter].append({"name": country_name, "slug": country_slug})

        # Alfabe filtreleme linklerini oluştur
        alphabet_links = "".join([f'<a href="#" class="alphabet-letter" data-letter="{letter}">{letter}</a>' for letter in sorted(country_list_data.keys())])
        
        # Ülke butonlarını oluştur
        country_buttons_html = ""
        for letter in sorted(country_list_data.keys()):
            for country in sorted(country_list_data[letter], key=lambda x: x['name']):
                active_class = "active" if country['slug'] == name else ""
                country_buttons_html += f'<button class="country-button {active_class}" onclick="window.location.href=\'{country["slug"]}.html\'" data-letter="{letter}">{country["name"]}</button>'

        country_panel_html = f"""
        <div class="alphabet-filter">
            <a href="#" class="alphabet-letter active" data-letter="all">All</a>
            {alphabet_links}
        </div>
        <div class="country-list-wrapper">
            {country_buttons_html}
        </div>
        """

    # Ana HTML şablonu (f-string kullanılarak Python değişkenleri yerleştirilir)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Trending YouTube Videos {title_suffix}</title>
  <meta name="description" content="{description_prefix}">
  <meta name="keywords" content="YouTube trends {readable_name}, popular videos {readable_name}, trending YouTube, viral content">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical_link}" />
  <link rel="stylesheet" href="style.css" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103" crossorigin="anonymous"></script>
{structured_data_block}
</head>
<body class="{body_class}">

<header>
  <div class="container header-flex">
    <a href="index.html" id="logoLink">
      <img src="TopTubeListLogo.webp" alt="TopTubeList Logo" width="100" style="margin-right: 12px; vertical-align: middle;">
    </a>
    <h1>Most Viewed {title_suffix.replace(' - Updated Every 3 Hours | TopTubeList', '')}</h1>
    <button id="darkModeToggle" title="Toggle Dark Mode">🌙</button>
  </div>

  <nav id="continentNav">
    <a href="index.html" class="{worldwide_active}">Worldwide</a>
    <a href="asia.html" class="{asia_active}">Asia</a>
    <a href="europe.html" class="{europe_active}">Europe</a>
    <a href="africa.html" class="{africa_active}">Africa</a>
    <a href="north_america.html" class="{north_america_active}">North America</a>
    <a href="south_america.html" class="{south_america_active}">South America</a>
    <a href="oceania.html" class="{oceania_active}">Oceania</a>
  </nav>
</header>

<main class="main-content">
  <button id="hamburgerBtn" class="hamburger" style="display: {hamburger_display};">☰</button>
  <div class="layout-wrapper">
    <div class="country-panel" style="display: {country_panel_display};">
      {country_panel_html}
    </div>
    <div id="videoList" class="video-list">
      </div>
    <button id="loadMoreBtn" class="site-button">Load More</button>
  </div>
</main>

<section class="about-section">
  <button id="aboutToggle" class="site-button">About Us</button>
  <div id="aboutContent" style="display: none;">
    <p><strong>What is TopTubeList?</strong><br>
    TopTubeList helps you quickly see what people are watching on YouTube. You can explore videos by continent or country...</p>
    <p><strong>This is TopTubeList.</strong><br>
    If it’s trending, chances are… we’ve already listed it. 😉</p>
  </div>
</section>

{iframe_block}

<footer>
  <div class="contact-section">
    <button id="contactToggle" class="site-button">Contact Us</button>
    <div id="contactContent" style="display: none;">
      <form name="contact" id="contactForm" method="POST" data-netlify="true" netlify-honeypot="bot-field">
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
  // --- Hamburger Menü ---
  document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.querySelector(".hamburger");
    const panel = document.querySelector(".country-panel");

    if (hamburger && panel) {
      hamburger.addEventListener("click", () => {
        panel.classList.toggle("active");
      });
    }

    // --- Dark Mode Toggle ---
    const darkModeToggle = document.getElementById("darkModeToggle");
    const savedMode = localStorage.getItem("darkMode");
    if (savedMode === "true") {
      document.body.classList.add("dark-mode");
    }
    if (darkModeToggle) {
      darkModeToggle.addEventListener("click", () => {
        const isDarkNow = document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", isDarkNow);
      });
    }

    // --- Harf Filtreleme ---
    document.querySelectorAll(".alphabet-letter").forEach(letter => {
      letter.addEventListener("click", function (e) {
        e.preventDefault();
        const selectedLetter = this.getAttribute("data-letter");
        // Düzeltme: .country-column yerine .country-list-wrapper kullanıldı
        const allButtons = document.querySelectorAll(".country-list-wrapper button");

        allButtons.forEach(btn => {
          if (selectedLetter === "all" || btn.getAttribute("data-letter") === selectedLetter) {
            btn.style.display = "block";
          } else {
            btn.style.display = "none";
          }
        });

        document.querySelectorAll(".alphabet-letter").forEach(a => a.classList.remove("active"));
        this.classList.add("active");
      });
    });

    // --- FadeOut Animation ---
    const style = document.createElement("style");
    style.textContent = `
      @keyframes fadeOut {
        0% { opacity: 1; }
        80% { opacity: 1; }
        100% { opacity: 0; transform: translateY(10px); }
      }
    `;
    document.head.appendChild(style);

    // --- Contact Toggle ---
    const contactToggle = document.getElementById("contactToggle");
    const contactContent = document.getElementById("contactContent");
    if (contactToggle && contactContent) {
      contactToggle.addEventListener("click", () => {
        if (contactContent.classList.contains("show")) {
          contactContent.classList.remove("show");
          setTimeout(() => {
            contactContent.style.display = "none";
          }, 400);
        } else {
          contactContent.style.display = "block";
          setTimeout(() => {
            contactContent.classList.add("show");
            contactContent.scrollIntoView({ behavior: "smooth", block: "start" });
          }, 10);
        }
      });
    }

    // --- About Toggle ---
    const aboutToggle = document.getElementById("aboutToggle");
    const aboutContent = document.getElementById("aboutContent");
    if (aboutToggle && aboutContent) {
      aboutToggle.addEventListener("click", () => {
        if (aboutContent.classList.contains("show")) {
          aboutContent.classList.remove("show");
          setTimeout(() => {
            aboutContent.style.display = "none";
          }, 400);
        } else {
          aboutContent.style.display = "block";
          setTimeout(() => {
            aboutContent.classList.add("show");
            aboutContent.scrollIntoView({ behavior: "smooth", block: "start" });
          }, 10);
        }
      });
    }

    // --- Contact Form Submission ---
    const form = document.getElementById("contactForm");
    const statusDiv = document.getElementById("formStatus");
    if (form && statusDiv) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(formData).toString()
        })
        .then(() => {
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
        })
        .catch(() => {
          alert("❌ Mesaj gönderilemedi. Lütfen tekrar deneyin.");
        });
      });
    }

    // --- Video Render ---
    let allVideos = [];
    let displayCount = 10;
    const container = document.getElementById("videoList");
    const loadMoreBtn = document.getElementById("loadMoreBtn");

    function getPageNameFromURL() {
      const path = window.location.pathname;
      let name = path.split('/').pop().replace('.html', '').toLowerCase();
      if (name === "" || name === "index") { // index.html veya kök dizin için
          return "worldwide";
      }
      return name;
    }

    function createVideoCard(video) {
      const card = document.createElement("div");
      card.className = "video-card";
      card.innerHTML = `
        <a href="http://googleusercontent.com/youtube.com/${video.videoId}" target="_blank" rel="noopener" class="video-thumbnail">
          <img src="${video.thumbnail}" alt="${video.title}" loading="lazy" />
          <span class="duration">${video.duration || ''}</span>
        </a>
        <div class="video-info">
          <h2><a href="http://googleusercontent.com/youtube.com/${video.videoId}" target="_blank" rel="noopener">${video.title}</a></h2>
          <div class="meta">
            <span class="channel">${video.channelTitle}</span>
            <span class="views">${video.viewCount} views</span>
            <span class="date">${video.publishedAt ? new Date(video.publishedAt).toLocaleDateString() : ''}</span>
          </div>
        </div>
      `;
      return card;
    }

    function showNoDataMessage() {
      container.innerHTML = `
        <div class="no-data-message">
          <img src="no-data.svg" alt="No data" width="100">
          <h3>📊 Sorry, no trending video data for this page.</h3>
          <p>Would you like to explore other countries or continents instead?</p>
          <a href="index.html" class="site-button">Go Back to Homepage</a>
        </div>
      `;
      loadMoreBtn.style.display = "none";
    }

    function renderVideos() {
      const fragment = document.createDocumentFragment();
      const startIndex = container.children.length; // Mevcut kartların sayısı
      const videosToRender = allVideos.slice(startIndex, displayCount);

      if (videosToRender.length === 0 && allVideos.length === 0) {
        showNoDataMessage();
        return;
      }

      videosToRender.forEach(video => {
        const card = createVideoCard(video);
        fragment.appendChild(card);
      });

      container.appendChild(fragment);
      // Yeni eklenen kartlara animasyon sınıfı ekleme (isteğe bağlı)
      Array.from(container.children).slice(startIndex).forEach(card => card.classList.add("show"));

      loadMoreBtn.style.display = displayCount >= allVideos.length ? "none" : "block";
    }

    async function loadVideos() {
      const pageName = getPageNameFromURL();
      const dataFile = `${pageName}.vid.data.json`; // Python'dan gelen dosya adıyla eşleşmeli

      try {
        const response = await fetch(dataFile);
        if (!response.ok) {
            console.warn(`Veri dosyası bulunamadı veya boş: ${dataFile}`);
            throw new Error('Data not found or empty');
        }

        allVideos = await response.json();

        // Eğer veri geldiyse, başlığı güncelle
        let readableTitle = pageName.replace("-", " ").title();
        if (pageName === "worldwide") {
            readableTitle = "Worldwide";
        }
        document.title = `Trending YouTube Videos in ${readableTitle} | TopTubeList`;

        // Başlangıçta 20 video göster, eğer varsa
        displayCount = Math.min(20, allVideos.length);
        renderVideos();

      } catch (error) {
        console.error("Veri yükleme hatası:", error);
        allVideos = []; // Veri yoksa boşalt
        showNoDataMessage();
      }
    }

    loadMoreBtn.addEventListener("click", () => {
      displayCount += 10;
      renderVideos();
      window.scrollBy({ top: 300, behavior: 'smooth' });
    });

    loadVideos();
  });
</script>

</body>
</html>
"""

    return html

# -----------------------------------------------------------------------------
# Ana Çalışma Bloğu
# -----------------------------------------------------------------------------

# Bu liste, hangi HTML sayfalarının oluşturulacağını belirler.
# Mevcut .vid.data.json ve .str.data.json dosyalarınızın isimlerine göre
# bu listeyi güncellediğinizden emin olun.
# 'index' ana sayfa için, 'worldwide' dünya geneli için kullanılır.
page_names_to_generate = [
    "index", # Ana sayfa (index.html)
    "worldwide", # Dünya geneli sayfa (worldwide.html)
    "asia", "europe", "africa", "north_america", "south_america", "oceania", # Kıtalar
    # Buradan sonra alfabetik sıraya göre tüm ülkeleri ekleyebilirsiniz.
    # Örnek: "afghanistan", "albania", "turkey", "united-states" gibi.
    "afghanistan", "albania", "algeria", "andorra", "angola", "antigua-and-barbuda",
    "argentina", "armenia", "australia", "austria", "azerbaijan", "bahamas",
    "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize",
    "benin", "bhutan", "bolivia", "bosnia-and-herzegovina", "botswana", "brazil",
    "brunei", "bulgaria", "burkina-faso", "burundi", "cabo-verde", "cambodia",
    "cameroon", "canada", "central-african-republic", "chad", "chile", "china",
    "colombia", "comoros", "congo-democratic-republic-of-the", "congo-republic-of-the",
    "costa-rica", "cote-d-ivoire", "croatia", "cuba", "cyprus", "czech-republic",
    "denmark", "djibouti", "dominica", "dominican-republic", "east-timor", "ecuador",
    "egypt", "el-salvador", "equatorial-guinea", "eritrea", "estonia", "eswatini",
    "ethiopia", "fiji", "finland", "france", "gabon", "gambia", "georgia",
    "germany", "ghana", "greece", "grenada", "guatemala", "guinea",
    "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland",
    "india", "indonesia", "iran", "iraq", "ireland", "israel", "italy",
    "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati",
    "korea-north", "korea-south", "kosovo", "kuwait", "kyrgyzstan", "laos",
    "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein",
    "lithuania", "luxembourg", "madagascar", "malawi", "malaysia", "maldives",
    "mali", "malta", "marshall-islands", "mauritania", "mauritius", "mexico",
    "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco",
    "mozambique", "myanmar", "namibia", "nauru", "nepal", "netherlands",
    "new-zealand", "nicaragua", "niger", "nigeria", "north-macedonia", "norway",
    "oman", "pakistan", "palau", "palestine", "panama", "papua-new-guinea",
    "paraguay", "peru", "philippines", "poland", "portugal", "qatar",
    "romania", "russia", "rwanda", "saint-kitts-and-nevis", "saint-lucia",
    "saint-vincent-and-the-grenadines", "samoa", "san-marino", "sao-tome-and-principe",
    "saudi-arabia", "senegal", "serbia", "seychelles", "sierra-leone", "singapore",
    "slovakia", "slovenia", "solomon-islands", "somalia", "south-africa", "south-sudan",
    "spain", "sri-lanka", "sudan", "suriname", "sweden", "switzerland", "syria",
    "taiwan", "tajikistan", "tanzania", "thailand", "togo", "tonga",
    "trinidad-and-tobago", "tunisia", "turkey", "turkmenistan", "tuvalu", "uganda",
    "ukraine", "united-arab-emirates", "united-kingdom", "united-states", "uruguay",
    "uzbekistan", "vanuatu", "vatican-city", "venezuela", "vietnam", "yemen",
    "zambia", "zimbabwe"
]

# Kıta isimleri listesi (build_html içinde kullanılır)
continent_names = ["asia", "europe", "africa", "north_america", "south_america", "oceania"]


if __name__ == "__main__":
    # Oluşturulacak her sayfa adı için döngü
    for name in page_names_to_generate:
        videos = load_video_data(name)
        structured = load_structured_data(name)

        # Sayfa türünü belirleme
        page_type = "country"
        if name == "index" or name == "worldwide":
            page_type = "worldwide"
        elif name in continent_names:
            page_type = "continent"

        # HTML içeriğini oluşturma
        html = build_html(name, videos, structured, page_type=page_type)

        # Çıktı dosya adını belirleme (index.html için özel durum)
        output_filename = f"{name}.html"
        if name == "index":
            output_filename = "index.html"

        # HTML dosyasını kaydetme
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ HTML oluşturuldu: {output_path}")