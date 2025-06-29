import json
import requests
import os
from time import sleep
from datetime import datetime

API_KEY = "AIzaSyDeEp8zM0PaRG26QlWmACmIkMZVJFu-QW8"
API_URL = "https://www.googleapis.com/youtube/v3/videos"
PART = "snippet,statistics"
MAX_RESULTS = 10  # Her ülkeden 10 video alacağız

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
        "uploadDate": datetime.utcnow().isoformat() + "Z",
        "description": video["title"],
        "contentUrl": video["url"],
        "embedUrl": video["url"].replace("watch?v=", "embed/")
    }

for continent, countries in continent_countries.items():
    all_videos = []
    print(f"\n🌍 Processing {continent.upper()}...")

    for country in countries:
        print(f"  📥 Fetching from {country}...")
        videos = fetch_videos(country)
        sleep(1)
        for item in videos:
            try:
                views = int(item["statistics"]["viewCount"])
            except:
                views = 0
            if views >= 1_000_000_000:
                views_str = f"{views/1_000_000_000:.2f}B"
            elif views >= 1_000_000:
                views_str = f"{views/1_000_000:.2f}M"
            else:
                views_str = str(views)

            video = {
                "title": item["snippet"]["title"],
                "views": views,
                "views_str": views_str,
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
            }
            all_videos.append(video)

    # Sıralama ve ilk 50’yi alma
    all_videos = sorted(all_videos, key=lambda x: x["views"], reverse=True)[:50]

    # JSON dosyaları
    with open(f"videos_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(all_videos, f, ensure_ascii=False, indent=2)

    structured_data = [generate_video_object(v) for v in all_videos]
    with open(f"structured_data_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Kaydedildi: videos_{continent}.json & structured_data_{continent}.json")

    # HTML’e gömme işlemi
    html_file = f"{continent}.html"
    if os.path.exists(html_file):
        with open(f"structured_data_{continent}.json", "r", encoding="utf-8") as json_file:
            json_ld = json_file.read()

        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        if "<!-- STRUCTURED_DATA_HERE -->" in html_content:
            html_content = html_content.replace(
                "<!-- STRUCTURED_DATA_HERE -->",
                f'<script type="application/ld+json">\n{json_ld}\n</script>'
            )
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✅ Structured data eklendi: {html_file}")
        else:
            print(f"⚠️ Etiket bulunamadı: {html_file}")
    else:
        print(f"❌ {html_file} dosyası bulunamadı.")
