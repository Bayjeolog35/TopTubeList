ocument.addEventListener("DOMContentLoaded", () => {
  const pageName = document.body.getAttribute("data-page");

  async function loadVideos() {
    try {
      const response = await fetch(`videos_${pageName}.json`);
      if (!response.ok) throw new Error("Veri alınamadı");
      const allVideos = await response.json();
      console.log(allVideos); // Render işlemleri burada
    } catch (error) {
      console.error("Hata:", error);
    }
  }

  loadVideos();
});
