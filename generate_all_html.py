import os
import json

VIDEO_DATA_DIR = "."
OUTPUT_DIR = "."

def load_video_data(name):
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.vid.data.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_structured_data(name):
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.str.data.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_html(name, videos, structured_data):
    readable_name = name.replace("-", " ").title()

    # Structured Data (JSON-LD)
    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2, ensure_ascii=False)
        structured_data_block = f"""
  <script type="application/ld+json">
{structured_json}
  </script>
"""
    script_block = """
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
    const style = document.createElement("style");
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
          // CSS stilindeki noktalama hatası düzeltildi: tek bir string olmalı
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
      <p>Would you like to explore
