import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_URL = "https://www.googleapis.com/youtube/v3/videos"
OUTPUT_FILE = "videos.json"
STRUCTURED_DATA_FILE = "structured_data.json"

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

        views_str = (
            f"{views_int / 1_000_000_000:.2f}B" if views_int >= 1_000_000_000 else
            f"{views_int / 1_000_000:.2f}M" if views_int >= 1_000_000 else
            str(views_int)
        )

        video_url = f"https://www.youtube.com/watch?v={item['id']}"
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]

        # JSON için sade video listesi
        videos.append({
            "title": item["snippet"]["title"],
            "views": views_int,
            "views_str": views_str,
            "url": video_url,
            "thumbnail": thumbnail
        })

        # Structured data için schema.org VideoObject
        structured_items.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": item["snippet"]["title"],
            "description": item["snippet"].get("description", ""),
            "thumbnailUrl": thumbnail,
            "uploadDate": item["snippet"].get("publishedAt", datetime.utcnow().isoformat() + "Z"),
            "contentUrl": video_url,
            "embedUrl": f"https://www.youtube.com/embed/{item['id']}"
        })

    # En çok izlenene göre sırala
    videos = sorted(videos, key=lambda x: x["views"], reverse=True)

    # Dosyalara yaz
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_items, f, ensure_ascii=False, indent=2)

    print("✅ videos.json ve structured_data.json dosyaları oluşturuldu.")
else:
    print(f"❌ API hatası: {response.status_code}")
