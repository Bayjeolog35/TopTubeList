'use strict';
// dynamic.js - TopTubeList için Etkileşimli UI betikleri
// Şunları yönetir: menü, karanlık mod, filtreler, video yükleme ve iletişim formu

document.addEventListener("DOMContentLoaded", async () => {
  // --- UI Element References ---
  const hamburger = document.querySelector(".hamburger");
  const countryPanel = document.querySelector(".country-panel");
  const darkModeToggle = document.getElementById("darkModeToggle");
  const savedMode = localStorage.getItem("darkMode");
  const contactToggle = document.getElementById("contactToggle");
  const contactContent = document.getElementById("contactContent");
  const aboutToggle = document.getElementById("aboutToggle");
  const aboutContent = document.getElementById("aboutContent");
  const contactForm = document.getElementById("contactForm");
  const formStatusDiv = document.getElementById("formStatus");
  const videoListContainer = document.getElementById("videoList");
  const loadMoreButton = document.getElementById("loadMoreBtn");

  // --- Video Render State ---
  let allVideos = [];
  let displayCount = 10;

  // --- Helpers ---
  function getCountryFromURL() {
    const path = window.location.pathname.replace(/\/+$/, "");
    let slug = path.split("/").pop() || "index";
    if (slug.endsWith(".html")) slug = slug.slice(0, -5);
    return slug.toLowerCase();
  }

  function createVideoCard(video) {
    function formatViews(num) {
      const n = Number(num) || 0;
      if (n >= 1_000_000_000) return (n / 1_000_000_000).toFixed(2).replace(/\.?0+$/, '') + "B";
      if (n >= 1_000_000)     return (n / 1_000_000).toFixed(2).replace(/\.?0+$/, '') + "M";
      if (n >= 1_000)         return Math.round(n / 1_000) + "K";
      return String(n);
    }

    const card = document.createElement("div");
    card.className = "video-card";
    card.style.position = "relative";

    const published =
      video.published_date_formatted ||
      (video.published_at ? new Date(video.published_at).toLocaleDateString("tr-TR") : "");

    const viewChange = Number(video.viewChange || 0);
    const trendText = viewChange !== 0 ? (video.viewChange_str || String(viewChange)) : null;
    const trendColor = viewChange > 0 ? "#28a745" : viewChange < 0 ? "#dc3545" : "inherit";

    let rankChange = 0;
    if (typeof video.rankChange === "number" && !Number.isNaN(video.rankChange)) {
      rankChange = video.rankChange;
    } else if (
      video.previousRank != null && video.rank != null &&
      !Number.isNaN(Number(video.previousRank)) && !Number.isNaN(Number(video.rank))
    ) {
      rankChange = Number(video.previousRank) - Number(video.rank);
    }

    const arrowType = rankChange > 0 ? "up" : rankChange < 0 ? "down" : "zero";
    const iconMap = { up: "up.webp", down: "down.webp", zero: "zero.webp" };
    const trendIconPath = iconMap[arrowType];

    let rankChangeHtml = "";
    if (rankChange > 0) {
      rankChangeHtml =
        '<span class="rank-change" style="display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:20px;padding:0 4px;border-radius:4px;font-weight:700;font-size:13px;color:#fff;background:#28a745;">+' +
        rankChange + "</span>";
    } else if (rankChange < 0) {
      rankChangeHtml =
        '<span class="rank-change" style="display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:20px;padding:0 4px;border-radius:4px;font-weight:700;font-size:13px;color:#fff;background:#dc3545;">' +
        rankChange + "</span>";
    }

    const is480 = window.matchMedia("(max-width: 480px)").matches;
    const is360 = window.matchMedia("(max-width: 360px)").matches;
    const trendLabel = is480 ? "View change (3h):" : "View Change (Last 3h):";

    const durationHtml = video.duration ? '<span class="duration">' + video.duration + "</span>" : "";
    const publishedHtml = published ? '<p><strong>Date:</strong> ' + published + "</p>" : "";
    const trendInfoHtml = trendText
      ? '<p class="trend-info" style="color:' + trendColor + '; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><strong>' +
        trendLabel + "</strong> " + trendText + "</p>"
      : "";

    // --- KART HTML ---
    card.innerHTML =
      '<div class="thumb-wrap">' +
        '<a href="' + video.url + '" target="_blank" rel="noopener" class="video-thumbnail">' +
          '<img class="thumbnail" src="' + video.thumbnail + '" alt="' +
            video.title.replace(/"/g, "&quot;") + '" loading="lazy" width="320" height="180" />' +
          durationHtml +
        '</a>' +
      '</div>' +
      '<div class="video-info">' +
        "<h2>" + video.title + "</h2>" +
        "<p><strong>Channel:</strong> " + video.channel + "</p>" +
        "<p><strong>Views:</strong> " + formatViews(video.views) + " views</p>" +
        publishedHtml +
        trendInfoHtml +
      "</div>" +
      '<div class="trend-badge">' +
        rankChangeHtml +
        '<img src="' + trendIconPath + '" alt="' + arrowType + '" class="trend-icon" />' +
      "</div>";

    const badge = card.querySelector(".trend-badge");
    const info  = card.querySelector(".video-info");
    const icon  = card.querySelector(".trend-icon");

    if (badge) {
      Object.assign(badge.style, {
        position: "absolute",
        right: "12px",
        top: "50%",
        transform: "translateY(-50%)",
        width: "60px",
        height: "28px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: "6px",
        pointerEvents: "none",
      });
    }
    if (info) info.style.paddingRight = "72px";
    if (icon) Object.assign(icon.style, {
      width: "20px",
      height: "20px",
      objectFit: "contain",
      display: "block",
    });

    if (is480 && badge && info) {
      badge.style.width = "50px";
      badge.style.height = "26px";
      badge.style.right = "8px";
      info.style.paddingRight = "60px";
      const rc = card.querySelector(".rank-change");
      if (rc) rc.style.fontSize = "12px";
    }
    if (is360 && badge && info) {
      badge.style.width = "46px";
      badge.style.right = "6px";
      info.style.paddingRight = "54px";
    }

    return card;
  }

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

    Object.assign(videoListContainer.style, {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minHeight: "50vh",
      gap: "8px",
      textAlign: "center",
    });

    if (loadMoreButton) loadMoreButton.style.display = "none";
  }

  // --- Data load + simple render ---
  async function loadVideos() {
    const country = getCountryFromURL();
    const dataFile =
      country === "index" || country === ""
        ? "index.videos.json"
        : `${country}.vid.data.json`;

    try {
      const response = await fetch(dataFile);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`'${dataFile}' dosyası bulunamadı. URL: ${response.url}`);
        }
        throw new Error(`Veri yüklenirken HTTP hatası: ${response.status} ${response.statusText}`);
      }

      const jsonData = await response.json();
      if (!Array.isArray(jsonData)) throw new Error("Yüklenen veri bir dizi değil.");

      allVideos = jsonData.map(v => ({ ...v, viewChange: Number(v?.viewChange) || 0 }));
      allVideos.sort((a, b) => b.viewChange - a.viewChange);

      if (allVideos.length === 0) throw new Error("Video verisi boş.");

      if (country !== "index" && country !== "") {
        document.title = `Trending in ${country.charAt(0).toUpperCase() + country.slice(1)} | TopTubeList`;
      }

      renderVideos();
    } catch (error) {
      console.error("Veri yükleme hatası:", error);
      showNoDataMessage();
    }
  }

  function renderVideos() {
    if (!videoListContainer) {
      console.warn("videoListContainer bulunamadı, videolar render edilemiyor.");
      return;
    }

    // önceki no-data stillerini temizle
    ["display","flexDirection","alignItems","justifyContent","minHeight","gap","textAlign"]
      .forEach(p => videoListContainer.style.removeProperty(p));

    videoListContainer.innerHTML = "";
    const videosToDisplay = allVideos.slice(0, displayCount);

    if (videosToDisplay.length === 0) {
      showNoDataMessage();
      return;
    }

    videosToDisplay.forEach(video => {
      const card = createVideoCard(video);
      videoListContainer.appendChild(card);
    });

    if (loadMoreButton) {
      loadMoreButton.style.display = displayCount >= allVideos.length ? "none" : "block";
    }
  }

  // --- Events & Setup ---
  const setupResponsivePanel = () => {
    if (hamburger && countryPanel) {
      if (window.innerWidth <= 768) {
        hamburger.style.display = "block";
        countryPanel.classList.remove("active");
        countryPanel.style.display = "";
      } else {
        hamburger.style.display = "none";
        countryPanel.classList.add("active");
        countryPanel.style.display = "flex";
      }
    } else if (hamburger) {
      hamburger.style.display = window.innerWidth <= 768 ? "block" : "none";
    }
  };

  setupResponsivePanel();
  window.addEventListener("resize", setupResponsivePanel);

  if (hamburger && countryPanel) {
    hamburger.addEventListener("click", () => {
      countryPanel.classList.toggle("active");
    });
  }

  if (savedMode === "true") document.body.classList.add("dark-mode");
  if (darkModeToggle) {
    darkModeToggle.addEventListener("click", () => {
      const isDarkNow = document.body.classList.toggle("dark-mode");
      localStorage.setItem("darkMode", isDarkNow);
    });
  }

  document.querySelectorAll(".alphabet-letter").forEach(letter => {
    letter.addEventListener("click", function (e) {
      e.preventDefault();
      const selectedLetter = this.getAttribute("data-letter");
      const allLinks = document.querySelectorAll(".country-column .country-link");

      allLinks.forEach(link => {
        const countryName = link.textContent.trim();
        const linkFirstLetter = countryName.charAt(0).toUpperCase();
        link.style.display =
          selectedLetter === "all" || (linkFirstLetter && linkFirstLetter === selectedLetter.toUpperCase())
            ? "block" : "none";
      });

      document.querySelectorAll(".alphabet-letter").forEach(a => a.classList.remove("active"));
      this.classList.add("active");
    });
  });

  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeOut {
      0% { opacity: 1; }
      80% { opacity: 1; }
      100% { opacity: 0; transform: translateY(10px); }
    }`;
  document.head.appendChild(style);

  function toggleContent(element) {
    if (!element) return;
    if (element.classList.contains("show")) {
      element.classList.remove("show");
      setTimeout(() => { element.style.display = "none"; }, 400);
    } else {
      element.style.display = "block";
      setTimeout(() => {
        element.classList.add("show");
        element.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 10);
    }
  }

  if (contactToggle && contactContent) {
    contactToggle.addEventListener("click", () => toggleContent(contactContent));
  }
  if (aboutToggle && aboutContent) {
    aboutToggle.addEventListener("click", () => toggleContent(aboutContent));
  }

  if (contactForm && formStatusDiv) {
    contactForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = new FormData(contactForm);
      try {
        const response = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(formData).toString()
        });
        if (!response.ok) throw new Error("Form gönderilirken sunucu hatası oluştu.");

        contactForm.reset();
        formStatusDiv.innerText = "✅ ✅ Message sent successfully!";
        formStatusDiv.style.display = "block";
        formStatusDiv.style.cssText = `
          position: fixed; bottom: 20px; right: 20px;
          background: #28a745; color: white; padding: 12px 24px;
          border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
          font-family: sans-serif; z-index: 9999;
          animation: fadeOut 5s forwards;`;
        setTimeout(() => formStatusDiv.remove(), 5000);
      } catch (error) {
        console.error("Form gönderme hatası:", error);
        alert("❌ Mesaj gönderilemedi. Lütfen tekrar deneyin.");
      }
    });
  }

  // Load More
  if (loadMoreButton) {
    loadMoreButton.addEventListener("click", () => {
      displayCount += 10;
      renderVideos();
      window.scrollBy({ top: 300, behavior: 'smooth' });
    });
  }

  // Başlat
  loadVideos();
}); // DOMContentLoaded kapanış

// (opsiyonel) dışarıda kalsın
function toTitleCase(str) {
  return str.replace(/\w\S*/g, w => w.charAt(0).toUpperCase() + w.substring(1).toLowerCase());
}
