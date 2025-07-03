import json
import os
import re

# Bu COUNTRY_INFO sözlüğünü gerçek verilerinizle güncellemeyi unutmayın.
# Eğer API'den gelen kodlarda veya display-name'lerde farklılık varsa, burayı düzeltin.
COUNTRY_INFO = {
    "afghanistan": {"code": "AF"},
    "albania": {"code": "AL"},
    "algeria": {"code": "DZ"},
    "andorra": {"code": "AD"},
    "angola": {"code": "AO"},
    "argentina": {"code": "AR"},
    "armenia": {"code": "AM"},
    "australia": {"code": "AU"},
    "austria": {"code": "AT"},
    "azerbaijan": {"code": "AZ"},
    "bahamas": {"code": "BS"},
    "bahrain": {"code": "BH"},
    "bangladesh": {"code": "BD"},
    "barbados": {"code": "BB"},
    "belarus": {"code": "BY"},
    "belgium": {"code": "BE"},
    "belize": {"code": "BZ"},
    "benin": {"code": "BJ"},
    "bhutan": {"code": "BT"},
    "bolivia": {"code": "BO"},
    "bosnia-and-herzegovina": {"code": "BA", "display_name": "Bosnia and Herzegovina"},
    "botswana": {"code": "BW"},
    "brazil": {"code": "BR"},
    "brunei": {"code": "BN"},
    "bulgaria": {"code": "BG"},
    "burkina-faso": {"code": "BF", "display_name": "Burkina Faso"},
    "burundi": {"code": "BI"}, # Bı -> BI düzeltildi
    "cabo-verde": {"code": "CV", "display_name": "Cabo Verde"},
    "cambodia": {"code": "KH"},
    "cameroon": {"code": "CM"},
    "canada": {"code": "CA"},
    "central-african-republic": {"code": "CF", "display_name": "Central African Republic"},
    "chad": {"code": "TD"},
    "chile": {"code": "CL"},
    "china": {"code": "CN"},
    "colombia": {"code": "CO"},
    "comoros": {"code": "KM"},
    "congo-democratic-republicofthe": {"code": "CD", "display_name": "Congo (Democratic Republic of the)"},
    "congo-republic-of-the": {"code": "CG", "display_name": "Congo (Republic of the)"},
    "costa-rica": {"code": "CR", "display_name": "Costa Rica"},
    "cote-divoire": {"code": "CI", "display_name": "Cote d'Ivoire"}, # ıvoire -> ivoire düzeltildi
    "croatia": {"code": "HR"},
    "cuba": {"code": "CU"},
    "cyprus": {"code": "CY"},
    "czech-republic": {"code": "CZ", "display_name": "Czech Republic"},
    "denmark": {"code": "DK"},
    "djibouti": {"code": "DJ"},
    "dominica": {"code": "DM"},
    "dominican-republic": {"code": "DO", "display_name": "Dominican Republic"},
    "east-timor": {"code": "TL", "display_name": "East Timor"},
    "ecuador": {"code": "EC"},
    "egypt": {"code": "EG"},
    "el-salvador": {"code": "SV", "display_name": "El Salvador"}, # elsalvador -> el-salvador düzeltildi
    "equatorial-guinea": {"code": "GQ", "display_name": "Equatorial Guinea"},
    "eritrea": {"code": "ER"},
    "estonia": {"code": "EE"},
    "eswatini": {"code": "SZ"},
    "ethiopia": {"code": "ET"},
    "fiji": {"code": "FJ"},
    "finland": {"code": "FI"}, # fı -> FI düzeltildi
    "france": {"code": "FR"},
    "gabon": {"code": "GA"},
    "gambia": {"code": "GM"},
    "georgia": {"code": "GE"},
    "germany": {"code": "DE"},
    "ghana": {"code": "GH"},
    "greece": {"code": "GR"},
    "grenada": {"code": "GD"},
    "guatemala": {"code": "GT"},
    "guinea": {"code": "GN"},
    "guinea-bissau": {"code": "GW", "display_name": "Guinea-Bissau"},
    "guyana": {"code": "GY"},
    "haiti": {"code": "HT"},
    "honduras": {"code": "HN"},
    "hungary": {"code": "HU"},
    "iceland": {"code": "IS"}, # ıceland -> iceland, ıs -> IS düzeltildi
    "india": {"code": "IN"}, # ındia -> india düzeltildi
    "indonesia": {"code": "ID"}, # ındonesia -> indonesia, ıd -> ID düzeltildi
    "iran": {"code": "IR"}, # ıran -> iran, ır -> IR düzeltildi
    "iraq": {"code": "IQ"}, # ıraq -> iraq, ıq -> IQ düzeltildi
    "ireland": {"code": "IE"}, # ıreland -> ireland, ıe -> IE düzeltildi
    "israel": {"code": "IL"}, # ısrael -> israel düzeltildi
    "italy": {"code": "IT"}, # ıtaly -> italy, ıt -> IT düzeltildi
    "jamaica": {"code": "JM"},
    "japan": {"code": "JP"},
    "jordan": {"code": "JO"},
    "kazakhstan": {"code": "KZ"},
    "kenya": {"code": "KE"},
    "kiribati": {"code": "KI"}, # kı -> KI düzeltildi
    "korea-north": {"code": "KP", "display_name": "Korea (North)"},
    "korea-south": {"code": "KR", "display_name": "Korea (South)"},
    "kosovo": {"code": "XK", "display_name": "Kosovo"},
    "kuwait": {"code": "KW"},
    "kyrgyzstan": {"code": "KG"},
    "laos": {"code": "LA"},
    "latvia": {"code": "LV"},
    "lebanon": {"code": "LB"},
    "lesotho": {"code": "LS"},
    "liberia": {"code": "LR"},
    "libya": {"code": "LY"},
    "liechtenstein": {"code": "LI"}, # lı -> LI düzeltildi
    "lithuania": {"code": "LT"},
    "luxembourg": {"code": "LU"},
    "madagascar": {"code": "MG"},
    "malawi": {"code": "MW"},
    "malaysia": {"code": "MY"},
    "maldives": {"code": "MV"},
    "mali": {"code": "ML"},
    "malta": {"code": "MT"},
    "marshall-islands": {"code": "MH", "display_name": "Marshall Islands"}, # ıslands -> islands düzeltildi
    "mauritania": {"code": "MR"},
    "mauritius": {"code": "MU"},
    "mexico": {"code": "MX"},
    "micronesia": {"code": "FM"},
    "moldova": {"code": "MD"},
    "monaco": {"code": "MC"},
    "mongolia": {"code": "MN"},
    "montenegro": {"code": "ME"},
    "morocco": {"code": "MA"},
    "mozambique": {"code": "MZ"},
    "myanmar": {"code": "MM"},
    "namibia": {"code": "NA"},
    "nauru": {"code": "NR"},
    "nepal": {"code": "NP"},
    "netherlands": {"code": "NL"},
    "new-zealand": {"code": "NZ", "display_name": "New Zealand"},
    "nicaragua": {"code": "NI"}, # nı -> NI düzeltildi
    "niger": {"code": "NE"},
    "nigeria": {"code": "NG"},
    "north-macedonia": {"code": "MK", "display_name": "North Macedonia"},
    "norway": {"code": "NO"},
    "oman": {"code": "OM"},
    "pakistan": {"code": "PK"},
    "palau": {"code": "PW"},
    "palestine": {"code": "PS"},
    "panama": {"code": "PA"},
    "papua-new-guinea": {"code": "PG", "display_name": "Papua New Guinea"},
    "paraguay": {"code": "PY"},
    "peru": {"code": "PE"},
    "philippines": {"code": "PH"},
    "poland": {"code": "PL"},
    "portugal": {"code": "PT"},
    "qatar": {"code": "QA"},
    "romania": {"code": "RO"},
    "russia": {"code": "RU"},
    "rwanda": {"code": "RW"},
    "saint-kitts-and-nevis": {"code": "KN", "display_name": "Saint Kitts and Nevis"},
    "saint-lucia": {"code": "LC", "display_name": "Saint Lucia"},
    "saint-vincent-and-the-grenadines": {"code": "VC", "display_name": "Saint Vincent and the Grenadines"},
    "samoa": {"code": "WS"},
    "san-marino": {"code": "SM", "display_name": "San Marino"},
    "sao-tome-and-principe": {"code": "ST", "display_name": "Sao Tome and Principe"},
    "saudi-arabia": {"code": "SA", "display_name": "Saudi Arabia"},
    "senegal": {"code": "SN"},
    "serbia": {"code": "RS"},
    "seychelles": {"code": "SC"},
    "sierra-leone": {"code": "SL", "display_name": "Sierra Leone"},
    "singapore": {"code": "SG"},
    "slovakia": {"code": "SK"},
    "slovenia": {"code": "SI"}, # sı -> SI düzeltildi
    "solomon-islands": {"code": "SB", "display_name": "Solomon Islands"}, # ıslands -> islands düzeltildi
    "somalia": {"code": "SO"},
    "south-africa": {"code": "ZA", "display_name": "South Africa"},
    "south-sudan": {"code": "SS", "display_name": "South Sudan"},
    "spain": {"code": "ES"},
    "sri-lanka": {"code": "LK", "display_name": "Sri Lanka"},
    "sudan": {"code": "SD"},
    "suriname": {"code": "SR"},
    "sweden": {"code": "SE"},
    "switzerland": {"code": "CH"},
    "syria": {"code": "SY"},
    "taiwan": {"code": "TW"},
    "tajikistan": {"code": "TJ"},
    "tanzania": {"code": "TZ"},
    "thailand": {"code": "TH"},
    "togo": {"code": "TG"},
    "tonga": {"code": "TO"},
    "trinidad-and-tobago": {"code": "TT", "display_name": "Trinidad and Tobago"},
    "tunisia": {"code": "TN"},
    "turkey": {"code": "TR"},
    "turkmenistan": {"code": "TM"},
    "tuvalu": {"code": "TV"},
    "uganda": {"code": "UG"},
    "ukraine": {"code": "UA"},
    "united-arab-emirates": {"code": "AE", "display_name": "United Arab Emirates"},
    "united-kingdom": {"code": "GB", "display_name": "United Kingdom"},
    "united-states": {"code": "US", "display_name": "United States"},
    "uruguay": {"code": "UY"},
    "uzbekistan": {"code": "UZ"},
    "vanuatu": {"code": "VU"},
    "vatican-city": {"code": "VA", "display_name": "Vatican City"},
    "venezuela": {"code": "VE"},
    "vietnam": {"code": "VN"},
    "yemen": {"code": "YE"},
    "zambia": {"code": "ZM"},
    "zimbabwe": {"code": "ZW"}
}

