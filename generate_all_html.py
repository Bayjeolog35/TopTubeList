import os
import json

VIDEO_DATA_DIR = "."  # Video JSON'larının bulunduğu dizin
OUTPUT_DIR = "."      # Çıktı dizini (kök dizin)

def load_video_data(name):
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.vid.data.json")
    if not os.path.exists(path):
        print(f"⛔ Video verisi yok: {name}")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_structured_data(name):
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.str.data.json")
    if not os.path.exists(path):
        print(f"⚠️ Structured data bulunamadı: {name}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Ülke panelini burada global olarak tanımla
# Bu kısım, tüm HTML dosyalarında aynı ülke listesinin görünmesini sağlar.
country_panel_html = """
<div class="country-panel">
  <div class="alphabet-column"> <a href="#" class="alphabet-letter" data-letter="all">All</a>
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
  <div class="country-list-wrapper">
    <button onclick="location.href='afghanistan.html'" data-letter="A">Afghanistan</button>
    <button onclick="location.href='albania.html'" data-letter="A">Albania</button>
    <button onclick="location.href='algeria.html'" data-letter="A">Algeria</button>
    <button onclick="location.href='andorra.html'" data-letter="A">Andorra</button>
    <button onclick="location.href='angola.html'" data-letter="A">Angola</button>
    <button onclick="location.href='antigua-and-barbuda.html'" data-letter="A">Antigua and Barbuda</button>
    <button onclick="location.href='argentina.html'" data-letter="A">Argentina</button>
    <button onclick="location.href='armenia.html'" data-letter="A">Armenia</button>
    <button onclick="location.href='australia.html'" data-letter="A">Australia</button>
    <button onclick="location.href='austria.html'" data-letter="A">Austria</button>
    <button onclick="location.href='azerbaijan.html'" data-letter="A">Azerbaijan</button>

    <button onclick="location.href='bahamas.html'" data-letter="B">Bahamas</button>
    <button onclick="location.href='bahrain.html'" data-letter="B">Bahrain</button>
    <button onclick="location.href='bangladesh.html'" data-letter="B">Bangladesh</button>
    <button onclick="location.href='barbados.html'" data-letter="B">Barbados</button>
    <button onclick="location.href='belarus.html'" data-letter="B">Belarus</button>
    <button onclick="location.href='belgium.html'" data-letter="B">Belgium</button>
    <button onclick="location.href='belize.html'" data-letter="B">Belize</button>
    <button onclick="location.href='benin.html'" data-letter="B">Benin</button>
    <button onclick="location.href='bhutan.html'" data-letter="B">Bhutan</button>
    <button onclick="location.href='bolivia.html'" data-letter="B">Bolivia</button>
    <button onclick="location.href='bosnia-and-herzegovina.html'" data-letter="B">Bosnia and Herzegovina</button>
    <button onclick="location.href='botswana.html'" data-letter="B">Botswana</button>
    <button onclick="location.href='brazil.html'" data-letter="B">Brazil</button>
    <button onclick="location.href='brunei.html'" data-letter="B">Brunei</button>
    <button onclick="location.href='bulgaria.html'" data-letter="B">Bulgaria</button>
    <button onclick="location.href='burkina-faso.html'" data-letter="B">Burkina Faso</button>
    <button onclick="location.href='burundi.html'" data-letter="B">Burundi</button>

    <button onclick="location.href='cabo-verde.html'" data-letter="C">Cabo Verde</button>
    <button onclick="location.href='cambodia.html'" data-letter="C">Cambodia</button>
    <button onclick="location.href='cameroon.html'" data-letter="C">Cameroon</button>
    <button onclick="location.href='canada.html'" data-letter="C">Canada</button>
    <button onclick="location.href='central-african-republic.html'" data-letter="C">Central African Republic</button>
    <button onclick="location.href='chad.html'" data-letter="C">Chad</button>
    <button onclick="location.href='chile.html'" data-letter="C">Chile</button>
    <button onclick="location.href='china.html'" data-letter="C">China</button>
    <button onclick="location.href='colombia.html'" data-letter="C">Colombia</button>
    <button onclick="location.href='comoros.html'" data-letter="C">Comoros</button>
    <button onclick="location.href='congo-democratic-republic-of-the.html'" data-letter="C">Congo (Democratic Republic of the)</button>
    <button onclick="location.href='congo-republic-of-the.html'" data-letter="C">Congo (Republic of the)</button>
    <button onclick="location.href='costa-rica.html'" data-letter="C">Costa Rica</button>
    <button onclick="location.href='cote-d-ivoire.html'" data-letter="C">Cote d'Ivoire</button>
    <button onclick="location.href='croatia.html'" data-letter="C">Croatia</button>
    <button onclick="location.href='cuba.html'" data-letter="C">Cuba</button>
    <button onclick="location.href='cyprus.html'" data-letter="C">Cyprus</button>
    <button onclick="location.href='czech-republic.html'" data-letter="C">Czech Republic</button>

    <button onclick="location.href='denmark.html'" data-letter="D">Denmark</button>
    <button onclick="location.href='djibouti.html'" data-letter="D">Djibouti</button>
    <button onclick="location.href='dominica.html'" data-letter="D">Dominica</button>
    <button onclick="location.href='dominican-republic.html'" data-letter="D">Dominican Republic</button>

    <button onclick="location.href='east-timor.html'" data-letter="E">East Timor</button>
    <button onclick="location.href='ecuador.html'" data-letter="E">Ecuador</button>
    <button onclick="location.href='egypt.html'" data-letter="E">Egypt</button>
    <button onclick="location.href='el-salvador.html'" data-letter="E">El Salvador</button>
    <button onclick="location.href='equatorial-guinea.html'" data-letter="E">Equatorial Guinea</button>
    <button onclick="location.href='eritrea.html'" data-letter="E">Eritrea</button>
    <button onclick="location.href='estonia.html'" data-letter="E">Estonia</button>
    <button onclick="location.href='eswatini.html'" data-letter="E">Eswatini</button>
    <button onclick="location.href='ethiopia.html'" data-letter="E">Ethiopia</button>

    <button onclick="location.href='fiji.html'" data-letter="F">Fiji</button>
    <button onclick="location.href='finland.html'" data-letter="F">Finland</button>
    <button onclick="location.href='france.html'" data-letter="F">France</button>

    <button onclick="location.href='gabon.html'" data-letter="G">Gabon</button>
    <button onclick="location.href='gambia.html'" data-letter="G">Gambia</button>
    <button onclick="location.href='georgia.html'" data-letter="G">Georgia</button>
    <button onclick="location.href='germany.html'" data-letter="G">Germany</button>
    <button onclick="location.href='ghana.html'" data-letter="G">Ghana</button>
    <button onclick="location.href='greece.html'" data-letter="G">Greece</button>
    <button onclick="location.href='grenada.html'" data-letter="G">Grenada</button>
    <button onclick="location.href='guatemala.html'" data-letter="G">Guatemala</button>
    <button onclick="location.href='guinea.html'" data-letter="G">Guinea</button>
    <button onclick="location.href='guinea-bissau.html'" data-letter="G">Guinea-Bissau</button>
    <button onclick="location.href='guyana.html'" data-letter="G">Guyana</button>

    <button onclick="location.href='haiti.html'" data-letter="H">Haiti</button>
    <button onclick="location.href='honduras.html'" data-letter="H">Honduras</button>
    <button onclick="location.href='hungary.html'" data-letter="H">Hungary</button>

    <button onclick="location.href='iceland.html'" data-letter="I">Iceland</button>
    <button onclick="location.href='india.html'" data-letter="I">India</button>
    <button onclick="location.href='indonesia.html'" data-letter="I">Indonesia</button>
    <button onclick="location.href='iran.html'" data-letter="I">Iran</button>
    <button onclick="location.href='iraq.html'" data-letter="I">Iraq</button>
    <button onclick="location.href='ireland.html'" data-letter="I">Ireland</button>
    <button onclick="location.href='israel.html'" data-letter="I">Israel</button>
    <button onclick="location.href='italy.html'" data-letter="I">Italy</button>

    <button onclick="location.href='jamaica.html'" data-letter="J">Jamaica</button>
    <button onclick="location.href='japan.html'" data-letter="J">Japan</button>
    <button onclick="location.href='jordan.html'" data-letter="J">Jordan</button>

    <button onclick="location.href='kazakhstan.html'" data-letter="K">Kazakhstan</button>
    <button onclick="location.href='kenya.html'" data-letter="K">Kenya</button>
    <button onclick="location.href='kiribati.html'" data-letter="K">Kiribati</button>
    <button onclick="location.href='korea-north.html'" data-letter="K">Korea (North)</button>
    <button onclick="location.href='korea-south.html'" data-letter="K">Korea (South)</button>
    <button onclick="location.href='kosovo.html'" data-letter="K">Kosovo</button>
    <button onclick="location.href='kuwait.html'" data-letter="K">Kuwait</button>
    <button onclick="location.href='kyrgyzstan.html'" data-letter="K">Kyrgyzstan</button>

    <button onclick="location.href='laos.html'" data-letter="L">Laos</button>
    <button onclick="location.href='latvia.html'" data-letter="L">Latvia</button>
    <button onclick="location.href='lebanon.html'" data-letter="L">Lebanon</button>
    <button onclick="location.href='lesotho.html'" data-letter="L">Lesotho</button>
    <button onclick="location.href='liberia.html'" data-letter="L">Liberia</button>
    <button onclick="location.href='libya.html'" data-letter="L">Libya</button>
    <button onclick="location.href='liechtenstein.html'" data-letter="L">Liechtenstein</button>
    <button onclick="location.href='lithuania.html'" data-letter="L">Lithuania</button>
    <button onclick="location.href='luxembourg.html'" data-letter="L">Luxembourg</button>

    <button onclick="location.href='madagascar.html'" data-letter="M">Madagascar</button>
    <button onclick="location.href='malawi.html'" data-letter="M">Malawi</button>
    <button onclick="location.href='malaysia.html'" data-letter="M">Malaysia</button>
    <button onclick="location.href='maldives.html'" data-letter="M">Maldives</button>
    <button onclick="location.href='mali.html'" data-letter="M">Mali</button>
    <button onclick="location.href='malta.html'" data-letter="M">Malta</button>
    <button onclick="location.href='marshall-islands.html'" data-letter="M">Marshall Islands</button>
    <button onclick="location.href='mauritania.html'" data-letter="M">Mauritania</button>
    <button onclick="location.href='mauritius.html'" data-letter="M">Mauritius</button>
    <button onclick="location.href='mexico.html'" data-letter="M">Mexico</button>
    <button onclick="location.href='micronesia.html'" data-letter="M">Micronesia</button>
    <button onclick="location.href='moldova.html'" data-letter="M">Moldova</button>
    <button onclick="location.href='monaco.html'" data-letter="M">Monaco</button>
    <button onclick="location.href='mongolia.html'" data-letter="M">Mongolia</button>
    <button onclick="location.href='montenegro.html'" data-letter="M">Montenegro</button>
    <button onclick="location.href='morocco.html'" data-letter="M">Morocco</button>
    <button onclick="location.href='mozambique.html'" data-letter="M">Mozambique</button>
    <button onclick="location.href='myanmar.html'" data-letter="M">Myanmar</button>

    <button onclick="location.href='namibia.html'" data-letter="N">Namibia</button>
    <button onclick="location.href='nauru.html'" data-letter="N">Nauru</button>
    <button onclick="location.href='nepal.html'" data-letter="N">Nepal</button>
    <button onclick="location.href='netherlands.html'" data-letter="N">Netherlands</button>
    <button onclick="location.href='new-zealand.html'" data-letter="N">New Zealand</button>
    <button onclick="location.href='nicaragua.html'" data-letter="N">Nicaragua</button>
    <button onclick="location.href='niger.html'" data-letter="N">Niger</button>
    <button onclick="location.href='nigeria.html'" data-letter="N">Nigeria</button>
    <button onclick="location.href='north-macedonia.html'" data-letter="N">North Macedonia</button>
    <button onclick="location.href='norway.html'" data-letter="N">Norway</button>

    <button onclick="location.href='oman.html'" data-letter="O">Oman</button>

    <button onclick="location.href='pakistan.html'" data-letter="P">Pakistan</button>
    <button onclick="location.href='palau.html'" data-letter="P">Palau</button>
    <button onclick="location.href='palestine.html'" data-letter="P">Palestine</button>
    <button onclick="location.href='panama.html'" data-letter="P">Panama</button>
    <button onclick="location.href='papua-new-guinea.html'" data-letter="P">Papua New Guinea</button>
    <button onclick="location.href='paraguay.html'" data-letter="P">Paraguay</button>
    <button onclick="location.href='peru.html'" data-letter="P">Peru</button>
    <button onclick="location.href='philippines.html'" data-letter="P">Philippines</button>
    <button onclick="location.href='poland.html'" data-letter="P">Poland</button>
    <button onclick="location.href='portugal.html'" data-letter="P">Portugal</button>

    <button onclick="location.href='qatar.html'" data-letter="Q">Qatar</button>

    <button onclick="location.href='romania.html'" data-letter="R">Romania</button>
    <button onclick="location.href='russia.html'" data-letter="R">Russia</button>
    <button onclick="location.href='rwanda.html'" data-letter="R">Rwanda</button>

    <button onclick="location.href='saint-kitts-and-nevis.html'" data-letter="S">Saint Kitts and Nevis</button>
    <button onclick="location.href='saint-lucia.html'" data-letter="S">Saint Lucia</button>
    <button onclick="location.href='saint-vincent-and-the-grenadines.html'" data-letter="S">Saint Vincent and the Grenadines</button>
    <button onclick="location.href='samoa.html'" data-letter="S">Samoa</button>
    <button onclick="location.href='san-marino.html'" data-letter="S">San Marino</button>
    <button onclick="location.href='sao-tome-and-principe.html'" data-letter="S">Sao Tome and Principe</button>
    <button onclick="location.href='saudi-arabia.html'" data-letter="S">Saudi Arabia</button>
    <button onclick="location.href='senegal.html'" data-letter="S">Senegal</button>
    <button onclick="location.href='serbia.html'" data-letter="S">Serbia</button>
    <button onclick="location.href='seychelles.html'" data-letter="S">Seychelles</button>
    <button onclick="location.href='sierra-leone.html'" data-letter="S">Sierra Leone</button>
    <button onclick="location.href='singapore.html'" data-letter="S">Singapore</button>
    <button onclick="location.href='slovakia.html'" data-letter="S">Slovakia</button>
    <button onclick="location.href='slovenia.html'" data-letter="S">Slovenia</button>
    <button onclick="location.href='solomon-islands.html'" data-letter="S">Solomon Islands</button>
    <button onclick="location.href='somalia.html'" data-letter="S">Somalia</button>
    <button onclick="location.href='south-africa.html'" data-letter="S">South Africa</button>
    <button onclick="location.href='south-sudan.html'" data-letter="S">South Sudan</button>
    <button onclick="location.href='spain.html'" data-letter="S">Spain</button>
    <button onclick="location.href='sri-lanka.html'" data-letter="S">Sri Lanka</button>
    <button onclick="location.href='sudan.html'" data-letter="S">Sudan</button>
    <button onclick="location.href='suriname.html'" data-letter="S">Suriname</button>
    <button onclick="location.href='sweden.html'" data-letter="S">Sweden</button>
    <button onclick="location.href='switzerland.html'" data-letter="S">Switzerland</button>
    <button onclick="location.href='syria.html'" data-letter="S">Syria</button>

    <button onclick="location.href='taiwan.html'" data-letter="T">Taiwan</button>
    <button onclick="location.href='tajikistan.html'" data-letter="T">Tajikistan</button>
    <button onclick="location.href='tanzania.html'" data-letter="T">Tanzania</button>
    <button onclick="location.href='thailand.html'" data-letter="T">Thailand</button>
    <button onclick="location.href='togo.html'" data-letter="T">Togo</button>
    <button onclick="location.href='tonga.html'" data-letter="T">Tonga</button>
    <button onclick="location.href='trinidad-and-tobago.html'" data-letter="T">Trinidad and Tobago</button>
    <button onclick="location.href='tunisia.html'" data-letter="T">Tunisia</button>
    <button onclick="location.href='turkey.html'" data-letter="T">Turkey</button>
    <button onclick="location.href='turkmenistan.html'" data-letter="T">Turkmenistan</button>
    <button onclick="location.href='tuvalu.html'" data-letter="T">Tuvalu</button>

    <button onclick="location.href='uganda.html'" data-letter="U">Uganda</button>
    <button onclick="location.href='ukraine.html'" data-letter="U">Ukraine</button>
    <button onclick="location.href='united-arab-emirates.html'" data-letter="U">United Arab Emirates</button>
    <button onclick="location.href='united-kingdom.html'" data-letter="U">United Kingdom</button>
    <button onclick="location.href='united-states.html'" data-letter="U">United States</button>
    <button onclick="location.href='uruguay.html'" data-letter="U">Uruguay</button>
    <button onclick="location.href='uzbekistan.html'" data-letter="U">Uzbekistan</button>

    <button onclick="location.href='vanuatu.html'" data-letter="V">Vanuatu</button>
    <button onclick="location.href='vatican-city.html'" data-letter="V">Vatican City</button>
    <button onclick="location.href='venezuela.html'" data-letter="V">Venezuela</button>
    <button onclick="location.href='vietnam.html'" data-letter="V">Vietnam</button>

    <button onclick="location.href='yemen.html'" data-letter="Y">Yemen</button>

    <button onclick="location.href='zambia.html'" data-letter="Z">Zambia</button>
    <button onclick="location.href='zimbabwe.html'" data-letter="Z">Zimbabwe</button>
  </div>
</div>
"""

def build_html(name, videos, structured_data, page_type="country"):
    """
    Belirtilen 'name' için HTML sayfasını oluşturur.
    page_type: "country", "continent" veya "worldwide" olabilir.
    """
    readable_name = name.replace("-", " ").title()
    title_suffix = ""
    description_prefix = ""
    canonical_link = f"https://toptubelist.com/{name}.html"
    body_class = "" # Herhangi bir özel body sınıfı gerekirse

    if page_type == "country":
        title_suffix = f"in {readable_name} - Updated Every 3 Hours | TopTubeList"
        description_prefix = f"Watch the most popular YouTube videos trending across {readable_name}. Stay current with viral content."
        body_class = "country-page"
    elif page_type == "continent":
        title_suffix = f"in {readable_name} - Updated Every 3 Hours | TopTubeList"
        description_prefix = f"Explore the most popular YouTube videos trending across the continent of {readable_name}. Stay current with viral content."
        body_class = "continent-page"
    elif page_type == "worldwide":
        readable_name = "Worldwide" # Ana sayfa için başlığı "Worldwide" yap
        title_suffix = "- Updated Every 3 Hours | TopTubeList"
        description_prefix = "Watch the most popular YouTube videos trending worldwide. Stay current with viral content."
        canonical_link = "https://toptubelist.com/index.html"
        body_class = "worldwide-page"


    # Structured Data (JSON-LD Script Bloğu)
    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2, ensure_ascii=False)
        structured_data_block = f"""
  <script type="application/ld+json">
{structured_json}
  </script>
"""

    # iframe: İlk videodan embedUrl ve title çek
    # Bu iframe'i gizli tutuyoruz (position:absolute; width:1px; height:1px; left:-9999px;)
    # Sadece structured data'da olması istenen video için kullanılıyor olabilir.
    iframe_block = ""
    if structured_data and isinstance(structured_data, list) and len(structured_data) > 0:
        first_video = structured_data[0]
        embed_url = first_video.get("embedUrl", "")
        video_title = first_video.get("name", "")
        if embed_url:
            iframe_block = f"""
<iframe
  width="560"
  height="315"
  src="{embed_url}"
  title="{video_title}"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>
"""

    # Video Kartları (Bu kısım JavaScript tarafından doldurulacak, HTML'de boş kalmalı)
    # Daha önce burada olan döngüyü kaldırdık, çünkü JS dinamiği sağlıyor.
    video_cards_html = "" # Bu kısım boş bırakılacak

    # Continent Nav 'active' sınıfını belirle
    asia_active = 'active' if name == 'asia' else ''
    europe_active = 'active' if name == 'europe' else ''
    africa_active = 'active' if name == 'africa' else ''
    north_america_active = 'active' if name == 'north_america' else ''
    south_america_active = 'active' if name == 'south_america' else ''
    oceania_active = 'active' if name == 'oceania' else ''
    worldwide_active = 'active' if name == 'index' or name == 'worldwide' else '' # 'index' ana sayfa için

    # Ana sayfa (worldwide) için ülke panelini gizle, kıtalar ve ülkeler için göster.
    # Ayrıca kıta sayfaları için de hamburger butonunu ve ülke panelini gösteriyoruz.
    country_panel_display = "block"
    hamburger_display = "block"
    if page_type == "worldwide":
        country_panel_display = "none"
        hamburger_display = "none"


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
    // Düzeltme: HTML formuna id="contactForm" eklendi
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
        <a href="https://www.youtube.com/watch?v=${video.videoId}" target="_blank" rel="noopener" class="video-thumbnail">
          <img src="${video.thumbnail}" alt="${video.title}" loading="lazy" />
          <span class="duration">${video.duration || ''}</span>
        </a>
        <div class="video-info">
          <h2><a href="https://www.youtube.com/watch?v=${video.videoId}" target="_blank" rel="noopener">${video.title}</a></h2>
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
      // container.innerHTML = ""; // Yalnızca ilk yüklemede veya filtrelemede temizlenmeli, append için değil

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
        // setTimeout(() => card.classList.add("show"), 50); // Kartları yavaş yavaş göstermek isterseniz
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

