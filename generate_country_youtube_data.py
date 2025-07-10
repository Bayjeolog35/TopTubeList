import requests
import json
import os
from datetime import datetime
from country_info import COUNTRY_INFO  # country_info.py dosyasından COUNTRY_INFO'yu içe aktarıyoruz

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_URL = "https://www.googleapis.com/youtube/v3/videos"
IFRAME_PLACEHOLDER = ""
STRUCTURED_DATA_PLACEHOLDER = ""

# COUNTRY_INFO'dan ülke kodlarını ve isimlerini alıyoruz
country_data_for_processing = {}
for country_slug, info in COUNTRY_INFO.items():
    code = info["code"].upper()
    display_name_human_readable = info.get("display-name", country_slug.replace("-", " ")).title()
    
    country_data_for_processing[country_slug] = {
        "code": code,
        "display_name_human_readable": display_name_human_readable
    }

for country_slug, info in country_data_for_processing.items():
    code = info["code"]
    display_name_human_readable = info["display_name_human_readable"]
    
    print(f"'{display_name_human_readable}' ({code}) için veri çekiliyor...")

    OUTPUT_VIDEO_FILE = f"{country_slug}.vid.data.json"
    STRUCTURED_DATA_FILE = f"{country_slug}.str.data.json"
    HTML_OUTPUT_FILE = f"{country_slug}.html"

    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "maxResults": 50,
        "regionCode": code,
        "key": API_KEY
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        videos = []
        structured_items = []

        for item in data["items"]:
            try:
                views_int = int(item["statistics"].get("viewCount", 0))
            except (KeyError, ValueError):
                views_int = 0

            if views_int >= 1_000_000_000:
                views_str = f"{views_int / 1_000_000_000:.2f}B"
            elif views_int >= 1_000_000:
                views_str = f"{views_int / 1_000_000:.2f}M"
            elif views_int >= 1_000:
                views_str = f"{views_int / 1_000:.1f}K"
            else:
                views_str = str(views_int)

            video_id = item["id"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            thumbnail_url = item["snippet"]["thumbnails"]["medium"]["url"]
            published_at = item["snippet"]["publishedAt"]

            try:
                published_date_formatted = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")
            except ValueError:
                published_date_formatted = ""

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

            structured = {
                "@context": "https://schema.org",
                "@type": "VideoObject",
                "name": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnailUrl": thumbnail_url,
                "uploadDate": published_at,
                "contentUrl": video_url,
                "embedUrl": embed_url,
                "interactionStatistic": {
                    "@type": "InteractionCounter",
                    "interactionType": {"@type": "WatchAction"},
                    "userInteractionCount": views_int
                }
            }
            structured_items.append(structured)

        videos = sorted(videos, key=lambda x: x["views"], reverse=True)

        with open(OUTPUT_VIDEO_FILE, "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)

        with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(structured_items, f, ensure_ascii=False, indent=2)

        print(f"✅ {OUTPUT_VIDEO_FILE} ve {STRUCTURED_DATA_FILE} güncellendi.")

        if os.path.exists(HTML_OUTPUT_FILE):
            print(f"'{HTML_OUTPUT_FILE}' dosyası mevcut. Güncelleniyor...")
            with open(HTML_OUTPUT_FILE, "r", encoding="utf-8") as f:
                current_html_content = f.read()

            structured_script = f'<script type="application/ld+json">\n{json.dumps(structured_items, ensure_ascii=False, indent=2)}\n</script>'
            current_html_content = current_html_content.replace(STRUCTURED_DATA_PLACEHOLDER, structured_script)

            if videos:
                top_video = videos[0]
                iframe_html = f'''
<iframe 
  width="560" 
  height="315" 
  src="{top_video['embed_url']}" 
  title="{top_video['title']}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>
'''
                current_html_content = current_html_content.replace(IFRAME_PLACEHOLDER, iframe_html)
            else:
                current_html_content = current_html_content.replace(IFRAME_PLACEHOLDER, "")

            with open(HTML_OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(current_html_content)

            print(f"✅ {HTML_OUTPUT_FILE} içine structured data ve iframe eklendi.")
        else:
            print(f"⚠️ '{HTML_OUTPUT_FILE}' dosyası mevcut değil. HTML güncelleme atlanıyor.")

        print("-" * 50)

    else:
        print(f"❌ API Hatası ({code}):", response.status_code)
        if response.status_code == 403:
            print("API anahtarınızda kota sorunu veya geçersiz anahtar olabilir. Lütfen kontrol edin.")
        print("-" * 50)
