import os
import json
import requests
from datetime import datetime
import re

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("❌ YOUTUBE_API_KEY ortam değişkeni eksik.")

# 🌍 Kıtalar ve örnek ülkeler (listeni genişletebilirsin)
CONTINENT_COUNTRIES = {
    "asia": [
        {"slug": "india", "code": "IN"},
        {"slug": "indonesia", "code": "ID"},
        {"slug": "japan", "code": "JP"},
        {"slug": "pakistan", "code": "PK"},
        {"slug": "bangladesh", "code": "BD"},
    ],
    "europe": [
        {"slug": "united-kingdom", "code": "GB"},
        {"slug": "germany", "code": "DE"},
        {"slug": "france", "code": "FR"},
        {"slug": "italy", "code": "IT"},
        {"slug": "spain", "code": "ES"},
    ],
    "north-america": [
        {"slug": "united-states", "code": "US"},
        {"slug": "canada", "code": "CA"},
        {"slug": "mexico", "code": "MX"},
    ],
    "south-america": [
        {"slug": "brazil", "code": "BR"},
        {"slug": "argentina", "code": "AR"},
        {"slug": "colombia", "code": "CO"},
        {"slug": "chile", "code": "CL"},
    ],
    "africa": [
        {"slug": "nigeria", "code": "NG"},
        {"slug": "egypt", "code": "EG"},
        {"slug": "south-africa", "code": "ZA"},
        {"slug": "kenya", "code": "KE"},
    ],
    "oceania": [
        {"slug": "australia", "code": "AU"},
        {"slug": "new-zealand", "code": "NZ"},
    ],
}

# HTML yer tutucuları / desenleri
STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_VIDEO_HERE -->"
STRUCTURED_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*<!-- STRUCTURED_DATA_HERE -->(.*?)</script>',
    re.DOTALL,
)
IFRAME_PATTERN = re.compile(
    r'<!-- IFRAME_VIDEO_HERE -->(.*?)<!-- IFRAME_VIDEO_HERE_END -->',
    re.DOTALL,
)

# -------------- yardımcılar --------------

def fetch_videos_for_country(code):
    """YouTube mostPopular’dan ülke için 50 video çek."""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": code,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY,
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code != 200:
            print(f"❌ API hatası [{code}]: {r.status_code}")
            return []
        items = r.json().get("items", [])
    except requests.RequestException as e:
        print(f"❌ API isteği hatası [{code}]: {e}")
        return []

    out = []
    for it in items:
        vid = it["id"]

        try:
            views_int = int(it["statistics"].get("viewCount", 0))
        except Exception:
            views_int = 0

        if views_int >= 1_000_000_000:
            views_str = f"{views_int/1_000_000_000:.1f}B views"
        elif views_int >= 1_000_000:
            views_str = f"{views_int/1_000_000:.1f}M views"
        elif views_int >= 1_000:
            views_str = f"{views_int/1_000:.1f}K views"
        else:
            views_str = f"{views_int} views"

        title = it["snippet"]["title"]
        channel = it["snippet"]["channelTitle"]
        thumb = it["snippet"]["thumbnails"]["medium"]["url"]
        published_at = it["snippet"].get("publishedAt", "")

        try:
            formatted_date = (
                datetime.fromisoformat(published_at.replace("Z", "+00:00")).strftime("%d.%m.%Y")
                if published_at else "Tarih Yok"
            )
        except Exception:
            formatted_date = "Tarih Yok"

        out.append({
            "id": vid,
            "title": title,
            "channel": channel,
            "views": views_int,
            "views_str": views_str,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "embed_url": f"https://www.youtube.com/embed/{vid}",
            "thumbnail": thumb,
            "published_at": published_at,
            "published_date_formatted": formatted_date,
        })
    return out

def deduplicate_by_title(videos):
    """Aynı başlıkları (title) eleyip en çok izleneni bırak."""
    seen = {}
    for v in videos:
        key = v["title"].strip().lower()
        if key not in seen or v["views"] > seen[key]["views"]:
            seen[key] = v
    return list(seen.values())

