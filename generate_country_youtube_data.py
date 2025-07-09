import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict
import re

try:
    from country_info import COUNTRY_INFO
except ImportError:
    raise ValueError("❌ country_info.py dosyası ya yok ya da COUNTRY_INFO tanımlı değil.")

# API Key
if os.getenv("CI"):
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
else:
    load_dotenv()
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("❌ YOUTUBE_API_KEY tanımlı değil!")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"
OUTPUT_DIR = "."


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
        print(f"❌ API Hatası: {e}")
        return None


def process_video_data(item):
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    published_at = snippet.get("publishedAt", "")
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        date_str = dt.strftime("%d.%m.%Y")
    except:
        date_str = "N/A"
    return {
        "id": item["id"],
        "title": snippet.get("title", ""),
        "channel": snippet.get("channelTitle", ""),
        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        "url": f"https://youtube.com/watch?v={item['id']}",
        "embed_url": f"https://youtube.com/embed/{item['id']}",
        "views": int(stats.get("viewCount", 0)),
        "views_formatted": format_number(int(stats.get("viewCount", 0))),
        "likes": int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
        "comments": int(stats.get("commentCount", 0)) if stats.get("commentCount") else 0,
        "published_at": published_at,
        "published_date_formatted": date_str
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


def update_html_with_embedded_data(name, videos):
    html_file = f"{name}.html" if name != "worldwide" else "index.html"
    if not os.path.exists(html_file):
        print(f"⚠️ HTML dosyası bulunamadı: {html_file}")
        return
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()

        json_data = json.dumps(videos, ensure_ascii=False, indent=4)

        pattern = re.compile(r"(window\.embeddedVideoData\s*=\s*)([\{\[].*?[\}\]])(\s*;\s*</script>)", re.DOTALL)

        if pattern.search(html):
            html = pattern.sub(r"\g<1>" + json_data + r"\g<3>", html)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✅ HTML güncellendi: {html_file}")
        else:
            print(f"⚠️ Gömülü veri bloğu bulunamadı: {html_file}")

    except Exception as e:
        print(f"❌ Hata oluştu ({html_file}): {e}")


def main():
    print("🎬 Ülke verileri güncelleniyor...\n")

    for country, info in COUNTRY_INFO.items():
        code = info["code"]
        print(f"📥 {country.upper()} ({code})")
        data = get_trending_videos(code)
        if not data or 'items' not in data:
            print(f"⚠️ Veri alınamadı: {country}")
            videos = []
        else:
            videos = [process_video_data(item) for item in data["items"]]
        
        save_json(country, videos)
        update_html_with_embedded_data(country, videos)

    print("\n🏁 Ülke verileri tamamlandı.")


if __name__ == "__main__":
    main()
