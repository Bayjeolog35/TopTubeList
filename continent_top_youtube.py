import json
import requests
from time import sleep

API_KEY = "AIzaSyDeEp8zM0PaRG26QlWmACmIkMZVJFu-QW8"
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

for continent, countries in continent_countries.items():
    all_videos = {}
    print(f"🌍 Processing {continent.upper()}...")
    for country in countries:
        print(f"  📥 Fetching from {country}...")
        videos = fetch_videos(country)
        for item in videos:
            video_id = item["id"]
            if video_id not in all_videos:
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
                all_videos[video_id] = {
                    "title": item["snippet"]["title"],
                    "views": views,
                    "views_str": views_str,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
                }
        sleep(1)  # API kotasını yormamak için
    sorted_videos = sorted(all_videos.values(), key=lambda x: x["views"], reverse=True)
    with open(f"videos_{continent}.json", "w", encoding="utf-8") as f:
        json.dump(sorted_videos[:50], f, ensure_ascii=False, indent=2)
    print(f"✅ Saved: videos_{continent}.json")
