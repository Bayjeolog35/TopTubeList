'use strict';
// dynamic.js - TopTubeList için Etkileşimli UI betikleri
// Şunları yönetir: menü, karanlık mod, filtreler, video yükleme ve iletişim formu


document.addEventListener("DOMContentLoaded", async () => { // <--- BURAYI 'async' OLARAK İŞARETLEDİK!
    // --- UI Element References ---
    // Tüm element referanslarını en başta tanımlamak daha düzenlidir.
    const hamburger = document.querySelector(".hamburger");
    const countryPanel = document.querySelector(".country-panel"); // "panel" yerine "countryPanel" daha açıklayıcı
    const darkModeToggle = document.getElementById("darkModeToggle");
    // === DÜZENLEME BAŞLANGICI: savedMode değişkeni buraya taşındı ===
    const savedMode = localStorage.getItem("darkMode");
    // === DÜZENLEME SONU ===
    const contactToggle = document.getElementById("contactToggle");
    const contactContent = document.getElementById("contactContent");
    const aboutToggle = document.getElementById("aboutToggle");
    const aboutContent = document.getElementById("aboutContent");
    const contactForm = document.getElementById("contactForm"); // "form" yerine "contactForm" daha açıklayıcı
    const formStatusDiv = document.getElementById("formStatus"); // "statusDiv" yerine "formStatusDiv" daha açıklayıcı
    const videoListContainer = document.getElementById("videoList"); // "container" yerine "videoListContainer" daha açıklayıcı
    const loadMoreButton = document.getElementById("loadMoreBtn"); // "loadMoreBtn" yerine "loadMoreButton" daha tutarlı

    // --- Video Render State Variables ---
    let allVideos = [];
    let displayCount = 10;


    // --- Helper Functions ---

    /**
     * Gets the country name from the current URL pathname.
     * Example: /path/to/country.html -> country
     */
    function getCountryFromURL() {
        const path = window.location.pathname;
        const filename = path.split('/').pop(); // örnek: "turkey.html", "index.html", veya ""
        if (!filename || filename === "" || filename === "index.html") return "index";
        return filename.replace('.html', '').toLowerCase();
    }
    /**
     * Creates an HTML video card element from a video object.
     * @param {Object} video - The video data object.
     * @returns {HTMLElement} The created video card div.
     */
// dynamic.js dosyanızdaki createVideoCard fonksiyonunu bu kodla değiştirin.
// dynamic.js dosyanızdaki createVideoCard fonksiyonunu bu kodla değiştirin.
function createVideoCard(video) {
  const card = document.createElement("div");
  card.className = "video-card";

  // ---- Güvenli değerler ----
  const viewsStr = video.views_str || (typeof video.views === "number" ? video.views.toLocaleString("en-US") : "0");
  const published =
    video.published_date_formatted ||
    (video.published_at ? new Date(video.published_at).toLocaleDateString("tr-TR") : "");

  const viewChange = Number(video.viewChange || 0);
  const trend = video.trend || (viewChange > 0 ? "rising" : viewChange < 0 ? "falling" : "stable");

  // Trend class'ı (Gemini'nin bıraktığı eksik parça)
  const trendClass =
    trend === "rising" || trend === "new"
      ? "trend-up"
      : trend === "falling"
      ? "trend-down"
      : "trend-stable";

  const iconMap = { rising: "up.webp", new: "up.webp", falling: "down.webp", stable: "zero.webp" };
  const trendIconPath = iconMap[trend] || "zero.webp";

  // Sıralama değişimi rozeti
  const rankChange = Number(video.rankChange || 0);
  let rankChangeHtml = "";
  if (rankChange !== 0) {
    const isUp = rankChange > 0;
    const changeText = isUp ? `+${rankChange}` : `${rankChange}`;
    const changeClass = isUp ? "rank-up" : "rank-down";
    const changeArrow = isUp ? "⬆" : "⬇";
    rankChangeHtml = `<span class="rank-change ${changeClass}">${changeText} ${changeArrow}</span>`;
  }

  card.innerHTML = `
    <a href="${video.url}" target="_blank" rel="noopener" class="video-thumbnail">
      <img class="thumbnail" src="${video.thumbnail}" alt="${video.title}" loading="lazy" />
      ${video.duration ? `<span class="duration">${video.duration}</span>` : ""}
    </a>

    <div class="video-info">
      <h2>${video.title}</h2>
      <p><strong>Channel:</strong> ${video.channel}</p>
      <p><strong>Views:</strong> ${viewsStr} views</p>
      ${published ? `<p><strong>Date:</strong> ${published}</p>` : ""}
      ${video.duration ? `<p><strong>Duration:</strong> ${video.duration}</p>` : ""}
      ${
        viewChange !== 0 || trend === "new"
          ? `<p class="trend-info ${trendClass}"><strong>View change (last 3h):</strong> ${video.viewChange_str || String(viewChange)}</p>`
          : ""
      }
    </div>

    <div class="trend-badge">
      ${rankChangeHtml}
      <img src="${trendIconPath}" alt="${trend}" class="trend-icon" width="20" height="20" />
    </div>
  `;

  return card;
}



    /**
     * Displays a message when no video data is available for a country.
     */
    function showNoDataMessage() {
        if (!videoListContainer) {
            console.warn("videoListContainer bulunamadı. 'No Data' mesajı gösterilemiyor.");
            return;
        }

        videoListContainer.innerHTML = `
            <div class="no-data-message">
                <img src="nodata.webp" alt="No data" width="100">
                <h2>Oops... No trending videos here 😔</h2>
                <p><strong>YouTube doesn’t currently share data for this country.</strong></p>
                <p>But don’t worry. The rest of the world is buzzing with viral content!</p>
                <p>Why not explore what’s trending elsewhere? 🌍</p>
            </div>
        `;

        // sadece veri yoksa main'e class ekle
const mainElement = document.querySelector("main");
if (mainElement) {
  mainElement.classList.add("centered-no-data");
}
        
        // Load More butonunu gizle, eğer mevcutsa
        if (loadMoreButton) {
            loadMoreButton.style.display = "none";
        }
    }
    
    /**
     * Fetches video data for the current country and renders it.
     */
   async function loadVideos() {
  const country = getCountryFromURL();
  const dataFile =
    country === "index" || country === ""
      ? "index.videos.json"
      : `${country}.vid.data.json`;

  console.log(`Veri yükleme denemesi: ${dataFile}`);

  try {
    const response = await fetch(dataFile);
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`'${dataFile}' dosyası bulunamadı. URL: ${response.url}`);
      }
      throw new Error(`Veri yüklenirken HTTP hatası: ${response.status} ${response.statusText}`);
    }

    const jsonData = await response.json();
    console.log("Yüklenen JSON verisi (ilk 5 video):", Array.isArray(jsonData) ? jsonData.slice(0, 5) : jsonData);

    if (!Array.isArray(jsonData)) {
      throw new Error("Yüklenen veri bir dizi değil.");
    }

    // Normalize et: viewChange sayıya çevrilir; yoksa 0 yapılır
    allVideos = jsonData.map(v => ({
      ...v,
      viewChange: Number(v?.viewChange) || 0
    }));

    // Son 3 saatteki izlenme artışına göre (büyükten küçüğe) sırala
    allVideos.sort((a, b) => b.viewChange - a.viewChange);

    if (allVideos.length === 0) {
      throw new Error("Video verisi boş.");
    }

    if (country !== "index" && country !== "") {
      document.title = `Trending in ${country.charAt(0).toUpperCase() + country.slice(1)} | TopTubeList`;
    }

    renderVideos();
  } catch (error) {
    console.error("Veri yükleme hatası:", error);
    showNoDataMessage();
  }
}

    /**
     * Renders videos into the videoListContainer based on displayCount.
     */
    function renderVideos() {
        if (!videoListContainer) {
            console.warn("videoListContainer bulunamadı, videolar render edilemiyor.");
            return;
        }

        videoListContainer.innerHTML = ""; // Mevcut videoları temizle
        const videosToDisplay = allVideos.slice(0, displayCount);

        if (videosToDisplay.length === 0) {
            showNoDataMessage();
            return;
        }

        videosToDisplay.forEach(video => {
            const card = createVideoCard(video);
            videoListContainer.appendChild(card);
        });

        // Load More butonunun görünürlüğünü yönet
        if (loadMoreButton) {
            if (displayCount >= allVideos.length) {
                loadMoreButton.style.display = "none"; // Tüm videolar gösterildiyse gizle
            } else {
                loadMoreButton.style.display = "block"; // Daha fazla video varsa göster
            }
        }
    }



    // --- Event Listeners and Initial Setup ---

    // Hamburger menü ve ülke paneli görünürlüğü (Responsive tasarım)
    // Bu kısım biraz karmaşık. Daha iyi bir responsive tasarım için CSS media query'ler ve JS class toggle'lar tercih edilmeli.
    // Ancak mevcut mantığı koruyarak iyileştirildi.
    const setupResponsivePanel = () => {
        if (hamburger && countryPanel) {
            if (window.innerWidth <= 768) {
                hamburger.style.display = "block";
                countryPanel.classList.remove("active"); // Mobilde varsayılan olarak kapalı
                countryPanel.style.display = ""; // CSS tarafından yönetilmesine izin ver
            } else {
                hamburger.style.display = "none";
                countryPanel.classList.add("active"); // Masaüstünde varsayılan olarak açık
                countryPanel.style.display = "flex"; // Masaüstünde her zaman flex olarak göster
            }
        } else if (hamburger) {
            // Eğer sadece hamburger varsa ve panel yoksa yine de hamburgeri kontrol et
            hamburger.style.display = window.innerWidth <= 768 ? "block" : "none";
        }
    };

    setupResponsivePanel(); // Sayfa yüklendiğinde bir kez ayarla
    window.addEventListener("resize", setupResponsivePanel); // Pencere boyutu değiştiğinde tekrar ayarla

    if (hamburger && countryPanel) {
        hamburger.addEventListener("click", () => {
            countryPanel.classList.toggle("active");
            // Mobilde tıklandığında display özelliğini değiştirmek yerine sadece class toggle kullanın.
            // CSS'te .country-panel.active için display: flex ve display: none kurallarını tanımlayın.
            // Bu JS satırları karmaşıklaşmaması için kaldırıldı.
            // if (countryPanel.classList.contains("active")) {
            //    countryPanel.style.display = "flex";
            // } else {
            //    countryPanel.style.display = "none";
            // }
        });
    }


    // Dark Mode Toggle
    if (savedMode === "true") { // savedMode artık global scope'ta tanımlı, sorun yok
        document.body.classList.add("dark-mode");
    }
    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", () => {
            const isDarkNow = document.body.classList.toggle("dark-mode");
            localStorage.setItem("darkMode", isDarkNow);
        });
    }

    // Harf Filtreleme
    document.querySelectorAll(".alphabet-letter").forEach(letter => {
        letter.addEventListener("click", function (e) {
            e.preventDefault();
            const selectedLetter = this.getAttribute("data-letter"); // 'all', 'A', 'B' vb. alır
            const allLinks = document.querySelectorAll(".country-column .country-link"); // Tüm ülke bağlantılarını seçer

            allLinks.forEach(link => {
                // DÜZELTME: Ülke adının ilk harfini al
                const countryName = link.textContent.trim();
                const linkFirstLetter = countryName.charAt(0).toUpperCase(); // Ülke adının ilk harfini büyük harfe çevir

                if (selectedLetter === "all" || (linkFirstLetter && linkFirstLetter === selectedLetter.toUpperCase())) {
                    link.style.display = "block"; // Eşleşenleri göster
                } else {
                    link.style.display = "none"; // Eşleşmeyenleri gizle
                }
            });

            // Aktif harfi vurgula
            document.querySelectorAll(".alphabet-letter").forEach(a => a.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // FadeOut Animation (CSS ekleme) - Zaten eklenmiş, tekrar etmeye gerek yok
    // Bu kısım DOMContentLoaded içinde olması sorun değil, ancak tek seferlik bir işlem olduğu için
    // fonksiyonların veya olay dinleyicilerinin dışında, hemen DOMContentLoaded'ın altında olabilir.
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            0% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; transform: translateY(10px); }
        }`;
    document.head.appendChild(style);

 /**
     * Toggles the display of a content section with fade/slide effect.
     * @param {HTMLElement} element - The content element to toggle.
     */
    function toggleContent(element) {
        if (!element) return; // Element yoksa hata vermesini engelle

        if (element.classList.contains("show")) {
            element.classList.remove("show");
            // Elementi tamamen gizlemeden önce transition'ın bitmesini bekle
            setTimeout(() => {
                element.style.display = "none";
            }, 400); // CSS transition süresiyle eşleşmeli
        } else {
            element.style.display = "block";
            // Display: block olduktan sonra tarayıcının yeniden render yapmasına izin ver
            // ve sonra "show" sınıfını ekleyerek transition'ı tetikle
            setTimeout(() => {
                element.classList.add("show");
                // Element görünür hale geldikten sonra scroll yap
                element.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 10); // Çok küçük bir gecikme
        }
    }
    
    // Contact Toggle
    if (contactToggle && contactContent) {
        contactToggle.addEventListener("click", () => {
            toggleContent(contactContent);
        });
    }

    // About Toggle
    if (aboutToggle && aboutContent) {
        aboutToggle.addEventListener("click", () => {
            toggleContent(aboutContent);
        });
    }

    // Contact Form Submission
    if (contactForm && formStatusDiv) {
        contactForm.addEventListener("submit", async function (e) { // Async fonksiyon yapıldı
            e.preventDefault();
            const formData = new FormData(contactForm);

            try {
                const response = await fetch("/", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: new URLSearchParams(formData).toString()
                });

                if (!response.ok) {
                    throw new Error("Form gönderilirken sunucu hatası oluştu.");
                }

                contactForm.reset();
                formStatusDiv.innerText = "✅ ✅ Message sent successfully!";
                formStatusDiv.style.display = "block";
                formStatusDiv.style.cssText = `
                    position: fixed; bottom: 20px; right: 20px;
                    background: #28a745; color: white; padding: 12px 24px;
                    border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                    font-family: sans-serif; z-index: 9999;
                    animation: fadeOut 5s forwards;
                `;
                // Elementi DOM'dan kaldır
                setTimeout(() => formStatusDiv.remove(), 5000);
            } catch (error) {
                console.error("Form gönderme hatası:", error);
                alert("❌ Mesaj gönderilemedi. Lütfen tekrar deneyin.");
            }
        });
    }

    // Load More Button
    if (loadMoreButton) {
        loadMoreButton.addEventListener("click", () => {
            displayCount += 10;
            renderVideos();
            window.scrollBy({ top: 300, behavior: 'smooth' });
        });
    }

    // Sayfa yüklendiğinde videoları yüklemeyi başlat
    await loadVideos(); // <--- BURAYI 'await' OLARAK İŞARETLEDİK!
}); // <-- BURASI KODUN SONU OLMALI, ALTINDA HİÇBİR ŞEY OLMAMALI

    function toTitleCase(str) {
    return str.replace(/\w\S*/g, word => word.charAt(0).toUpperCase() + word.substring(1).toLowerCase());
}
