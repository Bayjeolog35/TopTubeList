import requests
import json
import os
import re
from datetime import datetime
import sys

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_URL = "https://www.googleapis.com/youtube/v3/videos"
STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_VIDEO_HERE -->"
# Placeholder desenleri
STRUCTURED_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*<!-- STRUCTURED_DATA_HERE -->(.*?)</script>',
    re.DOTALL
)
IFRAME_PATTERN = re.compile(
    r'<!-- IFRAME_VIDEO_HERE -->(.*?)<!-- IFRAME_VIDEO_HERE_END -->',
    re.DOTALL
)

COUNTRY_INFO = {
    "afghanistan": {"code": "AF", "continent": "asia"},
    "albania": {"code": "AL", "continent": "europe"},
    "algeria": {"code": "DZ", "continent": "africa"}, # THIS IS THE FIX
    "andorra": {"code": "AD", "continent": "europe"},
    "angola": {"code": "AO", "continent": "africa"},
    "argentina": {"code": "AR", "continent": "south_america"},
    "armenia": {"code": "AM", "continent": "asia"},
    "australia": {"code": "AU", "continent": "oceania"},
    "austria": {"code": "AT", "continent": "europe"},
    "azerbaijan": {"code": "AZ", "continent": "asia"},
    "bahamas": {"code": "BS", "continent": "north_america"},
    "bahrain": {"code": "BH", "continent": "asia"},
    "bangladesh": {"code": "BD", "continent": "asia"},
    "barbados": {"code": "BB", "continent": "north_america"},
    "belarus": {"code": "BY", "continent": "europe"},
    "belgium": {"code": "BE", "continent": "europe"},
    "belize": {"code": "BZ", "continent": "north_america"},
    "benin": {"code": "BJ", "continent": "africa"},
    "bhutan": {"code": "BT", "continent": "asia"},
    "bolivia": {"code": "BO", "continent": "south_america"},
    "bosnia-and-herzegovina": {"code": "BA", "display-name": "bosnia and herzegovina", "continent": "europe"},
    "botswana": {"code": "BW", "continent": "africa"},
    "brazil": {"code": "BR", "continent": "south_america"},
    "brunei": {"code": "BN", "continent": "asia"},
    "bulgaria": {"code": "BG", "continent": "europe"},
    "burkina-faso": {"code": "BF", "display-name": "burkina faso", "continent": "africa"},
    "burundi": {"code": "BI", "continent": "africa"},
    "cabo-verde": {"code": "CV", "display-name": "cabo verde", "continent": "africa"},
    "cambodia": {"code": "KH", "continent": "asia"},
    "cameroon": {"code": "CM", "continent": "africa"},
    "canada": {"code": "CA", "continent": "north_america"},
    "central-african-republic": {"code": "CF", "display-name": "central african republic", "continent": "africa"},
    "chad": {"code": "TD", "continent": "africa"},
    "chile": {"code": "CL", "continent": "south_america"},
    "china": {"code": "CN", "continent": "asia"},
    "colombia": {"code": "CO", "continent": "south_america"},
    "comoros": {"code": "KM", "continent": "africa"},
    "congo-democratic-republicofthe": {"code": "CD", "display-name": "congo (democratic republic of the)", "continent": "africa"},
    "congo-republic-of-the": {"code": "CG", "display-name": "congo (republic of the)", "continent": "africa"},
    "costa-rica": {"code": "CR", "display-name": "costa rica", "continent": "north_america"},
    "cote-divoire": {"code": "CI", "display-name": "cote d'ivoire", "continent": "africa"},
    "croatia": {"code": "HR", "continent": "europe"},
    "cuba": {"code": "CU", "continent": "north_america"},
    "cyprus": {"code": "CY", "continent": "asia"},
    "czech-republic": {"code": "CZ", "display-name": "czech republic", "continent": "europe"},
    "denmark": {"code": "DK", "continent": "europe"},
    "djibouti": {"code": "DJ", "continent": "africa"},
    "dominica": {"code": "DM", "continent": "north_america"},
    "dominican-republic": {"code": "DO", "display-name": "dominican republic", "continent": "north_america"},
    "east-timor": {"code": "TL", "display-name": "east timor", "continent": "asia"},
    "ecuador": {"code": "EC", "continent": "south_america"},
    "egypt": {"code": "EG", "continent": "africa"},
    "el-salvador": {"code": "SV", "display-name": "el salvador", "continent": "north_america"},
    "equatorial-guinea": {"code": "GQ", "display-name": "equatorial guinea", "continent": "africa"},
    "eritrea": {"code": "ER", "continent": "africa"},
    "estonia": {"code": "EE", "continent": "europe"},
    "eswatini": {"code": "SZ", "continent": "africa"},
    "ethiopia": {"code": "ET", "continent": "africa"},
    "fiji": {"code": "FJ", "continent": "oceania"},
    "finland": {"code": "FI", "continent": "europe"},
    "france": {"code": "FR", "continent": "europe"},
    "gabon": {"code": "GA", "continent": "africa"},
    "gambia": {"code": "GM", "continent": "africa"},
    "georgia": {"code": "GE", "continent": "asia"},
    "germany": {"code": "DE", "continent": "europe"},
    "ghana": {"code": "GH", "continent": "africa"},
    "greece": {"code": "GR", "continent": "europe"},
    "grenada": {"code": "GD", "continent": "north_america"},
    "guatemala": {"code": "GT", "continent": "north_america"},
    "guinea": {"code": "GN", "continent": "africa"},
    "guinea-bissau": {"code": "GW", "display-name": "guinea-bissau", "continent": "africa"},
    "guyana": {"code": "GY", "continent": "south_america"},
    "haiti": {"code": "HT", "continent": "north_america"},
    "honduras": {"code": "HN", "continent": "north_america"},
    "hungary": {"code": "HU", "continent": "europe"},
    "iceland": {"code": "IS", "continent": "europe"},
    "india": {"code": "IN", "continent": "asia"},
    "indonesia": {"code": "ID", "continent": "asia"},
    "iran": {"code": "IR", "continent": "asia"},
    "iraq": {"code": "IQ", "continent": "asia"},
    "ireland": {"code": "IE", "continent": "europe"},
    "israel": {"code": "IL", "continent": "asia"},
    "italy": {"code": "IT", "continent": "europe"},
    "jamaica": {"code": "JM", "continent": "north_america"},
    "japan": {"code": "JP", "continent": "asia"},
    "jordan": {"code": "JO", "continent": "asia"},
    "kazakhstan": {"code": "KZ", "continent": "asia"},
    "kenya": {"code": "KE", "continent": "africa"},
    "kiribati": {"code": "KI", "continent": "oceania"},
    "korea-north": {"code": "KP", "display-name": "korea (north)", "continent": "asia"},
    "korea-south": {"code": "KR", "display-name": "korea (south)", "continent": "asia"},
    "kosovo": {"code": "XK", "display-name": "kosovo", "continent": "europe"},
    "kuwait": {"code": "KW", "continent": "asia"},
    "kyrgyzstan": {"code": "KG", "continent": "asia"},
    "laos": {"code": "LA", "continent": "asia"},
    "latvia": {"code": "LV", "continent": "europe"},
    "lebanon": {"code": "LB", "continent": "asia"},
    "lesotho": {"code": "LS", "continent": "africa"},
    "liberia": {"code": "LR", "continent": "africa"},
    "libya": {"code": "LY", "continent": "africa"},
    "liechtenstein": {"code": "LI", "continent": "europe"},
    "lithuania": {"code": "LT", "continent": "europe"},
    "luxembourg": {"code": "LU", "continent": "europe"},
    "madagascar": {"code": "MG", "continent": "africa"},
    "malawi": {"code": "MW", "continent": "africa"},
    "malaysia": {"code": "MY", "continent": "asia"},
    "maldives": {"code": "MV", "continent": "asia"},
    "mali": {"code": "ML", "continent": "africa"},
    "malta": {"code": "MT", "continent": "europe"},
    "marshall-islands": {"code": "MH", "display-name": "marshall islands", "continent": "oceania"},
    "mauritania": {"code": "MR", "continent": "africa"},
    "mauritius": {"code": "MU", "continent": "africa"},
    "mexico": {"code": "MX", "continent": "north_america"},
    "micronesia": {"code": "FM", "continent": "oceania"},
    "moldova": {"code": "MD", "continent": "europe"},
    "monaco": {"code": "MC", "continent": "europe"},
    "mongolia": {"code": "MN", "continent": "asia"},
    "montenegro": {"code": "ME", "continent": "europe"},
    "morocco": {"code": "MA", "continent": "africa"},
    "mozambique": {"code": "MZ", "continent": "africa"},
    "myanmar": {"code": "MM", "continent": "asia"},
    "namibia": {"code": "NA", "continent": "africa"},
    "nauru": {"code": "NR", "continent": "oceania"},
    "nepal": {"code": "NP", "continent": "asia"},
    "netherlands": {"code": "NL", "continent": "europe"},
    "new-zealand": {"code": "NZ", "display-name": "new zealand", "continent": "oceania"},
    "nicaragua": {"code": "NI", "continent": "north_america"},
    "niger": {"code": "NE", "continent": "africa"},
    "nigeria": {"code": "NG", "continent": "africa"},
    "north-macedonia": {"code": "MK", "display-name": "north macedonia", "continent": "europe"},
    "norway": {"code": "NO", "continent": "europe"},
    "oman": {"code": "OM", "continent": "asia"},
    "pakistan": {"code": "PK", "continent": "asia"},
    "palau": {"code": "PW", "continent": "oceania"},
    "palestine": {"code": "PS", "continent": "asia"},
    "panama": {"code": "PA", "continent": "north_america"},
    "papua-new-guinea": {"code": "PG", "display-name": "papua new guinea", "continent": "oceania"},
    "paraguay": {"code": "PY", "continent": "south_america"},
    "peru": {"code": "PE", "continent": "south_america"},
    "philippines": {"code": "PH", "continent": "asia"},
    "poland": {"code": "PL", "continent": "europe"},
    "portugal": {"code": "PT", "continent": "europe"},
    "qatar": {"code": "QA", "continent": "asia"},
    "romania": {"code": "RO", "continent": "europe"},
    "russia": {"code": "RU", "continent": "europe"},
    "rwanda": {"code": "RW", "continent": "africa"},
    "saint-kitts-and-nevis": {"code": "KN", "display-name": "saint kitts and nevis", "continent": "north_america"},
    "saint-lucia": {"code": "LC", "display-name": "saint lucia", "continent": "north_america"},
    "saint-vincent-and-the-grenadines": {"code": "VC", "display-name": "saint vincent and the grenadines", "continent": "north_america"},
    "samoa": {"code": "WS", "continent": "oceania"},
    "san-marino": {"code": "SM", "display-name": "san marino", "continent": "europe"},
    "sao-tome-and-principe": {"code": "ST", "display-name": "sao tome and principe", "continent": "africa"},
    "saudi-arabia": {"code": "SA", "display-name": "saudi arabia", "continent": "asia"},
    "senegal": {"code": "SN", "continent": "africa"},
    "serbia": {"code": "RS", "continent": "europe"},
    "seychelles": {"code": "SC", "continent": "africa"},
    "sierra-leone": {"code": "SL", "display-name": "sierra leone", "continent": "africa"},
    "singapore": {"code": "SG", "continent": "asia"},
    "slovakia": {"code": "SK", "continent": "europe"},
    "slovenia": {"code": "SI", "continent": "europe"},
    "solomon-islands": {"code": "SB", "display-name": "solomon islands", "continent": "oceania"},
    "somalia": {"code": "SO", "continent": "africa"},
    "south-africa": {"code": "ZA", "display-name": "south africa", "continent": "africa"},
    "south-sudan": {"code": "SS", "display-name": "south sudan", "continent": "africa"},
    "spain": {"code": "ES", "continent": "europe"},
    "sri-lanka": {"code": "LK", "display-name": "sri lanka", "continent": "asia"},
    "sudan": {"code": "SD", "continent": "africa"},
    "suriname": {"code": "SR", "continent": "south_america"},
    "sweden": {"code": "SE", "continent": "europe"},
    "switzerland": {"code": "CH", "continent": "europe"},
    "syria": {"code": "SY", "continent": "asia"},
    "taiwan": {"code": "TW", "continent": "asia"},
    "tajikistan": {"code": "TJ", "continent": "asia"},
    "tanzania": {"code": "TZ", "continent": "africa"},
    "thailand": {"code": "TH", "continent": "asia"},
    "togo": {"code": "TG", "continent": "africa"},
    "tonga": {"code": "TO", "continent": "oceania"},
    "trinidad-and-tobago": {"code": "TT", "display-name": "trinidad and tobago", "continent": "north_america"},
    "tunisia": {"code": "TN", "continent": "africa"},
    "turkey": {"code": "TR", "continent": "europe"},
    "turkmenistan": {"code": "TM", "continent": "asia"},
    "tuvalu": {"code": "TV", "continent": "oceania"},
    "uganda": {"code": "UG", "continent": "africa"},
    "ukraine": {"code": "UA", "continent": "europe"},
    "united-arab-emirates": {"code": "AE", "display-name": "united arab emirates", "continent": "asia"},
    "united-kingdom": {"code": "GB", "display-name": "united kingdom", "continent": "europe"},
    "united-states": {"code": "US", "display-name": "united states", "continent": "north_america"},
    "uruguay": {"code": "UY", "continent": "south_america"},
    "uzbekistan": {"code": "UZ", "continent": "asia"},
    "vanuatu": {"code": "VU", "continent": "oceania"},
    "vatican-city": {"code": "VA", "display-name": "vatican city", "continent": "europe"},
    "venezuela": {"code": "VE", "continent": "south_america"},
    "vietnam": {"code": "VN", "continent": "asia"},
    "yemen": {"code": "YE", "continent": "asia"},
    "zambia": {"code": "ZM", "continent": "africa"},
    "zimbabwe": {"code": "ZW", "continent": "africa"}
}

