import requests
import json
from datetime import datetime

API_KEY = "AIzaSyDeEp8zM0PaRG26QlWmACmIkMZVJFu-QW8"
API_URL = "https://www.googleapis.com/youtube/v3/videos"
OUTPUT_JSON = "videos.json"
OUTPUT_STRUCTURED = "structured_data.json"
HTML_FILE = "index.html"
PLACEHOLDER_TAG = "<!-- STRUCTURED_DATA_HERE -->"

params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "maxResults": 50,
    "regionCode": "US",
    "key": API_KEY
}

response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data = response.json()
    videos = []
    structured_list = []

    for item in data["items"]:
        views_int = int(item["statistics"].get("viewCount", 0))
        views_str = f"{views_int / 1_000_000_000:.2f}B" if views_int >= 1_000_000_000 else \
                    f"{views_int / 1_000_000:.2f}M" if views_int >= 1_000_000 else str(views_int)

        video = {
            "title": item["snippet"]["title"],
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        videos.append(video)

        structured_list.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": item["snippet"]["title"],
            "description": item["snippet"].get("description", ""),
            "thumbnailUrl": item["snippet"]["thumbnails"]["medium"]["url"],
            "uploadDate": item["snippet"]["publishedAt"],
            "contentUrl": f"https://www.youtube.com/watch?v={item['id']}",
            "embedUrl": f"https://www.youtube.com/embed/{item['id']}"
        })

    videos = sorted(videos, key=lambda x: x["views"], reverse=True)

    # Save videos.json
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    # Save structured_data.json
    with open(OUTPUT_STRUCTURED, "w", encoding="utf-8") as f:
        json.dump(structured_list, f, ensure_ascii=False, indent=2)

    # Update index.html with structured data
    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()

        script_block = f'<script type="application/ld+json">\n{json.dumps(structured_list, ensure_ascii=False, indent=2)}\n</script>'
        
        if PLACEHOLDER_TAG in html_content:
            html_content = html_content.replace(PLACEHOLDER_TAG, script_block)
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(html_content)
            print("✅ index.html updated with JSON-LD")
        else:
            print("⚠️ Placeholder not found in index.html")

    except FileNotFoundError:
        print("❌ index.html not found.")
    
    print("✅ Data fetch and files updated.")

else:
    print("❌ API error:", response.status_code)
