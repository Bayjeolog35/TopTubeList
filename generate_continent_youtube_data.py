import json
import os

# Kıta ve ülke eşleşmeleri (slug + ISO country code)
CONTINENT_COUNTRIES = {
    "asia": [
        {"slug": "india", "code": "IN"},
        {"slug": "indonesia", "code": "ID"},
        {"slug": "japan", "code": "JP"},
        {"slug": "pakistan", "code": "PK"},
        {"slug": "bangladesh", "code": "BD"}
    ],
    "europe": [
        {"slug": "united-kingdom", "code": "GB"},
        {"slug": "germany", "code": "DE"},
        {"slug": "france", "code": "FR"},
        {"slug": "italy", "code": "IT"},
        {"slug": "spain", "code": "ES"}
    ],
    "north-america": [
        {"slug": "united-states", "code": "US"},
        {"slug": "canada", "code": "CA"},
        {"slug": "mexico", "code": "MX"}
    ],
    "south-america": [
        {"slug": "brazil", "code": "BR"},
        {"slug": "argentina", "code": "AR"},
        {"slug": "colombia", "code": "CO"},
        {"slug": "chile", "code": "CL"}
    ],
    "africa": [
        {"slug": "nigeria", "code": "NG"},
        {"slug": "egypt", "code": "EG"},
        {"slug": "south-africa", "code": "ZA"},
        {"slug": "kenya", "code": "KE"}
    ],
    "oceania": [
        {"slug": "australia", "code": "AU"},
        {"slug": "new-zealand", "code": "NZ"}
    ]
}

STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_PLACEHOLDER -->"

def load_country_video_data(slug):
    path = f"{slug}.vid.data.json"
    if not os.path.exists(path):
        print(f"⛔ {path} bulunamadı, atlanıyor.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_structured_data(videos):
    structured = []
    for video in videos[:50]:
        obj = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": video.get("title", ""),
            "description": video.get("description", ""),
            "thumbnailUrl": [video.get("thumbnail_url", "")],
            "uploadDate": video.get("published_at", ""),
            "embedUrl": video.get("embed_url", ""),
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": { "@type": "WatchAction" },
                "userInteractionCount": video.get("views", 0)
            }
        }
        structured.append(obj)
    return structured

def update_html(continent, top_videos, structured_items):
    html_file = f"{continent}.html"
    if not os.path.exists(html_file):
        print(f"⚠️ {html_file} dosyası yok, atlanıyor.")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    structured_block = f'<script type="application/ld+json">\n{json.dumps(structured_items, ensure_ascii=False, indent=2)}\n</script>'
    html = html.replace(STRUCTURED_DATA_PLACEHOLDER, structured_block)

    if top_videos:
        video = top_videos[0]
        iframe = f'''
<iframe 
  width="560" 
  height="315" 
  src="{video['embed_url']}" 
  title="{video['title']}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>'''
        html = html.replace(IFRAME_PLACEHOLDER, iframe)
    else:
        html = html.replace(IFRAME_PLACEHOLDER, "")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {html_file} güncellendi.")

def process_all():
    for continent, countries in CONTINENT_COUNTRIES.items():
        all_videos = []

        for country in countries:
            videos = load_country_video_data(country["slug"])
            all_videos.extend(videos)

        top_videos = sorted(all_videos, key=lambda x: x.get("views", 0), reverse=True)[:50]

        # Video JSON yaz
        with open(f"{continent}.vid.data.json", "w", encoding="utf-8") as f:
            json.dump(top_videos, f, ensure_ascii=False, indent=2)
        print(f"✅ {continent}.vid.data.json oluşturuldu.")

        # Structured JSON yaz
        structured = generate_structured_data(top_videos)
        with open(f"{continent}.str.data.json", "w", encoding="utf-8") as f:
            json.dump(structured, f, ensure_ascii=False, indent=2)
        print(f"✅ {continent}.str.data.json oluşturuldu.")

        # HTML güncelle
        update_html(continent, top_videos, structured)

if __name__ == "__main__":
    process_all()
