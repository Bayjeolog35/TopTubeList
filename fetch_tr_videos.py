import requests
import json
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")  # Ortam değişkeninden API anahtarını al


def fetch_trending_videos_tr():
    url = "https://www.googleapis.com/youtube/v3/videos"
   params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "regionCode": "TR",  # <-- düzeltildi
    "maxResults": 50,
    "key": API_KEY

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API Hatası: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    items = data.get("items", [])
    if not items:
        print("⚠️ Hiç video bulunamadı.")
        return

    videos = []
    for item in items:
        try:
            views = int(item["statistics"].get("viewCount", 0))
        except:
            views = 0

        video = {
            "id": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": views
        }
        videos.append(video)

    # Büyükten küçüğe sırala
    videos = sorted(videos, key=lambda x: x["views"], reverse=True)

    # Kaydet
    with open("tr.vid.data.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    print("✅ tr.vid.data.json dosyası oluşturuldu.")

if __name__ == "__main__":
    fetch_trending_videos_tr()
