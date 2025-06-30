import requests
import json
import os
from datetime import datetime

# 🔐 API key artık gizli bir çevre değişkeninden alınacak
API_KEY = os.getenv("YOUTUBE_API_KEY")
API_URL = "https://www.googleapis.com/youtube/v3/videos"
OUTPUT_FILE = "videos.json"
STRUCTURED_DATA_FILE = "structured_data.json"
HTML_FILE = "index.html"

params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "maxResults": 50,
    "regionCode": "US",
    "key": API_KEY
}
response = requests.get(API_URL, params=params)

if response.status_code == 200:
    data = response.json()
    videos = []
    structured_items = []

    for item in data["items"]:
        try:
            views_int = int(item["statistics"]["viewCount"])
        except:
            views_int = 0

        if views_int >= 1_000_000_000:
            views_str = f"{views_int/1_000_000_000:.2f}B"
        elif views_int >= 1_000_000:
            views_str = f"{views_int/1_000_000:.2f}M"
        else:
            views_str = str(views_int)

        video_url = f"https://www.youtube.com/watch?v={item['id']}"
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]

        # -- videos.json için --
        video = {
            "title": item["snippet"]["title"],
            "views": views_int,
            "views_str": views_str,
            "url": video_url,
            "thumbnail": thumbnail
        }
        videos.append(video)

        # -- structured_data.json için --
        structured = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": item["snippet"]["title"],
            "description": item["snippet"].get("description", ""),
            "thumbnailUrl": thumbnail,
            "uploadDate": item["snippet"].get("publishedAt", datetime.utcnow().isoformat() + "Z"),
            "contentUrl": video_url,
            "embedUrl": f"https://www.youtube.com/embed/{item['id']}"
        }
        structured_items.append(structured)

    # Sıralama
    videos = sorted(videos, key=lambda x: x["views"], reverse=True)

    # JSON çıktıları
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_items, f, ensure_ascii=False, indent=2)

    print("✅ videos.json ve structured_data.json güncellendi.")

    # HTML'e gömme
    with open(STRUCTURED_DATA_FILE, "r", encoding="utf-8") as f:
        structured_json = f.read()
    structured_script = f'<script type="application/ld+json">\n{structured_json}\n</script>'

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    html_content = html_content.replace("<!-- STRUCTURED_DATA_HERE -->", structured_script)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ index.html içine structured data gömüldü.")

else:
    print("❌ API Hatası:", response.status_code)