# Kıta bilgilerini ekliyoruz. Bu listelerin COUNTRY_INFO'daki 'code' değerleriyle eşleştiğinden emin olun.
# Örnek olarak bazılarını ekledim, tamamını projenize göre doldurmalısınız.
CONTINENT_COUNTRIES = {
    "asia": [
        "AF", "AM", "AZ", "BH", "BD", "BT", "CN", "CY", "GE", "IN", "ID", "IR", "IQ", "IL", "JP", "JO", "KZ",
        "KH", "KP", "KR", "KW", "KG", "LA", "LB", "MY", "MV", "MN", "MM", "NP", "OM", "PK", "PS", "PH", "QA",
        "SA", "SG", "LK", "SY", "TW", "TJ", "TH", "TL", "TR", "TM", "AE", "UZ", "VN", "YE"
    ],
    "europe": [
        "AL", "AD", "AT", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU",
        "IS", "IE", "IT", "XK", "LV", "LI", "LT", "LU", "MD", "MC", "ME", "NL", "MK", "NO", "PL", "PT", "RO",
        "RU", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA", "GB", "VA"
    ],
    "africa": [
        "DZ", "AO", "BJ", "BW", "BF", "BI", "CM", "CV", "CF", "TD", "KM", "CG", "CD", "CI", "DJ", "EG", "GQ",
        "ER", "SZ", "ET", "GA", "GM", "GH", "GN", "GW", "KE", "LS", "LR", "LY", "MG", "MW", "ML", "MR", "MU",
        "MZ", "NA", "NE", "NG", "RW", "ST", "SN", "SC", "SL", "SO", "ZA", "SS", "SD", "TG", "TN", "UG", "ZM", "ZW"
    ],
    "north_america": [
        "AG", "BS", "BB", "BZ", "CA", "CR", "CU", "DM", "DO", "SV", "GD", "GT", "HT", "HN", "JM", "MX", "NI",
        "PA", "KN", "LC", "VC", "TT", "US"
    ],
    "south_america": [
        "AR", "BO", "BR", "CL", "CO", "EC", "GY", "PY", "PE", "SR", "UY", "VE"
    ],
    "oceania": [
        "AU", "FJ", "KI", "MH", "FM", "NR", "NZ", "PW", "PG", "WS", "SB", "TO", "TV", "VU"
    ],
}


