import os
import json

def generate_html_file(continent_name, videos_data, structured_data):
    """Kıta sayfası için HTML dosyası oluşturur."""

    sanitized_continent_name = continent_name.replace("_", "-")
    display_continent_name = continent_name.replace("-", " ").replace("_", " ").title()

    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2)
        structured_data_block = (
            '<script type="application/ld+json">\n' +
            structured_json +
            '\n</script>'
        )

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Trending YouTube Videos in {display_continent_name} | TopTubeList</title>
  <meta name="description" content="Most viewed YouTube videos in {display_continent_name}. Updated every 3 hours.">
  <link rel="stylesheet" href="/style.css" />
  {structured_data_block}
</head>
<body>
  <h1>Trending in {display_continent_name}</h1>
  <div id="videoList"></div>
  <script>
    fetch("/Country_data/videos/videos_{continent_name}.json")
      .then(res => res.json())
      .then(videos => {{
        const container = document.getElementById("videoList");
        videos.forEach(video => {{
          const div = document.createElement("div");
          div.innerHTML = `<h3><a href="${{video.url}}" target="_blank">${{video.title}}</a></h3>`;
          container.appendChild(div);
        }});
      }});
  </script>
</body>
</html>
"""

    output_dir = sanitized_continent_name
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ {output_path} oluşturuldu.")

def main():
    base_data_dir = "Country_data"
    videos_base_dir = os.path.join(base_data_dir, "videos")
    structured_data_base_dir = os.path.join(base_data_dir, "structured_data")

    continents = ["asia", "africa", "europe", "north_america", "south_america", "oceania"]

    for continent_name in continents:
        videos_file = os.path.join(videos_base_dir, f"videos_{continent_name}.json")
        structured_data_file = os.path.join(structured_data_base_dir, f"structured_data_{continent_name}.json")

        videos_data = []
        structured_data = {}

        if os.path.exists(videos_file):
            with open(videos_file, "r", encoding="utf-8") as f:
                videos_data = json.load(f)
        else:
            print(f"❌ {videos_file} bulunamadı, atlanıyor.")
            continue

        if os.path.exists(structured_data_file):
            with open(structured_data_file, "r", encoding="utf-8") as f:
                structured_data = json.load(f)

        generate_html_file(continent_name, videos_data, structured_data)

if __name__ == "__main__":
    main()
