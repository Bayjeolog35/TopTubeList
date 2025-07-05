<script>

 /*hamburger menü*/
  
document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const panel = document.querySelector(".country-panel");

  if (hamburger && panel) {
    hamburger.addEventListener("click", () => {
      panel.classList.toggle("active");
    });
  }
});


/*hamburger menü son*/
  // --- Dark Mode Toggle ---
document.addEventListener("DOMContentLoaded", () => {
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
});

document.addEventListener("DOMContentLoaded", function () {
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


    // --- About Us Scroll + Toggle ---
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

    // --- Contact Us Scroll + Toggle ---
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

    // --- Harf filtreleme ---
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

    // --- Logo scroll to top ---
    const logoLink = document.getElementById("logoLink");
    if (logoLink) {
        logoLink.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // --- FadeOut animation style block ---
    const style = document.createElement("style");
    style.textContent = `
        @keyframes fadeOut {
            0% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; transform: translateY(10px); }
        }
    `;
    document.head.appendChild(style);
});
</script>