def safe_load_history(path):
    """history dosyasını güvenli oku; dict veya eski list formatını normalize et"""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Eski format: list of videos
        if isinstance(data, list):
            return {v.get("id"): {"views": v.get("views", 0), "rank": v.get("rank", 0)} for v in data if isinstance(v, dict)}
        # Yeni format: dict {id: {views, rank}}
        if isinstance(data, dict):
            return {k: {"views": int(v.get("views", 0)), "rank": int(v.get("rank", 0))} for k, v in data.items()}
    except Exception:
        pass
    return {}

def update_iframe(html_file_path, top_video):
    if not top_video:
        print(f"⚠️ {html_file_path} için iframe eklenmedi (video yok).")
        return

    iframe_code = f"""<!-- IFRAME_VIDEO_HERE -->
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
<!-- IFRAME_VIDEO_HERE_END -->"""

    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"⛔ HTML dosyası bulunamadı: {html_file_path}")
        return

    pattern = re.compile(r"<!-- IFRAME_VIDEO_HERE -->(.*?)<!-- IFRAME_VIDEO_HERE_END -->", re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(iframe_code, html)
    elif IFRAME_PLACEHOLDER in html:
        html = html.replace(IFRAME_PLACEHOLDER, iframe_code)
    else:
        html = html.replace("</body>", f"{iframe_code}\n</body>")

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Iframe güncellendi: {html_file_path}")

def update_html(slug):
    html_file = f"{slug}.html"
    struct_file = f"{slug}.str.data.json"
    videos_file = f"{slug}.vid.data.json"

    if not (os.path.exists(html_file) and os.path.exists(struct_file) and os.path.exists(videos_file)):
        print(f"⛔ {slug} için gerekli dosyalar eksik (HTML/STR/VID).")
        return

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        with open(struct_file, 'r', encoding='utf-8') as f:
            structured_data = json.load(f)
        with open(videos_file, 'r', encoding='utf-8') as f:
            videos = json.load(f)

        # Structured data bloğu (placeholder korunur)
        structured_json = json.dumps(structured_data, ensure_ascii=False, indent=2)
        structured_block = f'<script type="application/ld+json">\n<!-- STRUCTURED_DATA_HERE -->\n{structured_json}\n</script>'
        structured_pattern = re.compile(r'<script type="application/ld\+json">\s*<!-- STRUCTURED_DATA_HERE -->(.*?)</script>', re.DOTALL)
        if structured_pattern.search(html):
            html = structured_pattern.sub(structured_block, html)
        elif STRUCTURED_DATA_PLACEHOLDER in html:
            html = html.replace(STRUCTURED_DATA_PLACEHOLDER, structured_block)
        else:
            first_ld = re.compile(r'<script type="application/ld\+json">.*?</script>', re.DOTALL)
            if first_ld.search(html):
                html = first_ld.sub(structured_block, html, count=1)
            else:
                html = html.replace("</head>", f"{structured_block}\n</head>")

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)

        # 🔴 iFrame’i SON 3 SAATTE en çok artış alan video ile yaz
        top_video = videos[0] if videos else None
        update_iframe(html_file, top_video)

        print(f"✅ Güncellendi: {slug}.html")

    except Exception as e:
        print(f"❌ Hata ({slug}): {e}")

