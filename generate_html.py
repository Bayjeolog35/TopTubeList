import json
import os

def generate_html_file(continent_name, videos_data, structured_data):
    """Belirtilen kıta için HTML dosyasını oluşturur."""

    # Kıta adını dosya adına uygun hale getir (örn: north_america -> North America)
    display_continent_name = ' '.join(word.capitalize() for word in continent_name.split('_'))

    # Her kıta için aktif sınıfı hesapla
    asia_active = 'active' if continent_name == 'asia' else ''
    europe_active = 'active' if continent_name == 'europe' else ''
    africa_active = 'active' if continent_name == 'africa' else ''
    north_america_active = 'active' if continent_name == 'north_america' else ''
    south_america_active = 'active' if continent_name == 'south_america' else ''
    oceania_active = 'active' if continent_name == 'oceania' else ''

    # HTML şablonu (DİKKAT: r""" ile başlar ve üç tırnak içinde)
    # Koşullu ifadeler yerine doğrudan değişkenler kullanıyoruz.
    # JavaScript içindeki TÜM TEK SÜSLÜ PARANTEZLERİ {{ ve }} olarak değiştirdik.
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

  <title>Trending YouTube Videos in {display_continent_name} - Updated Every 3 Hours | TopTubeList</title>
  <meta name="description" content="Watch the most popular YouTube videos trending across {display_continent_name}. Stay current with viral content.">
  <meta name="keywords" content="YouTube trends {display_continent_name}, popular videos {display_continent_name}, trending YouTube, viral content">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://toptubelist.com/{continent_name}.html" />
  <link rel="stylesheet" href="style.css" />

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103"
    crossorigin="anonymous"></script>

  <script type="application/ld+json">
{structured_data_json}
</script>
</head>
  
<body>
  
