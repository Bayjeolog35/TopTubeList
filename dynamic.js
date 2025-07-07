document.addEventListener("DOMContentLoaded", () => {
    // Video verilerini yükle
    const pageName = "{name}"; // Bu, Python tarafından doldurulmalı veya JS içinde URL'den alınmalı.
                              // Aşağıdaki 'getCountryFromURL()' fonksiyonu zaten bunu yaptığı için bu satır gereksiz.

    // --- Hamburger Menü ---
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
            const allButtons = document.querySelectorAll(".country-column button");

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
    const style = document.createElement('style'); // Bu satır artık burada tanımlanmalı
    style.textContent = `
        @keyframes fadeOut {
            0% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; transform: translateY(10px); }
        }`;
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

    function getCountryFromURL() {
        const path = window.location.pathname;
        return path.split('/').pop().replace('.html', '').toLowerCase();
    }

    function createVideoCard(video) {
        const card = document.createElement("div");
        card.className = "video-card";
        card.innerHTML = `
            <a href="${video.url}" target="_blank" class="video-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy" />
                <span class="duration">${video.duration || ''}</span>
            </a>
            <div class="video-info">
                <h2>${video.title}</h2>
                <div class="meta">
                    <span class="channel">${video.channel}</span>
                    <span class="views">${video.views_str} views</span>
                    <span class="date">${new Date(video.uploadDate).toLocaleDateString()}</span>
                </div>
            </div>
        `;
        return card;
    }

    function showNoDataMessage() {
        container.innerHTML = `
            <div class="no-data-message">
                <img src="no-data.svg" alt="No data" width="100">
                <h3>📊 Sorry, YouTube does not provide statistics for this country</h3>
                <p>Would you like to explore other countries instead?</p>
                <a href="index.html" class="site-button">Go Back to Homepage</a>
            </div>
        `;
        loadMoreBtn.style.display = "none";
    }

    function renderVideos() {
        container.innerHTML = "";

        if (allVideos.length === 0) {
            showNoDataMessage();
            return;
        }

        const fragment = document.createDocumentFragment();
        allVideos.slice(0, displayCount).forEach(video => {
            const card = createVideoCard(video);
            fragment.appendChild(card);
            setTimeout(() => card.classList.add("show"), 50);
        });

        container.appendChild(fragment);
        loadMoreBtn.style.display = displayCount >= allVideos.length ? "none" : "block";
    }

    async function loadVideos() {
        const country = getCountryFromURL();
        const dataFile = `videos_${country}.json`;

        try {
            const response = await fetch(dataFile);
            if (!response.ok) throw new Error('Data not found');

            allVideos = await response.json();
            document.title = `Trending in ${country.charAt(0).toUpperCase() + country.slice(1)} | TopTubeList`;
            renderVideos();
        } catch (error) {
            console.error("Veri yükleme hatası:", error);
            showNoDataMessage();
        }
    }

    loadMoreBtn.addEventListener("click", () => {
        displayCount += 10;
        renderVideos();
        window.scrollBy({ top: 300, behavior: 'smooth' });
    });

    loadVideos(); // Sayfa yüklendiğinde videoları yüklemeyi başlat
});