# =========================
# Ana işlem: TÜM ÜLKELER
# =========================
for slug, info in COUNTRY_INFO.items():
    code = info["code"]
    display_name = slug.replace("-", " ").title()

    print(f"\n🌍 {display_name} ({code}) için veri çekiliyor...")

    video_file = f"{slug}.vid.data.json"
    struct_file = f"{slug}.str.data.json"
    history_file = f"{slug}.history.view.json"

    # Eski history verisini yükle (normalize)
    old_history = safe_load_history(history_file)
    # id -> eski rank sözlüğü
    old_ranks = {vid: data.get("rank", 0) for vid, data in old_history.items()}

    # API isteği
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": code,
        "maxResults": 50,
        "key": API_KEY
    }

    try:
        response = requests.get(API_URL, params=params, timeout=30)
    except requests.RequestException as e:
        print(f"❌ API İsteği Hatası ({code}): {e}")
        # boş dosyalar yaz
        for p in (video_file, struct_file):
            with open(p, "w", encoding="utf-8") as f:
                json.dump([], f)
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({}, f)
        update_html(slug)
        continue

    if response.status_code != 200:
        print(f"❌ API Hatası ({code}): {response.status_code}")
        # boş dosyalar yaz
        for p in (video_file, struct_file):
            with open(p, "w", encoding="utf-8") as f:
                json.dump([], f)
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({}, f)
        update_html(slug)
        continue

    items = response.json().get("items", [])
    if not items:
        print(f"⚠️ {slug} için API'den veri gelmedi.")
        with open(video_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(struct_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({}, f)
        update_html(slug)
        continue

    # --- Videoları topla ---
    video_list = []  # (video_obj, struct_obj, old_rank)

    for idx, item in enumerate(items, start=1):
        video_id = item["id"]

        # Views
        try:
            views_int = int(item["statistics"].get("viewCount", 0))
        except Exception:
            views_int = 0

        if views_int >= 1_000_000_000:
            views_str = f"{views_int / 1_000_000_000:.1f}B views"
        elif views_int >= 1_000_000:
            views_str = f"{views_int / 1_000_000:.1f}M views"
        elif views_int >= 1_000:
            views_str = f"{views_int / 1_000:.1f}K views"
        else:
            views_str = f"{views_int} views"

        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        published_at = item["snippet"].get("publishedAt", "")
        # Tarih formatı
        try:
            formatted_date = datetime.fromisoformat(
                published_at.replace("Z", "+00:00")
            ).strftime("%d.%m.%Y") if published_at else "Tarih Yok"
        except Exception:
            formatted_date = "Tarih Yok"

        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        embed_url = f"https://www.youtube.com/embed/{video_id}"

        # --- View Change ---
        old_views = int(old_history.get(video_id, {}).get("views", 0))
        view_diff = views_int - old_views
        trend = "up" if view_diff > 0 else "down" if view_diff < 0 else "stable"
        view_change_str = f"{view_diff:+,}"

        # --- Structured description temizleme ---
        raw_description = (item["snippet"].get("description") or "").strip().replace("\n", " ")
        if (not raw_description) or raw_description.lower().startswith("http") or len(raw_description) < 10:
            cleaned_description = f"{title} by {channel}"
        else:
            cleaned_description = raw_description[:200]

        video_obj = {
            "id": video_id,
            "title": title,
            "channel": channel,
            "views": views_int,
            "views_str": views_str,
            "url": video_url,
            "embed_url": embed_url,
            "thumbnail": thumbnail,
            "published_at": published_at,
            "published_date_formatted": formatted_date,
            "viewChange": view_diff,
            "viewChange_str": view_change_str,
            "trend": trend
        }

        struct_obj = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": title,
            "description": cleaned_description,
            "thumbnailUrl": [thumbnail],
            "uploadDate": published_at,
            "contentUrl": video_url,
            "embedUrl": embed_url,
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": views_int
            }
        }

        prev_rank = int(old_history.get(video_id, {}).get("rank", idx))
        video_list.append((video_obj, struct_obj, prev_rank))

    # --- Son 3 saatteki izlenme artışına göre sırala ---
    video_list.sort(key=lambda t: t[0]["viewChange"], reverse=True)

    # --- Sıralama SONRASI rank ve rankChange'i güncelle ---
    videos = []
    structured = []
    for new_idx, (v, s, prev_rank) in enumerate(video_list, start=1):
        rank_change = prev_rank - new_idx   # 5 -> 2 = +3 (yükselme pozitif)
        v["rank"] = new_idx
        v["rankChange"] = rank_change
        v["rankChange_str"] = f"{rank_change:+d}"
        videos.append(v)
        structured.append(s)

    # --- Dosyaları kaydet ---
    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(struct_file, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    # --- Yeni history kaydı (dict formatı) ---
    new_history = {v["id"]: {"views": v["views"], "rank": v["rank"]} for v in videos}
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)

    # --- HTML Güncelle ---
    update_html(slug)

sys.exit(0)
