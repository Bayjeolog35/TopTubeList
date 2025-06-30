import json
import requests
from time import sleep
import os
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

    # Aynı URL'den sadece yüksek izlenmeye sahip olan kalsın
    unique_videos = {}
    for video in all_videos:
        if video["url"] not in unique_videos or video["views"] > unique_videos[video["url"]]["views"]:
            unique_videos[video["url"]] = video

    top_50 = sorted(unique_videos.values(), key=lambda x: x["views"], reverse=True)[:50]

    with open(f"videos_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(top_50, f, ensure_ascii=False, indent=2)

    structured_data = [generate_video_object(v) for v in top_50]
    with open(f"structured_data_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: videos_{continent}.json & structured_data_{continent}.json")

   # ➕ İlk video için yalnızca gizli iframe oluştur
first_item = data["items"][0]
first_video_id = first_item["id"]
first_title = first_item["snippet"]["title"]
iframe_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{first_video_id}" title="{first_title}" frameborder="0" allowfullscreen style="display:none;"></iframe>'

# HTML'de <!-- VIDEO_EMBEDS --> etiketiyle değiştir
if "<!-- VIDEO_EMBEDS -->" in html_content:
    html_content = html_content.replace("<!-- VIDEO_EMBEDS -->", iframe_code)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ index.html içine gizli iframe eklendi.")
else:
    print("⚠️ index.html içinde <!-- VIDEO_EMBEDS --> etiketi bulunamadı.")

        print(f"❌ {html_file} bulunamadı.")
