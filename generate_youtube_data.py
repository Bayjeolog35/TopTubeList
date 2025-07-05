import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# API Key ayarı
if os.getenv("CI"):
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
else:
    load_dotenv()
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("API key bulunamadı!")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"
OUTPUT_DIR = "countries_html"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_number(num):
    num = float(num)
    for unit in ['', 'K', 'M', 'B']:
        if abs(num) < 1000:
            return f"{num:.1f}{unit}" if num % 1 else f"{int(num)}{unit}"
        num /= 1000
    return f"{num:.1f}B"

def get_trending_videos(region_code, max_results=50):
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(f"{YOUTUBE_API_BASE_URL}videos", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Hatası: {e}")
        return None

def process_video_data(item):
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    published_at_str = snippet.get("publishedAt", "")
    try:
        dt = datetime.fromisoformat(published_at_str.replace("Z", "+00:00"))
        formatted_date = dt.strftime("%d.%m.%Y")
    except Exception:
        formatted_date = "Tarih Yok"
    return {
        "id": item["id"],
        "title": snippet.get("title", "Başlık Yok"),
        "channel": snippet.get("channelTitle", "Kanal Yok"),
        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        "url": f"https://youtube.com/watch?v={item['id']}",
        "embed_url": f"https://youtube.com/embed/{item['id']}",
        "views": int(stats.get("viewCount", 0)),
        "views_formatted": format_number(int(stats.get("viewCount", 0))),
        "likes": int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
        "comments": int(stats.get("commentCount", 0)) if stats.get("commentCount") else 0,
        "published_at": published_at_str,
        "published_date_formatted": formatted_date
    }

def generate_structured_data(videos):
    return [{
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": v["title"],
        "description": v["title"],
        "thumbnailUrl": v["thumbnail"],
        "uploadDate": v["published_at"],
        "embedUrl": v["embed_url"],
        "url": v["url"],
        "interactionStatistic": {
            "@type": "InteractionCounter",
            "interactionType": {"@type": "WatchAction"},
            "userInteractionCount": v["views"]
        }
    } for v in videos]

def save_json(name, videos):
    with open(os.path.join(OUTPUT_DIR, f"{name}.vid.data.json"), 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTPUT_DIR, f"{name}.str.data.json"), 'w', encoding='utf-8') as f:
        json.dump(generate_structured_data(videos), f, ensure_ascii=False, indent=2)

def main():
    from country_info import COUNTRY_INFO

from collections import defaultdict
CONTINENT_GROUPS = defaultdict(list)
for country_name, info in COUNTRY_INFO.items():
    continent = info.get("continent")
    if continent:
        CONTINENT_GROUPS[continent].append(country_name)  # ayrı bir dosyadan çağıracağız
    videos_by_country = {}

    # Ülke verilerini çek
    for country, info in COUNTRY_INFO.items():
        code = info["code"]
        print(f"İşleniyor: {country} ({code})")
        data = get_trending_videos(code)
        if not data or 'items' not in data:
            print(f"Veri yok: {country}")
            continue
        videos = [process_video_data(item) for item in data["items"]]
        videos_by_country[country] = videos
        save_json(country, videos)

    # Kıta verilerini oluştur
    for continent, countries in CONTINENT_GROUPS.items():
        continent_videos = []
        for c in countries:
            continent_videos.extend(videos_by_country.get(c, []))
        continent_videos.sort(key=lambda x: x["views"], reverse=True)
        save_json(continent, continent_videos[:50])

    # Dünya geneli verisi (tüm ülkelerin birleşimi)
    all_videos = []
    for vids in videos_by_country.values():
        all_videos.extend(vids)
    all_videos.sort(key=lambda x: x["views"], reverse=True)
    save_json("worldwide", all_videos[:50])

if __name__ == "__main__":
    main()
