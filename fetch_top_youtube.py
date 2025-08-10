import requests
import json
import os
import re
from datetime import datetime

# 🔐 API Key
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("❌ API anahtarı bulunamadı.")

# 📁 Dosya yolları
OUTPUT_FILE = "index.videos.json"
STRUCTURED_DATA_FILE = "index.structured_data.json"
HISTORY_FILE = "index.history.view.json"
HTML_FILE = "index.html"

# 📌 Placeholder’lar
STRUCTURED_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*<!-- STRUCTURED_DATA_HERE -->(.*?)</script>',
    re.DOTALL
)
IFRAME_PATTERN = re.compile(
    r'<!-- IFRAME_VIDEO_HERE -->(.*?)<!-- IFRAME_VIDEO_HERE_END -->',
    re.DOTALL
)

# 📦 API Request
params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "maxResults": 50,
    "key": API_KEY
}

response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)

if response.status_code == 200:
    data = response.json()

    # 📚 Önceki history verisini yükle (güvenli)
    previous_history = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                previous_history = json.load(f)
                if not isinstance(previous_history, dict):
                    previous_history = {}
        except json.JSONDecodeError:
            print(f"⚠️ {HISTORY_FILE} bozuk, sıfırdan yazılacak.")
            previous_history = {}

    # --- Önce topla, sonra viewChange’e göre sırala ---
    video_list = []  # (video_dict, struct_dict) tuple’ları

    for index, item in enumerate(data.get("items", []), start=1):
        vid = item["id"]

        # views
        try:
            views_int = int(item["statistics"].get("viewCount", 0))
        except Exception:
            views_int = 0

        if views_int >= 1_000_000_000:
            views_str = f"{views_int/1_000_000_000:.2f}B"
        elif views_int >= 1_000_000:
            views_str = f"{views_int/1_000_000:.2f}M"
        else:
            views_str = str(views_int)

        # tarih
        published_at_iso = item["snippet"].get("publishedAt", "")
        if published_at_iso:
            try:
                published_date_formatted = datetime.fromisoformat(
                    published_at_iso.replace("Z", "+00:00")
                ).strftime("%d.%m.%Y")
            except Exception:
                published_date_formatted = "Tarih Yok"
        else:
            published_date_formatted = "Tarih Yok"

        # previous history
        prev = previous_history.get(vid, {})
        prev_views = int(prev.get("views", 0))
        prev_rank = int(prev.get("rank", index))

        view_change = views_int - prev_views
        trend = "rising" if view_change > 0 else "falling" if view_change < 0 else "stable"
        view_change_str = f"{view_change:+,}"

        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        video_url = f"https://www.youtube.com/watch?v={vid}"
        embed_url = f"https://www.youtube.com/embed/{vid}"

        # description fallback (boşsa, linkse ya da çok kısaysa)
        raw_desc = (item["snippet"].get("description") or "").strip().replace("\n", " ")
        if (not raw_desc) or raw_desc.lower().startswith("http") or len(raw_desc) < 10:
            cleaned_description = f"{title} by {channel}"
        else:
            cleaned_description = raw_desc[:200]

        video_dict = {
            "id": vid,
            "title": title,
            "channel": channel,
            "views": views_int,
            "views_str": views_str,
            "url": video_url,
            "embed_url": embed_url,
            "thumbnail": thumbnail,
            "published_at": published_at_iso,
            "published_date_formatted": published_date_formatted,
            # rank ve rankChange SIRALAMA SONRASINDA yazılacak
            "viewChange": view_change,
            "viewChange_str": view_change_str,
            "trend": trend,
        }

        struct_dict = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": title,
            "description": cleaned_description,
            "thumbnailUrl": [thumbnail],               # schema: Array olmalı
            "uploadDate": published_at_iso,
            "contentUrl": video_url,
            "embedUrl": embed_url,
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": {"@type": "WatchAction"},
                "userInteractionCount": views_int
            }
        }

        video_list.append((video_dict, struct_dict, prev_rank))

    # ❗ Son 3 saatteki izlenme artışına göre sırala (büyükten küçüğe)
    video_list.sort(key=lambda t: t[0]["viewChange"], reverse=True)

    # Sıralama SONRASI rank ve rankChange ata
    videos = []
    structured_items = []
    for new_idx, (v, s, prev_rank) in enumerate(video_list, start=1):
        rank_change = prev_rank - new_idx   # 5 -> 2 => +3 (yükselme = pozitif)
        v["rank"] = new_idx
        v["rankChange"] = rank_change
        v["rankChange_str"] = f"{rank_change:+d}"
        videos.append(v)
        structured_items.append(s)

    # 💾 JSON dosyaları kaydet
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    with open(STRUCTURED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_items, f, ensure_ascii=False, indent=2)

    # 🔁 Yeni history dosyasını yaz (dict {id: {views, rank}})
    new_history = {
        v["id"]: {"views": v["views"], "rank": v["rank"]}
        for v in videos
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)

    print("✅ JSON dosyaları ve history dosyası kaydedildi.")

    # 🧠 HTML güncelle
    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"⚠️ {HTML_FILE} bulunamadı, HTML güncellemesi atlandı.")
        html = None

    if html is not None:
        # Structured Data: placeholder’ı koruyarak içerik güncelle
        with open(STRUCTURED_DATA_FILE, "r", encoding="utf-8") as f:
            structured_json = f.read()
        structured_block = f'<script type="application/ld+json">\n<!-- STRUCTURED_DATA_HERE -->\n{structured_json}\n</script>'
        html = STRUCTURED_PATTERN.sub(structured_block, html)

        # 📌 Iframe: en çok artış alan ilk video (videos[0])
        if videos:
            top = videos[0]
            iframe_block = f'''<!-- IFRAME_VIDEO_HERE -->
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
<!-- IFRAME_VIDEO_HERE_END -->'''
            if IFRAME_PATTERN.search(html):
                html = IFRAME_PATTERN.sub(iframe_block, html)
            else:
                # placeholder yoksa body kapanışından önce ekle
                html = html.replace("</body>", f"{iframe_block}\n</body>")

        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)

        print("✅ index.html içine iframe ve structured data başarıyla güncellendi.")
else:
    print("❌ API Hatası:", response.status_code)