# Ülkeler, Kıtalar ve Worldwide için HTML dosyalarını oluşturma
# Örnek isim listesi (mevcut .vid.data.json dosyalarınıza göre ayarlanmalı)
# 'index' veya 'worldwide' .vid.data.json dosyası 'index.vid.data.json' veya 'worldwide.vid.data.json' olabilir.
# Lütfen sahip olduğunuz JSON dosyası adlarına göre bu listeyi güncelleyin.
# Örneğin: "index.vid.data.json", "turkey.vid.data.json", "asia.vid.data.json"
page_names_to_generate = [
    "index", # Ana sayfa için
    "worldwide", # Eğer worldwide için ayrı bir dosya adı kullanılıyorsa
    "asia", "europe", "africa", "north_america", "south_america", "oceania", # Kıtalar
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

continent_names = ["asia", "europe", "africa", "north_america", "south_america", "oceania"]


for name in page_names_to_generate:
    videos = load_video_data(name)
    structured = load_structured_data(name)

    page_type = "country"
    if name == "index" or name == "worldwide":
        page_type = "worldwide"
    elif name in continent_names:
        page_type = "continent"

    html = build_html(name, videos, structured, page_type=page_type)

    output_filename = f"{name}.html"
    if name == "index": # Ana sayfa için özel durum
        output_filename = "index.html"

    output_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML oluşturuldu: {output_path}")