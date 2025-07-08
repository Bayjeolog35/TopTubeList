'use strict';
// dynamic.js - Interactive UI scripts for TopTubeList
// Handles: menu, dark mode, filters, video loading, and contact form


document.addEventListener("DOMContentLoaded", () => {
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
        const filename = path.split('/').pop(); // "index.html"
        const countryName = filename.replace('.html', '').toLowerCase(); // "index"

        // Eğer ana sayfa URL'sindeysek ve özel bir JSON adı istiyorsak, burada ayarlanır.
        // Örneğin, index.html için 'worldwide.vid.data.json' gibi bir dosya arıyorsak.
        // Bu örnekte 'index' ise 'worldwide' döndürülecek.
        return countryName === "index" ? "worldwide" : countryName;
    }

    /**
     * Creates an HTML video card element from a video object.
     * @param {Object} video - The video data object.
     * @returns {HTMLElement} The created video card div.
     */
    function createVideoCard(video) {
        const card = document.createElement("div");
        card.className = "video-card";
        card.innerHTML = `
            <a href="${video.url}" target="_blank" class="video-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy" />
                ${video.duration ? `<span class="duration">${video.duration}</span>` : ''}
            </a>
            <div class="video-info">
                <h2>${video.title}</h2>
                <div class="meta">
                    <span class="channel">${video.channel}</span>
                    <span class="views">${video.views_formatted} views</span>
                    <span class="date">${new Date(video.published_at).toLocaleDateString('tr-TR')}</span>
                </div>
            </div>
        `;
        return card;
    }

    

    /**
     * Renders the current subset of videos to the DOM.
     */
    function renderVideos() {
        if (!videoListContainer) {
            console.warn("videoListContainer bulunamadı. Videolar render edilemiyor.");
            return;
        }

        videoListContainer.innerHTML = ""; // Önceki videoları temizle

        if (!Array.isArray(allVideos) || allVideos.length === 0) {
            showNoDataMessage();
            return;
        }

        const fragment = document.createDocumentFragment();
        allVideos.slice(0, displayCount).forEach(video => {
            const card = createVideoCard(video);
            fragment.appendChild(card);
            // Kartların görünmesini geciktirmek yerine CSS geçişi (transition) ile yönetmek daha iyi
            // setTimeout(() => card.classList.add("show"), 50); // Bu satır kaldırıldı
        });

        videoListContainer.appendChild(fragment);

        // Load More butonunun görünürlüğünü ayarla
        if (loadMoreButton) {
            loadMoreButton.style.display = displayCount >= allVideos.length ? "none" : "block";
        }
    }

    /**
     * Fetches video data for the current country from a JSON file.
     */
    async function loadVideos() {
        const country = getCountryFromURL();
        const dataFile = `${country}.vid.data.json`;

        console.log(`Veri yükleme denemesi: ${dataFile}`); // Debug için

        try {
            const response = await fetch(dataFile);

            // HTTP hata kodlarını (örn. 404, 500) kontrol et
            if (!response.ok) {
                // Spesifik hata mesajları için status kodlarını kontrol et
                if (response.status === 404) {
                    throw new Error(`'${dataFile}' dosyası bulunamadı. URL: ${response.url}`);
                }
                throw new Error(`Veri yüklenirken HTTP hatası oluştu: ${response.status} ${response.statusText}`);
            }

            const jsonData = await response.json(); // <-- JSON parse işlemi burada
            console.log("Yüklenen JSON verisi (ilk 5 video):", jsonData.slice(0, 5)); // Debug için

            // Gelen verinin beklenen formatta (dizi) olup olmadığını kontrol et
            if (!Array.isArray(jsonData)) {
                throw new Error('Yüklenen veri bir dizi değil. Beklenen JSON formatı geçersiz.');
            }

            allVideos = jsonData; // Veriyi global değişkene ata

            if (allVideos.length === 0) {
                throw new Error('Yüklenen video verisi boş bir dizi.');
            }

            // Sayfa başlığını ayarla
            document.title = `Trending in ${country.charAt(0).toUpperCase() + country.slice(1)} | TopTubeList`;

            // Videoları render et
            renderVideos();

        } catch (error) {
            console.error("Veri yükleme hatası:", error);
            showNoDataMessage(); // Hata durumunda "veri yok" mesajını göster
        }
    }

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
            //     countryPanel.style.display = "flex";
            // } else {
            //     countryPanel.style.display = "none";
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
            const selectedLetter = this.getAttribute("data-letter");
            const allButtons = document.querySelectorAll(".country-column button");

            allButtons.forEach(btn => {
                // 'data-letter' attribute'ünün olup olmadığını kontrol et
                const btnLetter = btn.getAttribute("data-letter");
                if (selectedLetter === "all" || (btnLetter && btnLetter.toLowerCase() === selectedLetter.toLowerCase())) {
                    btn.style.display = "block";
                } else {
                    btn.style.display = "none";
                }
            });

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
    loadVideos();
});
