import json
import os
from datetime import datetime

# Kıtalar ve temsilci ülkeler
CONTINENT_COUNTRIES = {
    "asia": ["india", "indonesia", "japan", "pakistan", "bangladesh"],
    "europe": ["united-kingdom", "germany", "france", "italy", "spain"],
    "north-america": ["united-states", "canada", "mexico"],
    "south-america": ["brazil", "argentina", "colombia", "chile"],
    "africa": ["nigeria", "egypt", "south-africa", "kenya"],
    "oceania": ["australia", "new-zealand"]
}

STRUCTURED_DATA_PLACEHOLDER = "<!-- STRUCTURED_DATA_HERE -->"
IFRAME_PLACEHOLDER = "<!-- IFRAME_PLACEHOLDER -->"

def load_country_data(country_slug):
    video_path = f"{country_slug}.vid.data.json"
    struct_path = f"{country_slug}.str.data.json"
    if not os.path.exists(video_path) or not os.path.exists(struct_path):
        return [], []

    with open(video_path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    with open(struct_path, "r", encoding="utf-8") as f:
        structured = json.load(f)

    return videos, structured

def update_html(continent, top_videos, structured_items):
    html_file = f"{continent}.html"
    if not os.path.exists(html_file):
        print(f"⚠️ {html_file} dosyası yok, atlanıyor.")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    structured_script = f'<script type="application/ld+json">\n{json.dumps(structured_items, ensure_ascii=False, indent=2)}\n</script>'
    html_content = html_content.replace(STRUCTURED_DATA_PLACEHOLDER, structured_script)

    if top_videos:
        video = top_videos[0]
        iframe_html = f'''
<iframe 
  width="560" 
  height="315" 
  src="{video['embed_url']}" 
  title="{video['title']}" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen 
  style="position:absolute; width:1px; height:1px; left:-9999px;">
</iframe>
'''
        html_content = html_content.replace(IFRAME_PLACEHOLDER, iframe_html)
    else:
        html_content = html_content.replace(IFRAME_PLACEHOLDER, "")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ {html_file} dosyası güncellendi.")

def generate_continent_data():
    for continent, countries in CONTINENT_COUNTRIES.items():
        video_dict = {}
        structured_dict = {}

        for country in countries:
            vids, structs = load_country_data(country)

            for video in vids:
                video_id = video.get("id")
                if video_id and video_id not in video_dict:
                    video_dict[video_id] = video

            for structured in structs:
                # Her iki alanı kontrol et, hangisi varsa onu kullan
                unique_key = structured.get("embedUrl") or structured.get("contentUrl")
                if unique_key and unique_key not in structured_dict:
                    structured_dict[unique_key] = structured

        # En çok izlenen ilk 50 video
        top_videos = sorted(video_dict.values(), key=lambda x: x.get("views", 0), reverse=True)[:50]

        # Structured datayı sadece ilk 50 videoyla eşleşenlerden al
        top_video_ids = {v["id"] for v in top_videos}
        top_structured = []
        for s in structured_dict.values():
            url = s.get("contentUrl") or s.get("embedUrl", "")
            if any(vid_id in url for vid_id in top_video_ids):
                top_structured.append(s)
            if len(top_structured) >= 50:
                break

        # Dosyalara yaz
        with open(f"{continent}.vid.data.json", "w", encoding="utf-8") as f:
            json.dump(top_videos, f, ensure_ascii=False, indent=2)

        with open(f"{continent}.str.data.json", "w", encoding="utf-8") as f:
            json.dump(top_structured, f, ensure_ascii=False, indent=2)

        print(f"📦 {continent} için {len(top_videos)} video ve {len(top_structured)} structured data kaydedildi.")
        update_html(continent, top_videos, top_structured)

generate_continent_data()

