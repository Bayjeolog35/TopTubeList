import os
import json
import requests
from bs4 import BeautifulSoup
from country_data import COUNTRY_INFO

# YouTube Data API Key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YouTube API key bulunamadı!")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"

def format_number(num):
    """Sayıları daha okunabilir hale getirir (1.5M, 150K gibi)"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def get_trending_videos(region_code, max_results=50):
    """YouTube'dan trend videoları çeker"""
    url = f"{YOUTUBE_API_BASE_URL}videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def process_video_data(item):
    """Ham video verisini işler"""
    snippet = item["snippet"]
    stats = item.get("statistics", {})
    
    return {
        "id": item["id"],
        "title": snippet.get("title", "Başlık Yok"),
        "channel": snippet.get("channelTitle", "Kanal Yok"),
        "thumbnail": snippet["thumbnails"]["high"]["url"] if "thumbnails" in snippet else "",
        "url": f"https://youtube.com/watch?v={item['id']}",
        "embed_url": f"https://youtube.com/embed/{item['id']}",
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
        "views_str": format_number(int(stats.get("viewCount", 0))),
        "likes_str": format_number(int(stats.get("likeCount", 0)))
    }

def update_html_file(country_folder, videos):
    """HTML dosyasını günceller"""
    html_path = os.path.join(country_folder, "index.html")
    
    if not os.path.exists(html_path):
        print(f"⚠️ {country_folder} için HTML dosyası bulunamadı!")
        return
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # En çok izlenen video için iframe ekle
        if videos:
            top_video = max(videos, key=lambda x: x["views"])
            
            # Eski iframe'i temizle
            for iframe in soup.find_all('iframe'):
                iframe.decompose()
            
            # Yeni iframe ekle
            iframe = soup.new_tag('iframe',
                                src=top_video["embed_url"],
                                width="560",
                                height="315",
                                frameborder="0",
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                                allowfullscreen="")
            
            # Uygun bir yere ekle (örneğin <div id="top-video">)
            container = soup.find('div', id='top-video') or soup.new_tag('div', id='top-video')
            container.append(iframe)
            if not soup.find('div', id='top-video'):
                soup.body.insert(0, container)
        
        # Değişiklikleri kaydet
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"✅ {country_folder} HTML'si güncellendi")
    
    except Exception as e:
        print(f"❌ {country_folder} HTML güncelleme hatası: {str(e)}")

def save_video_data(country_name, videos):
    """Video verilerini JSON olarak kaydeder"""
    os.makedirs("Country_data/videos", exist_ok=True)
    file_path = f"Country_data/videos/videos_{country_name}.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    print(f"📁 {country_name} video verileri kaydedildi")

def main():
    for country_folder, info in COUNTRY_INFO.items():
        country_code = info["code"]
        print(f"\n🔍 {country_folder} işleniyor...")
        
        try:
            # YouTube'dan veri çek
            data = get_trending_videos(country_code)
            videos = [process_video_data(item) for item in data.get("items", [])]
            
            if not videos:
                print("⚠️ Hiç video bulunamadı!")
                continue
            
            # Verileri kaydet
            save_video_data(country_folder, videos)
            
            # HTML'yi güncelle
            update_html_file(country_folder, videos)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ YouTube API hatası: {str(e)}")
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {str(e)}")

if __name__ == "__main__":
    main()