def generate_html_file(country_folder_name, videos_data, structured_data):
    """Belirtilen ülke için HTML dosyasını oluşturur."""

    # Klasör ve URL'lerde kullanılacak tireli isim
    sanitized_country_name_for_url = country_folder_name.replace('_', '-')

    # Görüntülenecek ülke adı (baş harfleri büyük)
    display_country_name = COUNTRY_INFO.get(
        country_folder_name, {}
    ).get("display_name", country_folder_name.replace('-', ' ').replace('_', ' ')).title()

    # Structured data JSON-LD bloğunu oluştur
    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2)
        structured_data_block = (
            '<script type="application/ld+json">\n' +
            structured_json +
            '\n</script>'
        )

    # Kıtaya göre aktif sınıfı belirle
    continent_of_country = ""
    country_code_for_folder = COUNTRY_INFO.get(country_folder_name, {}).get("code")
    if country_code_for_folder:
        for continent, countries_in_continent in CONTINENT_COUNTRIES.items():
            if country_code_for_folder.upper() in [c.upper() for c in countries_in_continent]:
                continent_of_country = continent
                break

    continent_active_classes = {
        'asia_active': 'active' if continent_of_country == 'asia' else '',
        'europe_active': 'active' if continent_of_country == 'europe' else '',
        'africa_active': 'active' if continent_of_country == 'africa' else '',
        'north_america_active': 'active' if continent_of_country == 'north_america' else '',
        'south_america_active': 'active' if continent_of_country == 'south_america' else '',
        'oceania_active': 'active' if continent_of_country == 'oceania' else '',
    }

    country_buttons_html = []
    sorted_country_info = sorted(
        COUNTRY_INFO.items(),
        key=lambda item: item[1].get("display_name", item[0].replace('_', ' ')).title()
    )

    for c_folder_name, c_info in sorted_country_info:
        c_display_name = c_info.get("display_name", c_folder_name.replace('_', ' ')).title()
        first_letter = c_display_name[0].upper()
        
        # Ülke butonlarının href'i için de tireli isim kullanıyoruz
        country_button_link_name = c_folder_name.replace("_", "-")

        is_current_country_active = " active" if c_folder_name == country_folder_name else ""

        country_buttons_html.append(
            f'''<button onclick="location.href='../{country_button_link_name}/'" data-letter="{first_letter}" class="country-button{is_current_country_active}">{c_display_name}</button>'''
        )

    # HTML şablonu (JavaScript'teki fetch yolu mutlak yapıldı ve tireli isme uygun)
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

    <title>Trending YouTube Videos in {display_country_name} - Updated Every 3 Hours | TopTubeList</title>
    <meta name="description" content="Watch the most popular YouTube videos trending across {display_country_name}. Stay current with viral content.">
    <meta name="keywords" content="YouTube trends {display_country_name}, popular videos {display_country_name}, trending YouTube, viral content">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://toptubelist.com/{sanitized_country_name_for_url}/" />
    <link rel="stylesheet" href="../style.css" />

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103"
        crossorigin="anonymous"></script>

