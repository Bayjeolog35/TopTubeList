import requests
import json

API_KEY = "AIzaSyDeEp8zM0PaRG26QlWmACmIkMZVJFu-QW8"
API_URL = "https://www.googleapis.com/youtube/v3/videos"
OUTPUT_FILE = "videos.json"

params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "maxResults": 50,
    "regionCode": "US",  # İstersen "TR" veya başka bir ülke kodu kullanabilirsin.
    "key": API_KEY
}

response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data = response.json()
    videos = []
    for item in data["items"]:
        try:
            views_int = int(item["statistics"]["viewCount"])
        except:
            views_int = 0
        # Görsel format: Milyon için "xx.xxM", milyar için "xx.xxB"
        if views_int >= 1_000_000_000:
            views_str = f"{views_int/1_000_000_000:.2f}B"
        elif views_int >= 1_000_000:
            views_str = f"{views_int/1_000_000:.2f}M"
        else:
            views_str = str(views_int)
        
        video = {
            "title": item["snippet"]["title"],
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        videos.append(video)
    
    # Descending sırayla (en çok izlenen en üstte)
    videos = sorted(videos, key=lambda x: x["views"], reverse=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    print("✅ videos.json updated.")
else:
    print("❌ Hata:", response.status_code)
