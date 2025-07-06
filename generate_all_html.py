import os
import json
from bs4 import BeautifulSoup

TEMPLATE_FILE = "base_index.html"  # Template dosyanız
VIDEO_DATA_DIR = "."              # Video JSON'larının bulunduğu dizin
OUTPUT_DIR = "."                  # Çıktı dizini (kök dizin)

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

def deduplicate_videos(video_list):
    seen_ids = set()
    unique = []
    for video in video_list:
        vid = video.get("videoId")
        if vid and vid not in seen_ids:
            seen_ids.add(vid)
            unique.append(video)
    return unique

def update_html(template_html, videos, name):
    print(f"🔍 {name} için {len(videos)} video yüklendi.")
    soup = BeautifulSoup(template_html, "html.parser")
    readable_name = name.replace("-", " ").title()

    # SEO ve başlık güncellemeleri
    title_tag = soup.find("title")
    if title_tag:
        title_tag.string = f"Trending YouTube Videos in {readable_name} | TopTubeList"

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        meta_desc["content"] = f"Watch the most popular YouTube videos trending across {readable_name}."

    # Video listesi oluşturma
      video_list_div = soup.find("div", id="videoList")
    if video_list_div:
        video_list_div.clear()
        for video in videos[:20]:
            card = soup.new_tag("div", **{"class": "video-card"})

            # Thumbnail
            thumbnail = soup.new_tag("img", src=video.get("thumbnail"), alt=video.get("title", ""), **{"class": "thumbnail"})
            card.append(thumbnail)

            # Title with link
            title = soup.new_tag("h3")
            # BURADAKİ SATIRI DEĞİŞTİRİN:
            link = soup.new_tag("a", href=f"https://www.youtube.com/watch?v={video.get('videoId')}", target="_blank", rel="noopener")
            link.string = video.get("title", "Untitled")
            title.append(link)
            card.append(title)

            # Channel name
            channel = soup.new_tag("p", **{"class": "channel-name"})
            channel.string = video.get("channelTitle", "")
            card.append(channel)

            # View count
            views = soup.new_tag("p", **{"class": "views"})
            views.string = video.get("viewCount", "") + " views"
            card.append(views)

            # Upload date
            date = soup.new_tag("p", **{"class": "upload-date"})
            date.string = video.get("publishedAt", "")[:10]
            card.append(date)

            # Add card to container
            video_list_div.append(card)

    return str(soup)


def main():
    template_html = load_template()

    for filename in os.listdir(VIDEO_DATA_DIR):
        if filename.endswith(".vid.data.json"):
            name = filename.replace(".vid.data.json", "")
            videos = load_video_data(name)
            html_content = update_html(template_html, videos, name)

            output_path = os.path.join(OUTPUT_DIR, f"{name}.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✅ {name}.html oluşturuldu.")


if __name__ == "__main__":
    main()
