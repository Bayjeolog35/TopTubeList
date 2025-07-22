import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict
import re # Yeni: Düzenli ifadeler için eklendi

# country_info.py dosyasından COUNTRY_INFO ve CONTINENT_INFO'yu içe aktardığınızı varsayıyorum
# Eğer ayrı bir dosya değillerse, bu değişkenlerin tanımlarını buraya eklemelisiniz.
try:
    from country_info import COUNTRY_INFO, CONTINENT_INFO
except ImportError:
    print("country_info.py dosyası bulunamadı veya COUNTRY_INFO/CONTINENT_INFO tanımlı değil.")
    print("Lütfen COUNTRY_INFO ve CONTINENT_INFO değişkenlerini bu betiğe ekleyin veya doğru yoldan import edin.")
    # Örnek boş tanımlar (kendi gerçek verilerinizle doldurun)
    # Bu kısmı kendi gerçek COUNTRY_INFO ve CONTINENT_INFO verinizle doldurmanız GEREKMEKTEDİR.
    COUNTRY_INFO = {
        "turkey": {"code": "TR", "name": "Turkey", "continent": "europe", "meta_description": "Trending YouTube videos in Turkey"},
        "united_states": {"code": "US", "name": "United States", "continent": "north_america", "meta_description": "Trending YouTube videos in United States"}
    }
    CONTINENT_INFO = {
        "europe": {"name": "Europe", "display_name": "Europe", "meta_description": "Trending YouTube videos in Europe"},
        "worldwide": {"display_name": "Worldwide", "meta_description": "Trending YouTube videos globally"}
    }


# API Key ayarı
if os.getenv("CI"):
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
else:
    load_dotenv()
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("API key bulunamadı!")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"
OUTPUT_DIR = "."  # HTML ve JSON'ların bulunduğu kök klasör

def format_number(num):
    num = float(num)
    for unit in ['', 'K', 'M', 'B']:
        if abs(num) < 1000:
            return f"{num:.1f}{unit}" if num % 1 else f"{int(num)}{unit}"
        num /= 1000
    return f"{num:.1f}B"

def get_trending_videos(region_code, max_results=50):
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(f"{YOUTUBE_API_BASE_URL}videos", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Hatası: {e}")
        return None

def process_video_data(item):
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    published_at_str = snippet.get("publishedAt", "")
    try:
        dt = datetime.fromisoformat(published_at_str.replace("Z", "+00:00"))
        formatted_date = dt.strftime("%d.%m.%Y")
    except Exception:
        formatted_date = "Tarih Yok"
    return {
        "id": item["id"],
        "title": snippet.get("title", "Başlık Yok"),
        "channel": snippet.get("channelTitle", "Kanal Yok"),
        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        "url": f"https://youtube.com/watch?v={item['id']}",
        "embed_url": f"https://youtube.com/embed/{item['id']}",
        "views": int(stats.get("viewCount", 0)),
        "views_formatted": format_number(int(stats.get("viewCount", 0))),
        "likes": int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
        "comments": int(stats.get("commentCount", 0)) if stats.get("commentCount") else 0,
        "published_at": published_at_str,
        "published_date_formatted": formatted_date
    }

def generate_structured_data(videos):
    structured = []
    for v in videos:
        try:
            iso_date = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00")).isoformat()
        except Exception:
            iso_date = "2025-01-01T00:00:00+00:00"  # fallback
        structured.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": v["title"],
            "description": v["title"] or "No description available",
            "thumbnailUrl": v["thumbnail"],
            "uploadDate": iso_date,
            "embedUrl": v["embed_url"],
            "url": v["url"],
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": v["views"]
            }
        })
    return structured


def save_json(name, videos):
    with open(os.path.join(OUTPUT_DIR, f"{name}.vid.data.json"), 'w', encoding='utf-8') as f:
       json.dump(videos, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTPUT_DIR, f"{name}.str.data.json"), 'w', encoding='utf-8') as f:
        json.dump(generate_structured_data(videos), f, ensure_ascii=False, indent=2)

def deduplicate(videos):
    seen = set()
    unique = []
    for v in videos:
        vid = v["id"]
        if vid not in seen:
            seen.add(vid)
            unique.append(v)
    return unique

def get_html_filename(name):
    """Ülke veya kıta adına göre HTML dosya adını döndürür."""
    if name == "worldwide":
        return "index.html"
    # Bu satırın kesinlikle bu şekilde olduğundan emin olun:
    return f"{name.lower().replace(' ', '-')}.html"

