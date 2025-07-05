// script.js

// Tek bir DOMContentLoaded dinleyicisi kullanmak daha iyidir.
// Tüm sayfa elemanları yüklendiğinde çalışacak ana blok.
document.addEventListener("DOMContentLoaded", () => {

    /* --- Hamburger Menü --- */
    const hamburger = document.querySelector(".hamburger");
    const panel = document.querySelector(".country-panel");

    if (hamburger && panel) {
        hamburger.addEventListener("click", () => {
            panel.classList.toggle("active");
        });
    }

    /* --- Dark Mode Toggle --- */
    const darkModeToggle = document.getElementById("darkModeToggle");

    // Sayfa yüklendiğinde dark mode'u uygula
    const savedMode = localStorage.getItem("darkMode");
    if (savedMode === "true") {
        document.body.classList.add("dark-mode");
    }

    // Tıklanınca dark mode'u toggle et
    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", () => {
            const isDarkNow = document.body.classList.toggle("dark-mode");
            localStorage.setItem("darkMode", isDarkNow);
        });
    }


    /* --- Video Yükleme ve Daha Fazla Butonu --- */
    let allVideos = [];
    let displayCount = 0;
    const videoList = document.getElementById("videoList");
    const loadMoreBtn = document.getElementById("loadMoreBtn");

    function renderVideos(startIndex = 0) {
        const videosToAdd = allVideos.slice(startIndex, displayCount);
        videosToAdd.forEach((video, index) => {
            const card = document.createElement("div");
            card.classList.add("video-card");
            card.innerHTML = `
                <img src="${video.thumbnail}" alt="${video.title}" />
                <div class="video-info">
                    <h2>${video.title}</h2>
                    <p><strong>Views:</strong> ${video.views_str}</p>
                    <a href="${video.url}" target="_blank">Watch on YouTube</a>
                </div>
            `;
            videoList.appendChild(card);

            setTimeout(() => {
                card.classList.add("show");
            }, 50 * index);
        });

        if (loadMoreBtn) {
            loadMoreBtn.style.display = (displayCount >= allVideos.length) ? "none" : "block";
        }
    }

    fetch("videos.json")
        .then(response => response.json())
        .then(videos => {
            allVideos = videos;
            displayCount = 10;
            renderVideos(0);
        })
        .catch(error => {
            console.error("❌ Error fetching videos.json:", error);
        });

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener("click", () => {
            const previousDisplayCount = displayCount;
            displayCount += 10;
            renderVideos(previousDisplayCount);
        });
    }


    /* --- Ülke ve Kıta Butonları Dinamik Yükleme --- */
    let allCountries = []; // Ülke verisini tutacak dizi
    const countryColumn = document.querySelector(".country-column"); // country-column div'i buraya taşıdık

    // Ülke butonlarını dinamik olarak oluşturan fonksiyon
    function generateCountryButtons(countriesToDisplay) {
        if (!countryColumn) {
            console.error("country-column div bulunamadı!");
            return;
        }

        countryColumn.innerHTML = ''; // Her çağrıldığında mevcut içeriği temizle

        countriesToDisplay.forEach(country => {
            const button = document.createElement("button");
            button.textContent = country.name;
            button.setAttribute("data-letter", country.letter);
            // Ülke butonlarına kıta bilgisini de ekleyebiliriz (filtreleme için)
            if (country.continent) {
                 button.setAttribute("data-continent", country.continent);
            }
            button.onclick = function() {
                location.href = country.link;
            };
            countryColumn.appendChild(button);
        });
    }

    // Ülke verisini JSON dosyasından çek
    fetch("countries.json") // Oluşturduğumuz JSON dosyasının yolu
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            allCountries = data; // Çekilen veriyi global değişkene ata

            // Mevcut sayfanın URL'sini al ve kıta ismini çıkar (örn: "asia.html" -> "asia")
            const currentPagePath = window.location.pathname.split('/').pop();
            const currentContinentSlug = currentPagePath.replace(".html", "").replace(".htm", ""); // .html veya .htm uzantısını kaldır

            let countriesToDisplayInitial = allCountries;

            // Eğer şu anki sayfa bir kıta sayfasıysa (örn: asia.html), sadece o kıtanın ülkelerini filtrele
            // "index.html" veya boş string (ana sayfa) değilse filtrele
            if (currentContinentSlug && currentContinentSlug !== "index") {
                // Kıta sluglarını kontrol edelim (örneğin "north_america", "south_america" vb.)
                const validContinents = new Set(allCountries.map(c => c.continent));
                if (validContinents.has(currentContinentSlug)) {
                    countriesToDisplayInitial = allCountries.filter(country => country.continent === currentContinentSlug);
                } else {
                    console.warn(`"${currentContinentSlug}" bir kıta slug'ı değil veya veride bulunmuyor.`);
                }
            }

            generateCountryButtons(countriesToDisplayInitial); // Başlangıçta ilgili ülkeleri göster
        })
        .catch(error => {
            console.error("❌ Ülke verisi çekilemedi:", error);
            // Kullanıcıya bir mesaj gösterebilirsiniz
            if (countryColumn) {
                countryColumn.innerHTML = "<p>Ülke listesi yüklenirken bir hata oluştu.</p>";
            }
        });


    /* --- Harf Filtreleme (ülke butonları artık dinamik) --- */
    document.querySelectorAll(".alphabet-letter").forEach(letter => {
        letter.addEventListener("click", function (e) {
            e.preventDefault();
            const selectedLetter = this.getAttribute("data-letter");
            let filteredCountries = [];

            if (selectedLetter === "all") {
                filteredCountries = allCountries;
            } else {
                // Sadece JSON'dan gelen veriyi filtreliyoruz, DOM'daki butonları değil
                filteredCountries = allCountries.filter(country => country.letter === selectedLetter);
            }
            generateCountryButtons(filteredCountries); // Filtrelenmiş ülkeleri yeniden oluştur

            // Aktif harfi vurgula
            document.querySelectorAll(".alphabet-letter").forEach(a => a.classList.remove("active"));
            this.classList.add("active");
        });
    });


    /* --- About Us Scroll + Toggle --- */
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
                    aboutContent.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }, 10);
            }
        });
    }

    /* --- Contact Us Scroll + Toggle --- */
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
                    contactContent.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }, 10);
            }
        });
    }

    /* --- Contact Form Submission --- */
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

    /* --- Logo scroll to top --- */
    const logoLink = document.getElementById("logoLink");
    if (logoLink) {
        logoLink.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    /* --- FadeOut animation style block (CSS dosyasına taşımanız tavsiye edilir) --- */
    const style = document.createElement("style");
    style.textContent = `
        @keyframes fadeOut {
            0% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; transform: translateY(10px); }
        }
    `;
    document.head.appendChild(style);

}); // DOMContentLoaded bitişi