{structured_data_block}
</head>
<body>
<header>
    <div class="container header-flex">
        <a href="../index.html" id="logoLink"> <img src="../TopTubeListLogo.webp" alt="TopTubeList Logo" width="100" style="margin-right: 12px; vertical-align: middle;">
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
                {country_buttons}
            </div>
        </div>
</main>
    
    <div class="video-list-wrapper">
        <div id="videoList" class="video-list"></div>
        <button id="loadMoreBtn" class="site-button">Load More</button>
    </div>

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
                            <p>We couldn’t fetch trending YouTube videos for this country at the moment.</p>
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

            // JSON dosyasının yolu dinamik olarak Python'dan geliyor
            // DİKKAT: Burada yolu mutlak yapıyoruz ve tireli dosya ismini kullanıyoruz!
            fetch("/Country_data/videos/videos-{sanitized_country_name_for_url}.json") 
                .then(res => {{
                    if (!res.ok) {{
                        // Eğer dosya bulunamazsa (404) veya başka bir HTTP hatası olursa
                        console.error(`HTTP error fetching videos: ${{res.status}} for /Country_data/videos/videos-{sanitized_country_name_for_url}.json`);
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
        display_country_name=display_country_name,
        sanitized_country_name_for_url=sanitized_country_name_for_url, # URL ve JS için tireli isim
        structured_data_block=structured_data_block,
        **continent_active_classes,
        country_buttons="\n".join(country_buttons_html),
    )

    # Ülke klasörünü oluştur ve HTML dosyasını yaz
    country_dir = os.path.join(os.getcwd(), sanitized_country_name_for_url) # Klasör ismi de tireli olacak
    os.makedirs(country_dir, exist_ok=True)

    output_path = os.path.join(country_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"{output_path} oluşturuldu.")


def main():
    base_data_dir = "Country_data"
    videos_base_dir = os.path.join(base_data_dir, "videos")
    structured_data_base_dir = os.path.join(base_data_dir, "structured_data")

    # Klasörlerin var olduğundan emin ol
    os.makedirs(videos_base_dir, exist_ok=True)
    os.makedirs(structured_data_base_dir, exist_ok=True)

    for country_folder_name_raw, info in COUNTRY_INFO.items():
        # Klasör ve dosya adlarında tire (-) kullanacağımız için dönüştürüyoruz
        sanitized_country_name = country_folder_name_raw.replace('_', '-')

        # JSON dosyalarının yollarını oluştururken tireli isim kullanıyoruz
        videos_file = os.path.join(videos_base_dir, f"videos-{sanitized_country_name}.json")
        structured_data_file = os.path.join(structured_data_base_dir, f"structured_data-{sanitized_country_name}.json")

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

        # HTML dosyasını oluştur (sanitized_country_name'i kullanıyoruz)
        generate_html_file(sanitized_country_name, videos_data, structured_data)

if __name__ == "__main__":
    main()
