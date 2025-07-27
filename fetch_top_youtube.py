import requests
import json
import os
import re
from datetime import datetime

# 🔐 API Key
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("❌ API anahtarı bulunamadı.")

# 📁 Dosya yolları
OUTPUT_FILE = "index.videos.json"
STRUCTURED_DATA_FILE = "index.structured_data.json"
HTML_FILE = "index.html"

# 📌 Placeholder’lar
STRUCTURED_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*<!-- STRUCTURED_DATA_HERE -->(.*?)</script>',
    re.DOTALL
)
IFRAME_PATTERN = re.compile(
    r'<!-- IFRAME_VIDEO_HERE -->(.*?)<!-- IFRAME_VIDEO_HERE_END -->',
    re.DOTALL
)

# 📦 API Request
params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "maxResults": 50,
    "key": API_KEY
}

response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)

if response.status_code == 200:
    data = response.json()
    videos = []
    structured_items = []

    for item in data["items"]:
        try:
            views_int = int(item["statistics"]["viewCount"])
        except:
            views_int = 0

        views_str = (
            f"{views_int/1_000_000_000:.2f}B" if views_int >= 1_000_000_000 else
            f"{views_int/1_000_000:.2f}M" if views_int >= 1_000_000 else
            str(views_int)
        )

        video = {
            "id": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "embed_url": f"https://www.youtube.com/embed/{item['id']}",
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "published_at": item["snippet"].get("publishedAt", ""),
            "published_date_formatted": datetime.fromisoformat(item["snippet"].get("publishedAt", "").replace("Z", "+00:00")).strftime("%d.%m.%Y")
                if item["snippet"].get("publishedAt", "") else "Tarih Yok"
        }
        videos.append(video)

        structured_items.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": item["snippet"]["title"],
            "description": item["snippet"].get("description", "").strip() or item["snippet"]["title"],
            "thumbnailUrl": video["thumbnail"],
            "uploadDate": video["published_at"],
            "embedUrl": video["embed_url"],
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": views_int
            }
        })

    # ⬇ JSON dosyaları kaydet
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_items, f, ensure_ascii=False, indent=2)

    print("✅ JSON dosyaları kaydedildi.")

    # 🧠 HTML güncelle
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 📌 Structured Data Güncelle
    with open(STRUCTURED_DATA_FILE, "r", encoding="utf-8") as f:
        structured_json = f.read()
    structured_block = f'<script type="application/ld+json">\n<!-- STRUCTURED_DATA_HERE -->\n{structured_json}\n</script>'
    html = STRUCTURED_PATTERN.sub(structured_block, html)

    # 📌 Iframe Güncelle
    top_video = videos[0]
    iframe_block = f'''<!-- IFRAME_VIDEO_HERE -->
<iframe 
  width="560" 
  height="315" 
  src="https://www.youtube.com/embed/{top_video['id']}" 
  title="{top_video['title']}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>
<!-- IFRAME_VIDEO_HERE_END -->'''

    if IFRAME_PATTERN.search(html):
        html = IFRAME_PATTERN.sub(iframe_block, html)
    else:
        # Eğer ilk kez ekleniyorsa
        html = html.replace("</body>", f"{iframe_block}\n</body>")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html içine iframe ve structured data başarıyla güncellendi.")

else:
    print("❌ API Hatası:", response.status_code)
