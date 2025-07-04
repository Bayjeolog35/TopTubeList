import os
import json

def generate_html_file(continent_name, videos_data, structured_data):
    """Kıta sayfası için HTML dosyasını /continents klasörü altına oluşturur."""

    sanitized_continent_name = continent_name.replace("_", "-")
    display_continent_name = continent_name.replace("-", " ").replace("_", " ").title()

    # Aktif kıta linkini vurgulamak için class ayarları
    def is_active(name): return "active" if name == continent_name else ""

    # Navigasyon menüsü
    continent_nav_html = f"""
    <nav id="continentNav">
        <a href="/index.html">Worldwide</a>
        <a href="/asia/" class="{is_active('asia')}">Asia</a>
        <a href="/europe/" class="{is_active('europe')}">Europe</a>
        <a href="/africa/" class="{is_active('africa')}">Africa</a>
        <a href="/north_america/" class="{is_active('north_america')}">North America</a>
        <a href="/south_america/" class="{is_active('south_america')}">South America</a>
        <a href="/oceania/" class="{is_active('oceania')}">Oceania</a>
    </nav>
    """

    # Structured Data bloğu
    structured_data_block = ""
    if structured_data:
        structured_json = json.dumps(structured_data, indent=2)
        structured_data_block = (
            '<script type="application/ld+json">\n' +
            structured_json +
            '\n</script>'
        )

    # HTML template
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
  {continent_nav_html}
  <h1>Trending in {display_continent_name}</h1>
  <div id="videoList"></div>
  <script>
    fetch("/videos_{continent_name}.json")
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

    # Klasöre yaz
    output_dir = os.path.join("continents", sanitized_continent_name)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"✅ {output_path} oluşturuldu.")


def main():
    videos_base_dir = "."
    structured_data_base_dir = "."
    continents = ["asia", "africa", "europe", "north_america", "south_america", "oceania"]

    for continent_name in continents:
        videos_file = os.path.join(videos_base_dir, f"videos_{continent_name}.json")
        structured_data_file = os.path.join(structured_data_base_dir, f"structured_data_{continent_name}.json")

        videos_data = []
        structured_data = {}

        # Video JSON dosyasını oku
        if os.path.exists(videos_file):
            try:
                with open(videos_file, "r", encoding="utf-8") as f:
                    videos_data = json.load(f)
            except Exception as e:
                print(f"HATA: {videos_file} okunurken hata: {e}")
        else:
            print(f"UYARI: {videos_file} bulunamadı.")

        # Structured data JSON dosyasını oku
        if os.path.exists(structured_data_file):
            try:
                with open(structured_data_file, "r", encoding="utf-8") as f:
                    structured_data = json.load(f)
            except Exception as e:
                print(f"HATA: {structured_data_file} okunurken hata: {e}")
        else:
            print(f"UYARI: {structured_data_file} bulunamadı.")

        # HTML dosyasını oluştur
        generate_html_file(continent_name, videos_data, structured_data)


if __name__ == "__main__":
    main()
