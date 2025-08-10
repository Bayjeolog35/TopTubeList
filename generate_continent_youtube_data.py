import os
import json
import requests
from datetime import datetime
import re

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 🌍 Kıta ve ülke listesi
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

# 📌 Placeholder tanımları
STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_VIDEO_HERE -->"

# 🔹 API'den video çek
def fetch_videos_for_country(code):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": code,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API hatası [{code}]: {response.status_code}")
        return []

    videos = []
    for item in response.json().get("items", []):
        try:
            views_int = int(item["statistics"]["viewCount"])
        except:
            views_int = 0

        if views_int >= 1_000_000_000:
            views_str = f"{views_int / 1_000_000_000:.1f}B"
        elif views_int >= 1_000_000:
            views_str = f"{views_int / 1_000_000:.1f}M"
        elif views_int >= 1_000:
            views_str = f"{views_int / 1_000:.1f}K"
        else:
            views_str = str(views_int)

        video_id = item["id"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        published_at = item["snippet"].get("publishedAt", "")
        try:
            formatted_date = datetime.fromisoformat(published_at.replace("Z", "+00:00")).strftime("%d.%m.%Y")
        except:
            formatted_date = "Tarih Yok"

        videos.append({
            "id": video_id,
            "title": title,
            "channel": channel,
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "embed_url": f"https://www.youtube.com/embed/{video_id}",
            "thumbnail": thumbnail,
            "published_at": published_at,
            "published_date_formatted": formatted_date
        })

    return videos

# 🔹 Aynı başlığa sahip tekrar eden videoları kaldır
def deduplicate_by_title(videos):
    seen = {}
    for v in videos:
        title = v["title"].strip().lower()
        if title not in seen or v["views"] > seen[title]["views"]:
            seen[title] = v
    return list(seen.values())

# 🔹 Structured data oluştur
def generate_structured_data(videos):
    structured = []
    for video in videos:
        structured.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": video["title"],
            "description": video.get("title", "")[:200],
            "thumbnailUrl": [video["thumbnail"]],
            "uploadDate": video["published_at"],
            "contentUrl": video["url"],
            "embedUrl": video["embed_url"],
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": video["views"]
            }
        })
    return structured

# 🔹 Sıra ve izlenme farkı hesapla
def calculate_rank_and_view_changes(continent, videos):
    history_file = f"{continent}.history.view.json"
    prev_data = {}
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            prev_data = {v["id"]: v for v in json.load(f)}

    for idx, video in enumerate(videos, start=1):
        prev_entry = prev_data.get(video["id"])

        if prev_entry:
            video["rankChange"] = prev_entry.get("rank", idx) - idx
            view_diff = video["views"] - prev_entry.get("views", video["views"])
            video["viewChange"] = view_diff
            video["viewChange_str"] = f"{'+' if view_diff > 0 else ''}{view_diff:,}" if view_diff else "-"
        else:
            video["rankChange"] = "-"
            video["viewChange"] = 0
            video["viewChange_str"] = "-"

        if video["viewChange"] > 0:
            video["trend"] = "rising"
        elif video["viewChange"] < 0:
            video["trend"] = "falling"
        else:
            video["trend"] = "stable"

        video["rank"] = idx

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    return videos

# 🔹 HTML güncelle
def update_html(continent, top_videos, structured_data):
    html_file = f"{continent}.html"
    if not os.path.exists(html_file):
        print(f"⚠️ {html_file} bulunamadı.")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    structured_block = f'<script type="application/ld+json">\n{STRUCTURED_DATA_PLACEHOLDER}\n{json.dumps(structured_data, ensure_ascii=False, indent=2)}\n</script>'
    structured_pattern = re.compile(
        r'<script type="application/ld\+json">\s*<!-- STRUCTURED_DATA_HERE -->(.*?)</script>',
        re.DOTALL
    )
    html = structured_pattern.sub(structured_block, html)

    if top_videos:
        first = top_videos[0]
        iframe_block = f"""<!-- IFRAME_VIDEO_HERE -->
<iframe width="560" height="315" src="{first['embed_url']}" title="{first['title']}" frameborder="0" allowfullscreen style="position:absolute; width:1px; height:1px; left:-9999px;"></iframe>
<!-- IFRAME_VIDEO_HERE_END -->"""
        iframe_pattern = re.compile(
            r'<!-- IFRAME_VIDEO_HERE -->(.*?)<!-- IFRAME_VIDEO_HERE_END -->',
            re.DOTALL
        )
        if iframe_pattern.search(html):
            html = iframe_pattern.sub(iframe_block, html)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {html_file} güncellendi.")

# 🔹 Tüm kıtaları işle
def process_all():
    for continent, countries in CONTINENT_COUNTRIES.items():
        print(f"\n🌍 {continent.upper()} işleniyor...")
        all_videos = []
        for country in countries:
            all_videos.extend(fetch_videos_for_country(country["code"]))

        deduped = deduplicate_by_title(all_videos)
        sorted_videos = sorted(deduped, key=lambda v: v["views"], reverse=True)[:50]
        sorted_videos = calculate_rank_and_view_changes(continent, sorted_videos)

        with open(f"{continent}.vid.data.json", "w", encoding="utf-8") as f:
            json.dump(sorted_videos, f, ensure_ascii=False, indent=2)

        structured = generate_structured_data(sorted_videos)
        with open(f"{continent}.str.data.json", "w", encoding="utf-8") as f:
            json.dump(structured, f, ensure_ascii=False, indent=2)

        update_html(continent, sorted_videos, structured)

if __name__ == "__main__":
    process_all()
