import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime # Import datetime for date formatting

# GitHub Actions için özel ayar
if os.getenv('CI'):
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
else:
    # Local development için .env dosyasından oku
    from dotenv import load_dotenv
    load_dotenv()
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

if not YOUTUBE_API_KEY:
    raise ValueError("API key bulunamadı! GitHub Secrets'ta YOUTUBE_API_KEY tanımlayın.")

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"

def format_number(num):
    """Sayı formatlama: 1.5M, 150K gibi"""
    num = float(num) # Ensure num is a float for division
    for unit in ['', 'K', 'M', 'B']:
        if abs(num) < 1000:
            # Check if it's an integer or has decimal part for formatting
            if num == int(num):
                return f"{int(num)}{unit}"
            else:
                return f"{num:.1f}{unit}"
        num /= 1000
    return f"{num:.1f}B"

def get_trending_videos(region_code, max_results=50):
    """YouTube API'den trend videoları çek"""
    params = {
        "part": "snippet,statistics,contentDetails",
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
        print(f"API Hatası: {str(e)}")
        return None

def process_video_data(item):
    """Video verilerini işle"""
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    
    # Format published_at
    published_at_str = snippet.get("publishedAt", "")
    formatted_date = ""
    if published_at_str:
        try:
            # Parse ISO 8601 string
            dt_object = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
            formatted_date = dt_object.strftime("%d.%m.%Y")
        except ValueError:
            formatted_date = "Tarih Yok"

    return {
        "id": item["id"],
        "title": snippet.get("title", "Başlık Yok"),
        "channel": snippet.get("channelTitle", "Kanal Yok"),
        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        "url": f"https://youtube.com/watch?v={item['id']}",
        "embed_url": f"https://youtube.com/embed/{item['id']}",
        "views": int(stats.get("viewCount", 0)),
        "views_formatted": format_number(int(stats.get("viewCount", 0))), # Add formatted views
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
        "published_at": published_at_str,
        "published_date_formatted": formatted_date # Add formatted date
    }

def update_html_file(country_folder, videos):
    """GitHub Pages için HTML güncelleme"""
    html_path = os.path.join(country_folder, "index.html")
    
    # Ensure the directory exists
    os.makedirs(country_folder, exist_ok=True)

    # Check if the HTML file exists, if not, create a base one
    if not os.path.exists(html_path):
        print(f"{country_folder} için HTML bulunamadı, yeni oluşturuluyor...")
        base_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trend Videos - {country_folder.replace('_', ' ').title()}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .video-container {{ margin: 20px 0; }}
        iframe {{ max-width: 100%; }}
        .video-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .video-card {{ border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
        .video-card img {{ width: 100%; height: auto; display: block; }}
        .video-card-info {{ padding: 10px; }}
        .video-card-info h3 {{ margin-top: 0; font-size: 1.1em; }}
        .video-card-info p {{ margin: 5px 0; font-size: 0.9em; color: #555; }}
    </style>
</head>
<body>
    <h1>{country_folder.replace('_', ' ').title()} Trend Videolar</h1>
    <div id="top-video" class="video-container"></div>
    <div class="video-list"></div>
</body>
</html>
        """
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(base_html)
    
    with open(html_path, 'r+', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Top video container
        top_div = soup.find('div', id='top-video')
        if top_div and videos:
            top_video = max(videos, key=lambda x: x["views"])
            new_iframe = soup.new_tag('iframe',
                                       src=top_video["embed_url"],
                                       width="560",
                                       height="315",
                                       frameborder="0",
                                       allowfullscreen="")
            top_div.clear()
            top_div.append(new_iframe)
            
            # Video bilgileri
            info_div = soup.new_tag('div')
            title = soup.new_tag('h2')
            title.string = top_video["title"]
            channel = soup.new_tag('p')
            channel.string = f"Kanal: {top_video['channel']}"
            
            # Add Uploaded Date
            uploaded_date = soup.new_tag('p')
            uploaded_date.string = f"Yüklenme: {top_video['published_date_formatted']}"
            
            # Add Formatted Views
            views = soup.new_tag('p')
            views.string = f"İzlenme: {top_video['views_formatted']}"
            
            info_div.extend([title, channel, uploaded_date, views])
            top_div.append(info_div)
        
        # Video listesi
        video_list = soup.find('div', class_='video-list')
        if video_list:
            video_list.clear()
            for video in videos[:20]:  # İlk 20 video
                video_card = soup.new_tag('div', **{'class': 'video-card'})
                
                # Thumbnail ve bağlantı
                link = soup.new_tag('a', href=video["url"], target="_blank")
                img = soup.new_tag('img', src=video["thumbnail"], alt=video["title"])
                img['style'] = "width:100%; border-radius:8px;"
                link.append(img)
                
                # Bilgi div'i
                info_div_card = soup.new_tag('div', **{'class': 'video-card-info'})

                # Başlık
                title_card = soup.new_tag('h3')
                title_card.string = video["title"]
                
                # Yüklenme Tarihi
                uploaded_date_card = soup.new_tag('p')
                uploaded_date_card.string = f"Yüklenme: {video['published_date_formatted']}"
                
                # İzlenme Sayısı
                views_card = soup.new_tag('p')
                views_card.string = f"İzlenme: {video['views_formatted']}"
                
                info_div_card.extend([title_card, uploaded_date_card, views_card])
                
                video_card.extend([link, info_div_card])
                video_list.append(video_card)
        
        # Değişiklikleri kaydet
        f.seek(0)
        f.write(str(soup))
        f.truncate()

def main():
    # GitHub için gerekli klasörleri oluştur
    os.makedirs("Country_data/videos", exist_ok=True)
    
    # Define a list of country codes to process
    # You can expand this list as needed
    country_codes_to_process =  {
    
    "afghanistan": {"code": "af"},
    "albania": {"code": "al"},
    "algeria": {"code": "dz"},
    "andorra": {"code": "ad"},
    "angola": {"code": "ao"},
    "argentina": {"code": "ar"},
    "armenia": {"code": "am"},
    "australia": {"code": "au"},
    "austria": {"code": "at"},
    "azerbaijan": {"code": "az"},
    "bahamas": {"code": "bs"},
    "bahrain": {"code": "bh"},
    "bangladesh": {"code": "bd"},
    "barbados": {"code": "bb"},
    "belarus": {"code": "by"},
    "belgium": {"code": "be"},
    "belize": {"code": "bz"},
    "benin": {"code": "bj"},
    "bhutan": {"code": "bt"},
    "bolivia": {"code": "bo"},
    "bosnia-and-herzegovina": {"code": "ba", "display-name": "bosnia and herzegovina"},
    "botswana": {"code": "bw"},
    "brazil": {"code": "br"},
    "brunei": {"code": "bn"},
    "bulgaria": {"code": "bg"},
    "burkina-faso": {"code": "bf", "display-name": "burkina faso"},
    "burundi": {"code": "bı"},
    "cabo-verde": {"code": "cv", "display-name": "cabo verde"},
    "cambodia": {"code": "kh"},
    "cameroon": {"code": "cm"},
    "canada": {"code": "ca"},
    "central-african-republic": {"code": "cf", "display-name": "central african republic"},
    "chad": {"code": "td"},
    "chile": {"code": "cl"},
    "china": {"code": "cn"}, # youtube'da çin için doğrudan trend verisi kısıtlı olabilir
    "colombia": {"code": "co"},
    "comoros": {"code": "km"},
    "congo-democratic-republicofthe": {"code": "cd", "display-name": "congo (democratic republic of the)"},
    "congo-republic-of-the": {"code": "cg", "display-name": "congo (republic of the)"},
    "costa-rica": {"code": "cr", "display-name": "costa rica"},
    "cote-dıvoire": {"code": "cı", "display-name": "cote d'ıvoire"},
    "croatia": {"code": "hr"},
    "cuba": {"code": "cu"}, # youtube'da küba için doğrudan trend verisi kısıtlı olabilir
    "cyprus": {"code": "cy"},
    "czech-republic": {"code": "cz", "display-name": "czech republic"},
    "denmark": {"code": "dk"},
    "djibouti": {"code": "dj"},
    "dominica": {"code": "dm"},
    "dominican-republic": {"code": "do", "display-name": "dominican republic"},
    "east-timor": {"code": "tl", "display-name": "east timor"},
    "ecuador": {"code": "ec"},
    "egypt": {"code": "eg"},
    "elsalvador": {"code": "sv", "display-name": "el salvador"},
    "equatorial-guinea": {"code": "gq", "display-name": "equatorial guinea"},
    "eritrea": {"code": "er"},
    "estonia": {"code": "ee"},
    "eswatini": {"code": "sz"},
    "ethiopia": {"code": "et"},
    "fiji": {"code": "fj"},
    "finland": {"code": "fı"},
    "france": {"code": "fr"},
    "gabon": {"code": "ga"},
    "gambia": {"code": "gm"},
    "georgia": {"code": "ge"},
    "germany": {"code": "de"},
    "ghana": {"code": "gh"},
    "greece": {"code": "gr"},
    "grenada": {"code": "gd"},
    "guatemala": {"code": "gt"},
    "guinea": {"code": "gn"},
    "guinea-bissau": {"code": "gw", "display-name": "guinea-bissau"},
    "guyana": {"code": "gy"},
    "haiti": {"code": "ht"},
    "honduras": {"code": "hn"},
    "hungary": {"code": "hu"},
    "ıceland": {"code": "ıs"},
    "ındia": {"code": "ın"},
    "ındonesia": {"code": "ıd"},
    "ıran": {"code": "ır"}, # youtube'da iran için doğrudan trend verisi kısıtlı olabilir
    "ıraq": {"code": "ıq"},
    "ıreland": {"code": "ıe"},
    "ısrael": {"code": "ıl"},
    "ıtaly": {"code": "ıt"},
    "jamaica": {"code": "jm"},
    "japan": {"code": "jp"},
    "jordan": {"code": "jo"},
    "kazakhstan": {"code": "kz"},
    "kenya": {"code": "ke"},
    "kiribati": {"code": "kı"},
    "korea-north": {"code": "kp", "display-name": "korea (north)"}, # youtube'da kuzey kore için doğrudan trend verisi kısıtlı olabilir
    "korea-south": {"code": "kr", "display-name": "korea (south)"},
    "kosovo": {"code": "xk", "display-name": "kosovo"}, # ıso 3166-1 alpha-2 standardına dahil değil, dikkat
    "kuwait": {"code": "kw"},
    "kyrgyzstan": {"code": "kg"},
    "laos": {"code": "la"},
    "latvia": {"code": "lv"},
    "lebanon": {"code": "lb"},
    "lesotho": {"code": "ls"},
    "liberia": {"code": "lr"},
    "libya": {"code": "ly"},
    "liechtenstein": {"code": "lı"},
    "lithuania": {"code": "lt"},
    "luxembourg": {"code": "lu"},
    "madagascar": {"code": "mg"},
    "malawi": {"code": "mw"},
    "malaysia": {"code": "my"},
    "maldives": {"code": "mv"},
    "mali": {"code": "ml"},
    "malta": {"code": "mt"},
    "marshall-ıslands": {"code": "mh", "display-name": "marshall ıslands"},
    "mauritania": {"code": "mr"},
    "mauritius": {"code": "mu"},
    "mexico": {"code": "mx"},
    "micronesia": {"code": "fm"},
    "moldova": {"code": "md"},
    "monaco": {"code": "mc"},
    "mongolia": {"code": "mn"},
    "montenegro": {"code": "me"},
    "morocco": {"code": "ma"},
    "mozambique": {"code": "mz"},
    "myanmar": {"code": "mm"},
    "namibia": {"code": "na"},
    "nauru": {"code": "nr"},
    "nepal": {"code": "np"},
    "netherlands": {"code": "nl"},
    "new-zealand": {"code": "nz", "display-name": "new zealand"},
    "nicaragua": {"code": "nı"},
    "niger": {"code": "ne"},
    "nigeria": {"code": "ng"},
    "north-macedonia": {"code": "mk", "display-name": "north macedonia"},
    "norway": {"code": "no"},
    "oman": {"code": "om"},
    "pakistan": {"code": "pk"},
    "palau": {"code": "pw"},
    "palestine": {"code": "ps"},
    "panama": {"code": "pa"},
    "papua-new-guinea": {"code": "pg", "display-name": "papua new guinea"},
    "paraguay": {"code": "py"},
    "peru": {"code": "pe"},
    "philippines": {"code": "ph"},
    "poland": {"code": "pl"},
    "portugal": {"code": "pt"},
    "qatar": {"code": "qa"},
    "romania": {"code": "ro"},
    "russia": {"code": "ru"},
    "rwanda": {"code": "rw"},
    "saint-kitts-and-nevis": {"code": "kn", "display-name": "saint kitts and nevis"},
    "saint-lucia": {"code": "lc", "display-name": "saint lucia"},
    "saint-vincent-and-the-grenadines": {"code": "vc", "display-name": "saint vincent and the grenadines"},
    "samoa": {"code": "ws"},
    "san-marino": {"code": "sm", "display-name": "san marino"},
    "sao-tome-and-principe": {"code": "st", "display-name": "sao tome and principe"},
    "saudi-arabia": {"code": "sa", "display-name": "saudi arabia"},
    "senegal": {"code": "sn"},
    "serbia": {"code": "rs"},
    "seychelles": {"code": "sc"},
    "sierra-leone": {"code": "sl", "display-name": "sierra leone"},
    "singapore": {"code": "sg"},
    "slovakia": {"code": "sk"},
    "slovenia": {"code": "sı"},
    "solomon-ıslands": {"code": "sb", "display-name": "solomon ıslands"},
    "somalia": {"code": "so"},
    "south-africa": {"code": "za", "display-name": "south africa"},
    "south-sudan": {"code": "ss", "display-name": "south sudan"},
    "spain": {"code": "es"},
    "sri-lanka": {"code": "lk", "display-name": "sri lanka"},
    "sudan": {"code": "sd"},
    "suriname": {"code": "sr"},
    "sweden": {"code": "se"},
    "switzerland": {"code": "ch"},
    "syria": {"code": "sy"},
    "taiwan": {"code": "tw"},
    "tajikistan": {"code": "tj"},
    "tanzania": {"code": "tz"},
    "thailand": {"code": "th"},
    "togo": {"code": "tg"},
    "tonga": {"code": "to"},
    "trinidad-and-tobago": {"code": "tt", "display-name": "trinidad and tobago"},
    "tunisia": {"code": "tn"},
    "turkey": {"code": "tr"},
    "turkmenistan": {"code": "tm"},
    "tuvalu": {"code": "tv"},
    "uganda": {"code": "ug"},
    "ukraine": {"code": "ua"},
    "united-arab-emirates": {"code": "ae", "display-name": "united arab emirates"},
    "united-kingdom": {"code": "gb", "display-name": "united kingdom"},
    "united-states": {"code": "us", "display-name": "united states"},
    "uruguay": {"code": "uy"},
    "uzbekistan": {"code": "uz"},
    "vanuatu": {"code": "vu"},
    "vatican-city": {"code": "va", "display-name": "vatican city"},
    "venezuela": {"code": "ve"},
    "vietnam": {"code": "vn"},
    "yemen": {"code": "ye"},
    "zambia": {"code": "zm"},
    "zimbabwe": {"code": "zw"}
}

    for country_folder, country_code in country_codes_to_process.items():
        print(f"\nİşleniyor: {country_folder} ({country_code})")
        
        try:
            # YouTube verilerini al
            data = get_trending_videos(country_code)
            if not data or 'items' not in data:
                print("Veri alınamadı, atlanıyor...")
                continue
                
            videos = [process_video_data(item) for item in data['items']]
            
            # JSON olarak kaydet
            # Ensure the directory for JSON files exists
            json_output_dir = "Country_data/videos"
            os.makedirs(json_output_dir, exist_ok=True)
            with open(os.path.join(json_output_dir, f"videos_{country_folder}.json"), 'w', encoding='utf-8') as f:
                json.dump(videos, f, ensure_ascii=False, indent=2)
            
            # HTML'yi güncelle
            update_html_file(country_folder, videos)
            
        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            continue

if __name__ == "__main__":
    main()
