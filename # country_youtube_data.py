# country_youtube_data.py

import os
import json
import requests
from datetime import datetime
from country_data import COUNTRY_INFO # country_data.py dosyasından bilgileri import ediyoruz

# YouTube Data API Key'inizi buraya girin
# Ortam değişkeni olarak ayarlamanız daha güvenlidir: export YOUTUBE_API_KEY="YOUR_API_KEY"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY ortam değişkeni ayarlanmamış. Lütfen API anahtarınızı ayarlayın.")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"

def format_number(num):
    """Sayıyı okunabilir formatta döndürür (örn: 1.2M, 50K)."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

def get_trending_videos(region_code, max_results=20):
    """Belirtilen bölge kodu için trend videoları çeker."""
    url = f"{YOUTUBE_API_BASE_URL}videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status() # Hata durumunda HTTPError yükselt
    return response.json()

def process_video_data(item):
    """API yanıtından gerekli video bilgilerini çıkarır."""
    snippet = item["snippet"]
    statistics = item.get("statistics", {}) # İstatistikler her zaman olmayabilir
    
    title = snippet.get("title", "No Title")
    channel_title = snippet.get("channelTitle", "Unknown Channel")
    video_id = item["id"]
    thumbnail = snippet["thumbnails"]["high"]["url"] if "thumbnails" in snippet and "high" in snippet["thumbnails"] else ""
    upload_date = snippet.get("publishedAt", "")
    
    views = int(statistics.get("viewCount", 0))
    likes = int(statistics.get("likeCount", 0))
    comments = int(statistics.get("commentCount", 0))

    return {
        "id": video_id,
        "title": title,
        "channelTitle": channel_title,
        "thumbnail": thumbnail,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "uploadDate": upload_date,
        "views": views,
        "views_str": format_number(views),
        "likes": likes,
        "comments": comments
    }

def generate_structured_data(videos, country_name, country_code):
    """Yapılandırılmış veri (Schema.org) oluşturur."""
    if not videos:
        return {}

    # İlk 5 videoyu al
    top_videos = videos[:5]

    structured_data = {
        "@context": "http://schema.org",
        "@type": "WebPage",
        "name": f"Trending YouTube Videos in {country_name}",
        "description": f"Most popular YouTube videos currently trending in {country_name}.",
        "publisher": {
            "@type": "Organization",
            "name": "TopTubeList",
            "url": "https://toptubelist.com/" # Sitenizin ana URL'si
        },
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": []
        }
    }

    for i, video in enumerate(top_videos):
        structured_data["mainEntity"]["itemListElement"].append({
            "@type": "ListItem",
            "position": i + 1,
            "item": {
                "@type": "VideoObject",
                "name": video["title"],
                "description": f"Trending video from {video['channelTitle']} in {country_name}",
                "thumbnailUrl": video["thumbnail"],
                "uploadDate": video["uploadDate"],
                "embedUrl": f"https://www.youtube.com/embed/{video['id']}",
                "interactionStatistic": {
                    "@type": "InteractionCounter",
                    "interactionType": "http://schema.org/WatchAction",
                    "userInteractionCount": video["views"]
                },
                "url": video["url"]
            }
        })
    return structured_data

def main():
    # Çıkış klasörü: Country_data altına videos ve structured_data klasörleri
    base_output_dir = "Country_data"
    output_dir_videos = os.path.join(base_output_dir, "videos")
    output_dir_structured_data = os.path.join(base_output_dir, "structured_data")

    os.makedirs(output_dir_videos, exist_ok=True)
    os.makedirs(output_dir_structured_data, exist_ok=True)

    for country_folder_name, info in COUNTRY_INFO.items():
        country_code = info["code"]
        display_name = info.get("display_name", country_folder_name.replace('_', ' '))

        print(f"Fetching trending videos for {display_name} ({country_code})...")
        try:
            youtube_response = get_trending_videos(region_code=country_code)
            
            videos_data = [process_video_data(item) for item in youtube_response.get("items", [])]
            
            # JSON dosyalarını kaydet (Country_data/videos altına)
            videos_output_path = os.path.join(output_dir_videos, f"videos_{country_folder_name}.json")
            with open(videos_output_path, "w", encoding="utf-8") as f:
                json.dump(videos_data, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(videos_data)} videos to {videos_output_path}")

            # Yapılandırılmış veriyi oluştur ve kaydet (Country_data/structured_data altına)
            structured_data = generate_structured_data(videos_data, display_name, country_code)
            structured_data_output_path = os.path.join(output_dir_structured_data, f"structured_data_{country_folder_name}.json")
            with open(structured_data_output_path, "w", encoding="utf-8") as f:
                json.dump(structured_data, f, ensure_ascii=False, indent=2)
            print(f"Generated structured data to {structured_data_output_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {display_name} ({country_code}): {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {display_name} ({country_code}): {e}")

if __name__ == "__main__":
    main()