def safe_load_history(path):
    """Kıta history dosyasını güvenli ve normalize ederek yükle (dict formatına çevirir)."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Eski format (list) desteği:
        if isinstance(data, list):
            return {v.get("id"): {"views": v.get("views", 0), "rank": v.get("rank", 0)} for v in data if isinstance(v, dict)}
        if isinstance(data, dict):
            # {id: {views, rank}}
            return {k: {"views": int(v.get("views", 0)), "rank": int(v.get("rank", 0))} for k, v in data.items()}
    except Exception:
        pass
    return {}

def compute_viewchange_sort_and_rank(continent, videos):
    """Ülke mantığıyla aynı: viewChange’a göre sırala, sonra rank/rankChange hesapla ve history yaz."""
    history_file = f"{continent}.history.view.json"
    old = safe_load_history(history_file)

    # viewChange hesapla
    enriched = []
    for idx, v in enumerate(videos, start=1):
        vid = v["id"]
        old_views = int(old.get(vid, {}).get("views", 0))
        old_rank  = int(old.get(vid, {}).get("rank", idx))
        view_diff = v["views"] - old_views
        trend = "up" if view_diff > 0 else ("down" if view_diff < 0 else "stable")
        v2 = {
            **v,
            "viewChange": view_diff,
            "viewChange_str": f"{view_diff:+,}",
            "trend": trend,
            "_prev_rank": old_rank,  # geçici
        }
        enriched.append(v2)

    # Son 3 saat artışına göre sırala
    enriched.sort(key=lambda e: e["viewChange"], reverse=True)

    # Sıralama SONRASI rank ve rankChange
    final_videos = []
    for new_rank, v in enumerate(enriched, start=1):
        prev_rank = v.pop("_prev_rank", new_rank)
        rank_change = prev_rank - new_rank  # 5 -> 2 => +3
        v["rank"] = new_rank
        v["rankChange"] = rank_change
        v["rankChange_str"] = f"{rank_change:+d}"
        final_videos.append(v)

    # History yaz (dict formatında)
    new_history = {v["id"]: {"views": v["views"], "rank": v["rank"]} for v in final_videos}
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)

    return final_videos

def build_structured_from_sorted(videos):
    """Structured data’yı SIRALANMIŞ listeye göre üret (ülkelerdeki gibi)."""
    out = []
    for v in videos:
        # description fallback
        desc = (v.get("description") or "").strip()
        if not desc or desc.lower().startswith("http") or len(desc) < 10:
            desc = f"{v['title']} by {v['channel']}"
        out.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": v["title"],
            "description": desc[:200],
            "thumbnailUrl": [v["thumbnail"]],
            "uploadDate": v["published_at"],
            "contentUrl": v["url"],
            "embedUrl": v["embed_url"],
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": v["views"],
            },
        })
    return out

def update_html(continent, videos_sorted, structured_sorted):
    """HTML’de hem structured data hem de iframe’i güncelle (placeholder/desenleri koru)."""
    html_file = f"{continent}.html"
    if not os.path.exists(html_file):
        print(f"⚠️ {html_file} bulunamadı.")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Structured data bloğu (placeholder korumalı)
    structured_json = json.dumps(structured_sorted, ensure_ascii=False, indent=2)
    structured_block = f'<script type="application/ld+json">\n<!-- STRUCTURED_DATA_HERE -->\n{structured_json}\n</script>'

    if STRUCTURED_PATTERN.search(html):
        html = STRUCTURED_PATTERN.sub(structured_block, html, count=1)
    elif STRUCTURED_DATA_PLACEHOLDER in html:
        html = html.replace(STRUCTURED_DATA_PLACEHOLDER, structured_block)
    else:
        # ilk ld+json etiketini bulup onun yerine yaz; hiç yoksa </head> öncesi ekle
        first_ld = re.compile(r'<script type="application/ld\+json">.*?</script>', re.DOTALL)
        if first_ld.search(html):
            html = first_ld.sub(structured_block, html, count=1)
        else:
            html = html.replace("</head>", f"{structured_block}\n</head>")

    # Iframe: sadece ilk video (viewChange en yüksek)
    iframe_block = ""
    if videos_sorted:
        top = videos_sorted[0]
        iframe_block = f"""<!-- IFRAME_VIDEO_HERE -->
<iframe 
  width="560" 
  height="315" 
  src="{top['embed_url']}" 
  title="{top['title']}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>
<!-- IFRAME_VIDEO_HERE_END -->"""

        if IFRAME_PATTERN.search(html):
            html = IFRAME_PATTERN.sub(iframe_block, html, count=1)
        elif IFRAME_PLACEHOLDER in html:
            html = html.replace(IFRAME_PLACEHOLDER, iframe_block)
        else:
            # yoksa body kapanışından önce ekle
            html = html.replace("</body>", f"{iframe_block}\n</body>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {continent}.html güncellendi (structured + iframe).")

# -------------- ana işlem --------------

def process_all():
    for continent, countries in CONTINENT_COUNTRIES.items():
        print(f"\n🌍 {continent.upper()} işleniyor...")
        # 1) Ülkelerden videoları topla
        raw = []
        for c in countries:
            raw.extend(fetch_videos_for_country(c["code"]))

        # 2) Tekilleştir → (opsiyonel) 50 ile sınırla
        deduped = deduplicate_by_title(raw)

        # 3) History’e göre viewChange hesapla + viewChange’a göre sırala + rank/rankChange yaz
        videos_sorted = compute_viewchange_sort_and_rank(continent, deduped)[:50]

        # 4) Structured data’yı AYNI sıraya göre üret
        structured_sorted = build_structured_from_sorted(videos_sorted)

        # 5) JSON’ları kaydet
        with open(f"{continent}.vid.data.json", "w", encoding="utf-8") as f:
            json.dump(videos_sorted, f, ensure_ascii=False, indent=2)
        with open(f"{continent}.str.data.json", "w", encoding="utf-8") as f:
            json.dump(structured_sorted, f, ensure_ascii=False, indent=2)

        # 6) HTML’yi güncelle (placeholder/desen)
        update_html(continent, videos_sorted, structured_sorted)

if __name__ == "__main__":
    process_all()
