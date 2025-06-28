import requests
import json

API_KEY = "YOUR_API_KEY"
API_URL = "https://www.googleapis.com/youtube/v3/videos"
OUTPUT_FILE = "videos.json"
STRUCTURED_DATA_FILE = "structured_data.json"

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
    structured_data = []

    for item in data["items"]:
        try:
            views_int = int(item["statistics"]["viewCount"])
        except:
            views_int = 0
        views_str = f"{views_int/1_000_000_000:.2f}B" if views_int >= 1_000_000_000 else (
            f"{views_int/1_000_000:.2f}M" if views_int >= 1_000_000 else str(views_int)
        )

        video = {
            "title": item["snippet"]["title"],
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        videos.append(video)

        structured_data.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": item["snippet"]["title"],
            "description": item["snippet"]["description"][:300],
            "thumbnailUrl": item["snippet"]["thumbnails"]["medium"]["url"],
            "uploadDate": item["snippet"]["publishedAt"],
            "contentUrl": f"https://www.youtube.com/watch?v={item['id']}",
            "embedUrl": f"https://www.youtube.com/embed/{item['id']}"
        })

    videos = sorted(videos, key=lambda x: x["views"], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    # ✅ HTML'e gömme
    structured_data_script = f'<script type="application/ld+json">\n{json.dumps(structured_data, ensure_ascii=False, indent=2)}\n</script>'
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    html_content = html_content.replace("<!-- STRUCTURED_DATA_HERE -->", structured_data_script)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ videos.json, structured_data.json ve index.html güncellendi.")

else:
    print("❌ Hata:", response.status_code)