<header>
  <div class="container header-flex">
    <a href="index.html" id="logoLink">
      <img src="TopTubeListLogo.webp" alt="TopTubeList Logo" width="100" style="margin-right: 12px; vertical-align: middle;">
    </a>
    <h1>Most Viewed in {display_continent_name}</h1>
    <button id="darkModeToggle" title="Toggle Dark Mode">🌙</button>
  </div>

  <nav id="continentNav">
    <a href="index.html">Worldwide</a>
    <a href="asia.html" class="{asia_active}">Asia</a>
    <a href="europe.html" class="{europe_active}">Europe</a>
    <a href="africa.html" class="{africa_active}">Africa</a>
    <a href="north_america.html" class="{north_america_active}">North America</a>
    <a href="south_america.html" class="{south_america_active}">South America</a>
    <a href="oceania.html" class="{oceania_active}">Oceania</a>
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
  <button onclick="location.href='Afghanistan.html'" data-letter="A">Afghanistan</button>
  <button onclick="location.href='Albania.html'" data-letter="A">Albania</button>
  <button onclick="location.href='Algeria.html'" data-letter="A">Algeria</button>
  <button onclick="location.href='Andorra.html'" data-letter="A">Andorra</button>
  <button onclick="location.href='Angola.html'" data-letter="A">Angola</button>
  <button onclick="location.href='Antigua_And_Barbuda.html'" data-letter="A">Antigua and Barbuda</button>
  <button onclick="location.href='Argentina.html'" data-letter="A">Argentina</button>
  <button onclick="location.href='Armenia.html'" data-letter="A">Armenia</button>
  <button onclick="location.href='Australia.html'" data-letter="A">Australia</button>
  <button onclick="location.href='Austria.html'" data-letter="A">Austria</button>
  <button onclick="location.href='Azerbaijan.html'" data-letter="A">Azerbaijan</button>

  <button onclick="location.href='Bahamas.html'" data-letter="B">Bahamas</button>
  <button onclick="location.href='Bahrain.html'" data-letter="B">Bahrain</button>
  <button onclick="location.href='Bangladesh.html'" data-letter="B">Bangladesh</button>
  <button onclick="location.href='Barbados.html'" data-letter="B">Barbados</button>
  <button onclick="location.href='Belarus.html'" data-letter="B">Belarus</button>
  <button onclick="location.href='Belgium.html'" data-letter="B">Belgium</button>
  <button onclick="location.href='Belize.html'" data-letter="B">Belize</button>
  <button onclick="location.href='Benin.html'" data-letter="B">Benin</button>
  <button onclick="location.href='Bhutan.html'" data-letter="B">Bhutan</button>
  <button onclick="location.href='Bolivia.html'" data-letter="B">Bolivia</button>
  <button onclick="location.href='Bosnia_And_Herzegovina.html'" data-letter="B">Bosnia and Herzegovina</button>
  <button onclick="location.href='Botswana.html'" data-letter="B">Botswana</button>
  <button onclick="location.href='Brazil.html'" data-letter="B">Brazil</button>
  <button onclick="location.href='Brunei.html'" data-letter="B">Brunei</button>
  <button onclick="location.href='Bulgaria.html'" data-letter="B">Bulgaria</button>
  <button onclick="location.href='Burkina_Faso.html'" data-letter="B">Burkina Faso</button>
  <button onclick="location.href='Burundi.html'" data-letter="B">Burundi</button>

  <button onclick="location.href='Cabo_Verde.html'" data-letter="C">Cabo Verde</button>
  <button onclick="location.href='Cambodia.html'" data-letter="C">Cambodia</button>
  <button onclick="location.href='Cameroon.html'" data-letter="C">Cameroon</button>
  <button onclick="location.href='Canada.html'" data-letter="C">Canada</button>
  <button onclick="location.href='Central_African_Republic.html'" data-letter="C">Central African Republic</button>
  <button onclick="location.href='Chad.html'" data-letter="C">Chad</button>
  <button onclick="location.href='Chile.html'" data-letter="C">Chile</button>
  <button onclick="location.href='China.html'" data-letter="C">China</button>
  <button onclick="location.href='Colombia.html'" data-letter="C">Colombia</button>
  <button onclick="location.href='Comoros.html'" data-letter="C">Comoros</button>
  <button onclick="location.href='Congo_Democratic_RepublicOfThe.html'" data-letter="C">Congo (Democratic Republic of the)</button>
  <button onclick="location.href='Congo_Republic_Of_The.html'" data-letter="C">Congo (Republic of the)</button>
  <button onclick="location.href='Costa_Rica.html'" data-letter="C">Costa Rica</button>
  <button onclick="location.href='Cote_DIvoire.html'" data-letter="C">Cote d'Ivoire</button>
  <button onclick="location.href='Croatia.html'" data-letter="C">Croatia</button>
  <button onclick="location.href='Cuba.html'" data-letter="C">Cuba</button>
  <button onclick="location.href='Cyprus.html'" data-letter="C">Cyprus</button>
  <button onclick="location.href='Czech_Republic.html'" data-letter="C">Czech Republic</button>

  <button onclick="location.href='Denmark.html'" data-letter="D">Denmark</button>
  <button onclick="location.href='Djibouti.html'" data-letter="D">Djibouti</button>
  <button onclick="location.href='Dominica.html'" data-letter="D">Dominica</button>
  <button onclick="location.href='Dominican_Republic.html'" data-letter="D">Dominican Republic</button>

  <button onclick="location.href='East_Timor.html'" data-letter="E">East Timor</button>
  <button onclick="location.href='Ecuador.html'" data-letter="E">Ecuador</button>
  <button onclick="location.href='Egypt.html'" data-letter="E">Egypt</button>
  <button onclick="location.href='ElSalvador.html'" data-letter="E">El Salvador</button>
  <button onclick="location.href='Equatorial_Guinea.html'" data-letter="E">Equatorial Guinea</button>
  <button onclick="location.href='Eritrea.html'" data-letter="E">Eritrea</button>
  <button onclick="location.href='Estonia.html'" data-letter="E">Estonia</button>
  <button onclick="location.href='Eswatini.html'" data-letter="E">Eswatini</button>
  <button onclick="location.href='Ethiopia.html'" data-letter="E">Ethiopia</button>

  <button onclick="location.href='Fiji.html'" data-letter="F">Fiji</button>
  <button onclick="location.href='Finland.html'" data-letter="F">Finland</button>
  <button onclick="location.href='France.html'" data-letter="F">France</button>

  <button onclick="location.href='Gabon.html'" data-letter="G">Gabon</button>
  <button onclick="location.href='Gambia.html'" data-letter="G">Gambia</button>
  <button onclick="location.href='Georgia.html'" data-letter="G">Georgia</button>
  <button onclick="location.href='Germany.html'" data-letter="G">Germany</button>
  <button onclick="location.href='Ghana.html'" data-letter="G">Ghana</button>
  <button onclick="location.href='Greece.html'" data-letter="G">Greece</button>
  <button onclick="location.href='Grenada.html'" data-letter="G">Grenada</button>
  <button onclick="location.href='Guatemala.html'" data-letter="G">Guatemala</button>
  <button onclick="location.href='Guinea.html'" data-letter="G">Guinea</button>
  <button onclick="location.href='Guinea_Bissau.html'" data-letter="G">Guinea-Bissau</button>
  <button onclick="location.href='Guyana.html'" data-letter="G">Guyana</button>

  <button onclick="location.href='Haiti.html'" data-letter="H">Haiti</button>
  <button onclick="location.href='Honduras.html'" data-letter="H">Honduras</button>
  <button onclick="location.href='Hungary.html'" data-letter="H">Hungary</button>

  <button onclick="location.href='Iceland.html'" data-letter="I">Iceland</button>
  <button onclick="location.href='India.html'" data-letter="I">India</button>
  <button onclick="location.href='Indonesia.html'" data-letter="I">Indonesia</button>
  <button onclick="location.href='Iran.html'" data-letter="I">Iran</button>
  <button onclick="location.href='Iraq.html'" data-letter="I">Iraq</button>
  <button onclick="location.href='Ireland.html'" data-letter="I">Ireland</sbutton>
  <button onclick="location.href='Israel.html'" data-letter="I">Israel</button>
  <button onclick="location.href='Italy.html'" data-letter="I">Italy</button>

  <button onclick="location.href='Jamaica.html'" data-letter="J">Jamaica</button>
  <button onclick="location.href='Japan.html'" data-letter="J">Japan</button>
  <button onclick="location.href='Jordan.html'" data-letter="J">Jordan</button>

  <button onclick="location.href='Kazakhstan.html'" data-letter="K">Kazakhstan</button>
  <button onclick="location.href='Kenya.html'" data-letter="K">Kenya</button>
  <button onclick="location.href='Kiribati.html'" data-letter="K">Kiribati</button>
  <button onclick="location.href='Korea_North.html'" data-letter="K">Korea (North)</button>
  <button onclick="location.href='Korea_South.html'" data-letter="K">Korea (South)</button>
  <button onclick="location.href='Kosovo.html'" data-letter="K">Kosovo</button>
  <button onclick="location.href='Kuwait.html'" data-letter="K">Kuwait</button>
  <button onclick="location.href='Kyrgyzstan.html'" data-letter="K">Kyrgyzstan</button>

  <button onclick="location.href='Laos.html'" data-letter="L">Laos</button>
  <button onclick="location.href='Latvia.html'" data-letter="L">Latvia</button>
  <button onclick="location.href='Lebanon.html'" data-letter="L">Lebanon</sbutton>
  <button onclick="location.href='Lesotho.html'" data-letter="L">Lesotho</button>
  <button onclick="location.href='Liberia.html'" data-letter="L">Liberia</button>
  <button onclick="location.href='Libya.html'" data-letter="L">Libya</button>
  <button onclick="location.href='Liechtenstein.html'" data-letter="L">Liechtenstein</button>
  <button onclick="location.href='Lithuania.html'" data-letter="L">Lithuania</button>
  <button onclick="location.href='Luxembourg.html'" data-letter="L">Luxembourg</button>

  <button onclick="location.href='Madagascar.html'" data-letter="M">Madagascar</button>
  <button onclick="location.href='Malawi.html'" data-letter="M">Malawi</button>
  <button onclick="location.href='Malaysia.html'" data-letter="M">Malaysia</button>
  <button onclick="location.href='Maldives.html'" data-letter="M">Maldives</button>
  <button onclick="location.href='Mali.html'" data-letter="M">Mali</button>
  <button onclick="location.href='Malta.html'" data-letter="M">Malta</button>
  <button onclick="location.href='Marshall_Islands.html'" data-letter="M">Marshall Islands</button>
  <button onclick="location.href='Mauritania.html'" data-letter="M">Mauritania</button>
  <button onclick="location.href='Mauritius.html'" data-letter="M">Mauritius</button>
  <button onclick="location.href='Mexico.html'" data-letter="M">Mexico</button>
  <button onclick="location.href='Micronesia.html'" data-letter="M">Micronesia</button>
  <button onclick="location.href='Moldova.html'" data-letter="M">Moldova</button>
  <button onclick="location.href='Monaco.html'" data-letter="M">Monaco</button>
  <button onclick="location.href='Mongolia.html'" data-letter="M">Mongolia</button>
  <button onclick="location.href='Montenegro.html'" data-letter="M">Montenegro</button>
  <button onclick="location.href='Morocco.html'" data-letter="M">Morocco</button>
  <button onclick="location.href='Mozambique.html'" data-letter="M">Mozambique</button>
  <button onclick="location.href='Myanmar.html'" data-letter="M">Myanmar</button>

  <button onclick="location.href='Namibia.html'" data-letter="N">Namibia</button>
  <button onclick="location.href='Nauru.html'" data-letter="N">Nauru</button>
  <button onclick="location.href='Nepal.html'" data-letter="N">Nepal</button>
  <button onclick="location.href='Netherlands.html'" data-letter="N">Netherlands</button>
  <button onclick="location.href='New_Zealand.html'" data-letter="N">New Zealand</button>
  <button onclick="location.href='Nicaragua.html'" data-letter="N">Nicaragua</button>
  <button onclick="location.href='Niger.html'" data-letter="N">Niger</button>
  <button onclick="location.href='Nigeria.html'" data-letter="N">Nigeria</button>
  <button onclick="location.href='North_Macedonia.html'" data-letter="N">North Macedonia</button>
  <button onclick="location.href='Norway.html'" data-letter="N">Norway</button>

  <button onclick="location.href='Oman.html'" data-letter="O">Oman</button>

  <button onclick="location.href='Pakistan.html'" data-letter="P">Pakistan</button>
  <button onclick="location.href='Palau.html'" data-letter="P">Palau</button>
  <button onclick="location.href='Palestine.html'" data-letter="P">Palestine</button>
  <button onclick="location.href='Panama.html'" data-letter="P">Panama</button>
  <button onclick="location.href='Papua_New_Guinea.html'" data-letter="P">Papua New Guinea</button>
  <button onclick="location.href='Paraguay.html'" data-letter="P">Paraguay</button>
  <button onclick="location.href='Peru.html'" data-letter="P">Peru</button>
  <button onclick="location.href='Philippines.html'" data-letter="P">Philippines</button>
  <button onclick="location.href='Poland.html'" data-letter="P">Poland</button>
  <button onclick="location.href='Portugal.html'" data-letter="P">Portugal</button>

  <button onclick="location.href='Qatar.html'" data-letter="Q">Qatar</button>

  <button onclick="location.href='Romania.html'" data-letter="R">Romania</button>
  <button onclick="location.href='Russia.html'" data-letter="R">Russia</button>
  <button onclick="location.href='Rwanda.html'" data-letter="R">Rwanda</button>

  <button onclick="location.href='Saint_Kitts_And_Nevis.html'" data-letter="S">Saint Kitts and Nevis</button>
  <button onclick="location.href='Saint_Lucia.html'" data-letter="S">Saint Lucia</sbutton>
  <button onclick="location.href='Saint_Vincent_And_The_Grenadines.html'" data-letter="S">Saint Vincent and the Grenadines</button>
  <button onclick="location.href='Samoa.html'" data-letter="S">Samoa</button>
  <button onclick="location.href='San_Marino.html'" data-letter="S">San Marino</button>
  <button onclick="location.href='Sao_Tome_And_Principe.html'" data-letter="S">Sao Tome and Principe</button>
  <button onclick="location.href='Saudi_Arabia.html'" data-letter="S">Saudi Arabia</button>
  <button onclick="location.href='Senegal.html'" data-letter="S">Senegal</sbutton>
  <button onclick="location.href='Serbia.html'" data-letter="S">Serbia</button>
  <button onclick="location.href='Seychelles.html'" data-letter="S">Seychelles</button>
  <button onclick="location.href='Sierra_Leone.html'" data-letter="S">Sierra Leone</sbutton>
  <button onclick="location.href='Singapore.html'" data-letter="S">Singapore</button>
  <button onclick="location.href='Slovakia.html'" data-letter="S">Slovakia</sbutton>
  <button onclick="location.href='Slovenia.html'" data-letter="S">Slovenia</button>
  <button onclick="location.href='Solomon_Islands.html'" data-letter="S">Solomon Islands</button>
  <button onclick="location.href='Somalia.html'" data-letter="S">Somalia</button>
  <button onclick="location.href='South_Africa.html'" data-letter="S">South Africa</button>
  <button onclick="location.href='South_Sudan.html'" data-letter="S">South Sudan</button>
  <button onclick="location.href='Spain.html'" data-letter="S">Spain</button>
  <button onclick="location.href='Sri_Lanka.html'" data-letter="S">Sri Lanka</button>
  <button onclick="location.href='Sudan.html'" data-letter="S">Sudan</button>
  <button onclick="location.href='Suriname.html'" data-letter="S">Suriname</button>
  <button onclick="location.href='Sweden.html'" data-letter="S">Sweden</button>
  <button onclick="location.href='Switzerland.html'" data-letter="S">Switzerland</button>
  <button onclick="location.href='Syria.html'" data-letter="S">Syria</button>

  <button onclick="location.href='Taiwan.html'" data-letter="T">Taiwan</button>
  <button onclick="location.href='Tajikistan.html'" data-letter="T">Tajikistan</button>
  <button onclick="location.href='Tanzania.html'" data-letter="T">Tanzania</button>
  <button onclick="location.href='Thailand.html'" data-letter="T">Thailand</button>
  <button onclick="location.href='Togo.html'" data-letter="T">Togo</button>
  <button onclick="location.href='Tonga.html'" data-letter="T">Tonga</button>
  <button onclick="location.href='Trinidad_And_Tobago.html'" data-letter="T">Trinidad and Tobago</button>
  <button onclick="location.href='Tunisia.html'" data-letter="T">Tunisia</button>
  <button onclick="location.href='Turkey.html'" data-letter="T">Turkey</button>
  <button onclick="location.href='Turkmenistan.html'" data-letter="T">Turkmenistan</button>
  <button onclick="location.href='Tuvalu.html'" data-letter="T">Tuvalu</button>

  <button onclick="location.href='Uganda.html'" data-letter="U">Uganda</button>
  <button onclick="location.href='Ukraine.html'" data-letter="U">Ukraine</button>
  <button onclick="location.href='United_Arab_Emirates.html'" data-letter="U">United Arab Emirates</button>
  <button onclick="location.href='United_Kingdom.html'" data-letter="U">United Kingdom</button>
  <button onclick="location.href='United_States.html'" data-letter="U">United States</button>
  <button onclick="location.href='Uruguay.html'" data-letter="U">Uruguay</button>
  <button onclick="location.href='Uzbekistan.html'" data-letter="U">Uzbekistan</button>

  <button onclick="location.href='Vanuatu.html'" data-letter="V">Vanuatu</button>
  <button onclick="location.href='Vatican_City.html'" data-letter="V">Vatican City</button>
  <button onclick="location.href='Venezuela.html'" data-letter="V">Venezuela</button>
  <button onclick="location.href='Vietnam.html'" data-letter="V">Vietnam</button>

  <button onclick="location.href='Yemen.html'" data-letter="Y">Yemen</button>

  <button onclick="location.href='Zambia.html'" data-letter="Z">Zambia</button>
  <button onclick="location.href='Zimbabwe.html'" data-letter="Z">Zimbabwe</button>
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



    fetch("videos_{continent_name}.json") 
      .then(res => res.json())
      .then(videos => {{
        allVideos = videos;
        renderVideos();
      }});
 
    document.getElementById("loadMoreBtn").addEventListener("click", () => {{
      displayCount += 10;
      renderVideos();
    }});

  }});
