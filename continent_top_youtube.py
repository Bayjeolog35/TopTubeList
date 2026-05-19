import json
import requests
from time import sleep
import os
import re
from datetime import datetime

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_URL = "https://www.googleapis.com/youtube/v3/videos"
PART = "snippet,statistics"
MAX_RESULTS = 50

continent_countries = {
    "asia": ["IN", "JP", "KR", "ID", "PH"],
    "europe": ["GB", "DE", "FR", "IT", "TR"],
    "africa": ["NG", "ZA", "EG"],
    "north_america": ["US", "CA", "MX"],
    "south_america": ["BR", "AR", "CO"],
    "oceania": ["AU", "NZ"]
}

def fetch_videos(region_code):
    params = {
        "part": PART,
        "chart": "mostPopular",
        "maxResults": MAX_RESULTS,
        "regionCode": region_code,
        "key": API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"❌ API error for {region_code}: {response.status_code}")
        return []

def generate_video_object(video):
    return {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": video["title"],
        "thumbnailUrl": video["thumbnail"],
        "uploadDate": video.get("uploadDate", datetime.utcnow().isoformat() + "Z"),
        "description": video["title"],
        "contentUrl": video["url"],
        "embedUrl": video["url"].replace("watch?v=", "embed/")
    }

for continent, countries in continent_countries.items():
    all_videos = []

    print(f"🌍 Processing {continent.upper()}...")
    for country in countries:
        print(f"  📥 Fetching from {country}...")
        videos = fetch_videos(country)
        for item in videos:
            try:
                views = int(item["statistics"]["viewCount"])
                video = {
                    "title": item["snippet"]["title"],
                    "views": views,
                    "views_str": f"{views / 1_000_000:.2f}M" if views >= 1_000_000 else str(views),
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                    "uploadDate": item["snippet"].get("publishedAt", datetime.utcnow().isoformat() + "Z"),
                    "videoId": item["id"]
                }
                all_videos.append(video)
            except KeyError:
                continue
        sleep(1)

    # En iyi videoları ayıkla (unique URL'lere göre en çok izlenen)
    unique_videos = {}
    for video in all_videos:
        if video["url"] not in unique_videos or video["views"] > unique_videos[video["url"]]["views"]:
            unique_videos[video["url"]] = video

    top_50 = sorted(unique_videos.values(), key=lambda x: x["views"], reverse=True)[:50]

    # JSON çıktılarını yaz
    with open(f"videos_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(top_50, f, ensure_ascii=False, indent=2)

    structured_data = [generate_video_object(v) for v in top_50]
    with open(f"structured_data_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: videos_{continent}.json & structured_data_{continent}.json")

    # HTML güncelleme işlemleri
    html_file = f"{continent}.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        # 1️⃣ Structured Data yerleştir
        html_content = html_content.replace(
            "<!-- STRUCTURED_DATA_HERE -->",
            f'<script type="application/ld+json">\n{json.dumps(structured_data, indent=2)}\n</script>'
        )

        # 2️⃣ İlk video için gizli iframe oluştur
        first_video = top_50[0]
        iframe_code = f'''
<iframe 
  width="560" 
  height="315" 
  src="https://www.youtube.com/embed/{first_video["videoId"]}" 
  title="{first_video["title"]}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>
'''

        # Eski iframe'i (varsa) temizle
        html_content = re.sub(
            r'<iframe[^>]*style="[^"]*left:-9999px;[^"]*"[^>]*></iframe>',
            '',
            html_content,
            flags=re.DOTALL
        )

        # Yeni iframe'i placeholder yerine koy
        html_content = html_content.replace("<!-- VIDEO_EMBEDS -->", iframe_code)

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ {continent}.html içine iframe ve structured data eklendi.")
    else:
        print(f"⚠️ HTML file {html_file} not found.")
