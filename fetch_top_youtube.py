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
HISTORY_FILE = "index.history.view.json"
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

    # 📚 Önceki history verisini yükle
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            previous_history = json.load(f)
    else:
        previous_history = {}

    for index, item in enumerate(data["items"]):
        video_id = item["id"]

        try:
            views_int = int(item["statistics"]["viewCount"])
        except:
            views_int = 0

        views_str = (
            f"{views_int/1_000_000_000:.2f}B" if views_int >= 1_000_000_000 else
            f"{views_int/1_000_000:.2f}M" if views_int >= 1_000_000 else
            str(views_int)
        )

        # 🔢 Sıra bilgisi
        current_rank = index + 1

        # 📊 Önceki veriye göre fark hesapla
        previous_data = previous_history.get(video_id, {})
        previous_views = previous_data.get("views", views_int)
        previous_rank = previous_data.get("rank", current_rank)

        view_change = views_int - previous_views
        rank_change = previous_rank - current_rank

        trend = "rising" if view_change > 0 else "falling" if view_change < 0 else "stable"

        # ➕/➖ string gösterimler
        view_change_str = f"+{view_change:,}" if view_change > 0 else f"{view_change:,}"
        rank_change_str = f"+{rank_change}" if rank_change > 0 else f"{rank_change}"

        video = {
            "id": video_id,
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "embed_url": f"https://www.youtube.com/embed/{video_id}",
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "published_at": item["snippet"].get("publishedAt", ""),
            "published_date_formatted": datetime.fromisoformat(
                item["snippet"].get("publishedAt", "").replace("Z", "+00:00")
            ).strftime("%d.%m.%Y") if item["snippet"].get("publishedAt", "") else "Tarih Yok",

            # 🆕 Ekstra bilgiler
            "rank": current_rank,
            "viewChange": view_change,
            "viewChange_str": view_change_str,
            "rankChange": rank_change,
            "rankChange_str": rank_change_str,
            "trend": trend
        }
        videos.append(video)

        # Structured data
        structured_items.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": video["title"],
            "description": item["snippet"].get("description", "").strip() or video["title"],
            "thumbnailUrl": video["thumbnail"],
            "uploadDate": video["published_at"],
            "embedUrl": video["embed_url"],
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": views_int
            }
        })

    # 💾 JSON dosyaları kaydet
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_items, f, ensure_ascii=False, indent=2)

    # 🔁 Yeni history dosyasını yaz
    new_history = {
        video["id"]: {
            "views": video["views"],
            "rank": video["rank"]
        } for video in videos
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)

    print("✅ JSON dosyaları ve history dosyası kaydedildi.")

    # 🧠 HTML güncelle
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

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
        html = html.replace("</body>", f"{iframe_block}\n</body>")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html içine iframe ve structured data başarıyla güncellendi.")

else:
    print("❌ API Hatası:", response.status_code)