</script>

</body>
</html>
"""
    
    # Python değişkenlerini HTML şablonuna yerleştirme
    # Bu sefer doğrudan hesapladığımız aktif sınıf değişkenlerini kullanıyoruz.
    html_content = html_template.format(
        display_continent_name=display_continent_name,
        continent_name=continent_name,
        structured_data_json=json.dumps(structured_data, indent=2),
        asia_active=asia_active,
        europe_active=europe_active,
        africa_active=africa_active,
        north_america_active=north_america_active,
        south_america_active=south_america_active,
        oceania_active=oceania_active
    )

    with open(f"{continent_name}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"{continent_name}.html oluşturuldu.")

def main():
    # Mevcut JSON dosyalarınıza göre bu listeyi güncelledim
    # Yüklediğiniz görsellerde structured_data_africa.json veya videos_africa.json görünmüyor.
    # Eğer bu dosyalarınız yoksa, listeye "africa" eklemeyin.
    # Ben şimdilik ekliyorum, eğer hata alırsanız "africa" yı kaldırabilirsiniz.
    continents = ["asia", "europe", "north_america", "south_america", "oceania", "africa"] 

    for continent in continents:
        videos_file = f"videos_{continent}.json"
        structured_data_file = f"structured_data_{continent}.json"

        videos_data = []
        structured_data = []

        if os.path.exists(videos_file):
            with open(videos_file, "r", encoding="utf-8") as f:
                videos_data = json.load(f)
        else:
            print(f"Uyarı: {videos_file} bulunamadı. Bu kıta için video verisi olmayacak.")

        if os.path.exists(structured_data_file):
            with open(structured_data_file, "r", encoding="utf-8") as f:
                structured_data = json.load(f)
        else:
            print(f"Uyarı: {structured_data_file} bulunamadı. Bu kıta için yapılandırılmış veri olmayacak.")

        generate_html_file(continent, videos_data, structured_data)

if __name__ == "__main__":
    main()