def update_html_with_embedded_data(name, videos_data):
    """
    Belirtilen HTML dosyasındaki gömülü video verilerini günceller.
    generate_all_html.py tarafından oluşturulan HTML'deki
    window.embeddedVideoData = [...]; veya {...}; yapısını bulur ve içeriğini değiştirir.
    """
    html_filename = get_html_filename(name)
    html_file_path = os.path.join(OUTPUT_DIR, html_filename)
    
    if not os.path.exists(html_file_path):
        print(f"Uyarı: '{html_file_path}' HTML dosyası bulunamadı. Lütfen önce generate_all_html.py'yi bir kez çalıştırın.")
        return

    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Yeni JSON verisini string'e dönüştür (okunabilirlik için indent kullanıldı)
        new_json_string = json.dumps(videos_data, ensure_ascii=False, indent=4)
        
        # Regex deseni:
        # (window\.embeddedVideoData\s*=\s*) : "window.embeddedVideoData =" kısmını yakalar (Grup 1)
        # ([\{\[].*?[\}\]]) : JSON objesini ({...}) veya dizisini ([...]) yakalar (Grup 2 - VERİ KISMI)
        # (\s*;\s*</script>) : JSON'dan sonraki noktalı virgül ve </script> etiketini yakalar (Grup 3)
        # re.DOTALL: '.' karakterinin yeni satırları da eşleştirmesini sağlar.
        pattern = re.compile(r"(window\.embeddedVideoData\s*=\s*)([\{\[].*?[\}\]])(\s*;\s*</script>)", re.DOTALL)

        if pattern.search(html_content):
            # Bulunan deseni, yakalanan grupları ve yeni JSON stringini kullanarak değiştir
            html_content = pattern.sub(r"\g<1>" + new_json_string + r"\g<3>", html_content)
            print(f"✅ HTML dosyası güncellendi: {html_file_path}")
        else:
            print(f"⚠️ '{html_file_path}' içinde 'window.embeddedVideoData = [veri];' bloğu bulunamadı. HTML yapısını kontrol edin.")
            # Eğer blok bulunamazsa, dosyanın üzerine yazmamak için buradan çıkarız.
            return 

        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    except Exception as e:
        print(f"❌ Hata: HTML dosyası güncellenirken sorun oluştu '{html_file_path}': {e}")


def main():
    print("#######################################")
    print("# TopTubeList - Veri Güncelleyici")
    print("# YouTube trend verileri çekiliyor ve HTML'lere gömülüyor...")
    print("#######################################\n")

    # Kıta gruplarını oluştur
    # COUNTRY_INFO'nun import edildiğinden veya tanımlandığından emin olun.
    CONTINENT_GROUPS = defaultdict(list)
    for country_name, info in COUNTRY_INFO.items():
        continent = info.get("continent")
        if continent:
            CONTINENT_GROUPS[continent].append(country_name)

    videos_by_country = {}

    # Ülke verilerini çek ve HTML'lere göm
    for country, info in COUNTRY_INFO.items():
        code = info["code"]
        print(f"➡️ İşleniyor: {country} ({code})")
        data = get_trending_videos(code)
        if not data or 'items' not in data:
            print(f"⚠️ Veri yok veya API hatası: {country}. Boş veri ile devam ediliyor.")
            videos = []
        else:
            videos = [process_video_data(item) for item in data["items"]]
            videos = deduplicate(videos)
        
        videos_by_country[country] = videos
        update_html_with_embedded_data(country, videos) # HTML'e göm
        save_json(country, videos)
    
    print("\n--- Kıta Verileri Güncelleniyor ---")
    # Kıtasal veriler
    for continent, country_list in CONTINENT_GROUPS.items():
        continent_videos = []
        for country in country_list:
            continent_videos.extend(videos_by_country.get(country, []))
        continent_videos = deduplicate(continent_videos)
        continent_videos.sort(key=lambda x: x["views"], reverse=True)
        update_html_with_embedded_data(continent, continent_videos[:50]) # HTML'e göm
        save_json(continent, continent_videos[:50])
        print(f"✅ Kıtasal veri güncellendi: {continent}")


    print("\n--- Dünya Geneli Verileri Güncelleniyor ---")
    # Dünya geneli
    all_videos = []
    for vids in videos_by_country.values():
        all_videos.extend(vids)
    all_videos = deduplicate(all_videos)
    all_videos.sort(key=lambda x: x["views"], reverse=True)
    update_html_with_embedded_data("worldwide", all_videos[:50]) # HTML'e göm (index.html'i de etkileyecek)
    print("✅ Dünya geneli veri güncellendi.")

    print("\n🏁 Tüm veri güncelleme işlemleri tamamlandı.")

if __name__ == "__main__":
    main()
