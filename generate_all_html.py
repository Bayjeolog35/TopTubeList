import os
import json
from bs4 import BeautifulSoup

TEMPLATE_FILE = "index.html"  # Şablon dosya
VIDEO_DATA_DIR = "countries_html"
OUTPUT_DIR = "countries_html"

def load_template():
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def load_video_data(name):
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.vid.data.json")
    if not os.path.exists(path):
        print(f"⛔ Video verisi yok: {name}")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_structured_data(name):
    path = os.path.join(VIDEO_DATA_DIR, f"{name}.str.data.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def update_html(template_html, videos, name):
    soup = BeautifulSoup(template_html, "html.parser")

    # <title>
    title_tag = soup.find("title")
    if title_tag:
        title_tag.string = f"Trending YouTube Videos in {name.replace('-', ' ').title()} | TopTubeList"

    # <h1>
    h1_tag = soup.find("h1")
    if h1_tag:
        h1_tag.string = f"Top Videos in {name.replace('-', ' ').title()}"

    # Video Listesi
    video_list_div = soup.find("div", id="videoList")
    if video_list_div:
        video_list_div.clear()

        if not videos:
            empty_div = soup.new_tag("div", **{"class": "no-data"})
            empty_div.string = "❌ Sorry, no video data available for this region."
            video_list_div.append(empty_div)
        else:
            for video in videos[:20]:
                card = soup.new_tag("div", **{"class": "video-card"})

                link = soup.new_tag("a", href=video["url"], target="_blank")
                thumbnail = soup.new_tag("img", src=video["thumbnail"], alt=video["title"])
                link.append(thumbnail)

                info = soup.new_tag("div", **{"class": "video-info"})
                title = soup.new_tag("h3")
                title.string = video["title"]
                channel = soup.new_tag("p")
                channel.string = f"Channel: {video['channel']}"
                date = soup.new_tag("p")
                date.string = f"Uploaded: {video['published_date_formatted']}"
                views = soup.new_tag("p")
                views.string = f"Views: {video['views_formatted']}"

                info.extend([title, channel, date, views])
                card.extend([link, info])
                video_list_div.append(card)

    # Structured Data (JSON-LD)
    structured = load_structured_data(name)
    if structured:
        script_tag = soup.new_tag("script", type="application/ld+json")
        script_tag.string = json.dumps(structured, ensure_ascii=False, indent=2)
        soup.head.append(script_tag)

    # En çok izlenen videoyu iframe olarak ekle (gizli)
    if videos:
        top_video = videos[0]
        video_id = top_video["url"].split("v=")[-1].split("&")[0]
        iframe_tag = soup.new_tag("iframe", width="0", height="0", style="display:none")
        iframe_tag["src"] = f"https://www.youtube.com/embed/{video_id}"
        iframe_tag["allow"] = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        iframe_tag["allowfullscreen"] = True
        soup.body.append(iframe_tag)

    return str(soup)

def main():
    template_html = load_template()

    json_files = [
        f for f in os.listdir(VIDEO_DATA_DIR)
        if f.endswith(".vid.data.json")
    ]

    for file in json_files:
        name = file.replace(".vid.data.json", "")
        videos = load_video_data(name)
        html_output = update_html(template_html, videos, name)

        # 👇 Kök dizine direkt yaz
        output_path = f"{name}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ {name}.html üretildi.")

        # 🌍 Worldwide için index.html olarak da yaz
        if name == "worldwide":
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html_output)
            print("🌍 index.html (worldwide) olarak güncellendi.")

if __name__ == "__main__":
    main()
