import os
import json
import requests
from datetime import datetime

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # API key ortam değişkeninden alınır

CONTINENT_COUNTRIES = {
    "asia": [
        {"slug": "india", "code": "IN"},
        {"slug": "indonesia", "code": "ID"},
        {"slug": "japan", "code": "JP"},
        {"slug": "pakistan", "code": "PK"},
        {"slug": "bangladesh", "code": "BD"}
    ],
    "europe": [
        {"slug": "united-kingdom", "code": "GB"},
        {"slug": "germany", "code": "DE"},
        {"slug": "france", "code": "FR"},
        {"slug": "italy", "code": "IT"},
        {"slug": "spain", "code": "ES"}
    ],
    "north-america": [
        {"slug": "united-states", "code": "US"},
        {"slug": "canada", "code": "CA"},
        {"slug": "mexico", "code": "MX"}
    ],
    "south-america": [
        {"slug": "brazil", "code": "BR"},
        {"slug": "argentina", "code": "AR"},
        {"slug": "colombia", "code": "CO"},
        {"slug": "chile", "code": "CL"}
    ],
    "africa": [
        {"slug": "nigeria", "code": "NG"},
        {"slug": "egypt", "code": "EG"},
        {"slug": "south-africa", "code": "ZA"},
        {"slug": "kenya", "code": "KE"}
    ],
    "oceania": [
        {"slug": "australia", "code": "AU"},
        {"slug": "new-zealand", "code": "NZ"}
    ]
}

STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_PLACEHOLDER -->"

def format_views(views):
    if views >= 1_000_000_000:
        return f"{views / 1_000_000_000:.1f}B views"
    elif views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M views"
    elif views >= 1_000:
        return f"{views / 1_000:.1f}K views"
    else:
        return f"{views} views"

def fetch_videos_for_country(code):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "regionCode": code,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API hatası [{code}]: {response.status_code}")
        return []

    items = response.json().get("items", [])
    videos = []

    for item in data["items"]:
    try:
        views_int = int(item["statistics"]["viewCount"])
    except:
        views_int = 0

    # ✅ KISALTMALI views_str formatı
    if views_int >= 1_000_000_000:
        views_str = f"{views_int / 1_000_000_000:.1f}B"
    elif views_int >= 1_000_000:
        views_str = f"{views_int / 1_000_000:.1f}M"
    elif views_int >= 1_000:
        views_str = f"{views_int / 1_000:.1f}K"
    else:
        views_str = str(views_int)

    video_url = f"https://www.youtube.com/watch?v={item['id']}"
    thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
    published_at = item["snippet"].get("publishedAt", "")

    try:
        formatted_date = datetime.fromisoformat(published_at.replace("Z", "+00:00")).strftime("%d.%m.%Y")
    except:
        formatted_date = "Tarih Yok"

    video = {
        "id": item["id"],
        "title": item["snippet"]["title"],
        "channel": item["snippet"]["channelTitle"],
        "views": views_int,
        "views_str": f"{views_str} views",  # 👈 örnek: "1.2M views"
        "url": video_url,
        "embed_url": f"https://www.youtube.com/embed/{item['id']}",
        "thumbnail": thumbnail,
        "published_at": published_at,
        "published_date_formatted": formatted_date
    }
    videos.append(video)

    structured = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": item["snippet"]["title"],
        "description": item["snippet"].get("description", ""),
        "thumbnailUrl": [thumbnail],
        "uploadDate": published_at,
        "contentUrl": video_url,
        "embedUrl": f"https://www.youtube.com/embed/{item['id']}",
        "interactionStatistic": {
            "@type": "InteractionCounter",
            "interactionType": {"@type": "WatchAction"},
            "userInteractionCount": views_int
        }
    }
    structured_items.append(structured)


def deduplicate_by_title(videos):
    seen = {}
    for v in videos:
        title = v["title"].strip().lower()
        if title not in seen or v["views"] > seen[title]["views"]:
            seen[title] = v
    return list(seen.values())

def update_html(continent, top_videos, structured_data):
    html_file = f"{continent}.html"
    if not os.path.exists(html_file):
        print(f"⚠️ {html_file} bulunamadı.")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    structured_block = f'<script type="application/ld+json">\n{json.dumps(structured_data, ensure_ascii=False, indent=2)}\n</script>'
    html = html.replace(STRUCTURED_DATA_PLACEHOLDER, structured_block)

    if top_videos:
        first = top_videos[0]
        iframe = f'''\n<iframe \n  width="560" \n  height="315" \n  src="{first['embed_url']}" \n  title="{first['title']}" \n  frameborder="0" \n  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" \n  allowfullscreen \n  style="position:absolute; width:1px; height:1px; left:-9999px;">\n</iframe>'''
        html = html.replace(IFRAME_PLACEHOLDER, iframe)
    else:
        html = html.replace(IFRAME_PLACEHOLDER, "")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {html_file} güncellendi.")

def process_all():
    for continent, countries in CONTINENT_COUNTRIES.items():
        print(f"\n🌍 {continent.upper()} işleniyor...")
        all_videos = []
        for country in countries:
            all_videos.extend(fetch_videos_for_country(country["code"]))

        deduped = deduplicate_by_title(all_videos)
        sorted_videos = sorted(deduped, key=lambda v: v["views"], reverse=True)[:50]

        with open(f"{continent}.vid.data.json", "w", encoding="utf-8") as f:
            json.dump(sorted_videos, f, ensure_ascii=False, indent=2)
        print(f"📦 {continent}.vid.data.json kaydedildi ({len(sorted_videos)} video).")

        structured = generate_structured_data(sorted_videos)
        with open(f"{continent}.str.data.json", "w", encoding="utf-8") as f:
            json.dump(structured, f, ensure_ascii=False, indent=2)
        print(f"📦 {continent}.str.data.json kaydedildi.")

        update_html(continent, sorted_videos, structured)

if __name__ == "__main__":
    process_all()
