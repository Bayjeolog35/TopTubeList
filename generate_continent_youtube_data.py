import os
import json
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # .env dosyasından veya CI ortamından gelir

CONTINENT_COUNTRIES = {
    "asia": [{"slug": "india", "code": "IN"}, {"slug": "indonesia", "code": "ID"}, {"slug": "japan", "code": "JP"}, {"slug": "pakistan", "code": "PK"}, {"slug": "bangladesh", "code": "BD"}],
    "europe": [{"slug": "united-kingdom", "code": "GB"}, {"slug": "germany", "code": "DE"}, {"slug": "france", "code": "FR"}, {"slug": "italy", "code": "IT"}, {"slug": "spain", "code": "ES"}],
    "north-america": [{"slug": "united-states", "code": "US"}, {"slug": "canada", "code": "CA"}, {"slug": "mexico", "code": "MX"}],
    "south-america": [{"slug": "brazil", "code": "BR"}, {"slug": "argentina", "code": "AR"}, {"slug": "colombia", "code": "CO"}, {"slug": "chile", "code": "CL"}],
    "africa": [{"slug": "nigeria", "code": "NG"}, {"slug": "egypt", "code": "EG"}, {"slug": "south-africa", "code": "ZA"}, {"slug": "kenya", "code": "KE"}],
    "oceania": [{"slug": "australia", "code": "AU"}, {"slug": "new-zealand", "code": "NZ"}]
}

STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_PLACEHOLDER -->"

def fetch_videos_for_country(code):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "regionCode": code,
        "maxResults": 50,  # <-- burada 10'dan 50'ye yükselttik
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API hatası [{code}]: {response.status_code}")
        return []

    items = response.json().get("items", [])
    videos = []

    for item in items:
        video_id = item.get("id")
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})

        video = {
                "id": video_id,
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "views": views_int,
                "views_str": views_str,
                "url": video_url,
                "embed_url": embed_url,
                "thumbnail": thumbnail_url,
                "published_at": published_at,
                "published_date_formatted": published_date_formatted
            }
            videos.append(video)

    return videos

def generate_structured_data(videos):
    structured = []
    for video in videos:
        obj = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": video["title"],
            "description": video["description"],
            "thumbnailUrl": [video["thumbnail_url"]],
            "uploadDate": video["published_at"],
            "embedUrl": video["embed_url"],
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": video["views"]
            }
        }
        structured.append(obj)
    return structured

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
        iframe = f'''
<iframe 
  width="560" 
  height="315" 
  src="{first['embed_url']}" 
  title="{first['title']}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>'''
        html = html.replace(IFRAME_PLACEHOLDER, iframe)
    else:
        html = html.replace(IFRAME_PLACEHOLDER, "")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {html_file} güncellendi.")

def deduplicate_videos(videos):
    unique = {}
    for video in videos:
        vid = video["id"]
        if vid not in unique or video["views"] > unique[vid]["views"]:
            unique[vid] = video
    return list(unique.values())

def process_all():
    for continent, countries in CONTINENT_COUNTRIES.items():
        print(f"\n🌍 {continent.upper()} işleniyor...")
        all_videos = []
        for country in countries:
            country_videos = fetch_videos_for_country(country["code"])
            all_videos.extend(country_videos)

        deduped_videos = deduplicate_videos(all_videos)
        sorted_videos = sorted(deduped_videos, key=lambda x: x["views"], reverse=True)[:50]

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
