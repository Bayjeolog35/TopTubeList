import datetime

BASE_URL = "https://toptubelist.com"

COUNTRY_SLUGS = [
    "turkey", "united-states", "germany", "brazil", "india", "japan", "france",
    # ... diğer 194 ülke
]

CONTINENT_SLUGS = [
    "africa", "asia", "europe", "north-america", "south-america", "oceania"
]

today = datetime.date.today().isoformat()

urls = []

# Ana sayfa
urls.append(f"""
  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>""")

# Kıta sayfaları
for continent in CONTINENT_SLUGS:
    urls.append(f"""
  <url>
    <loc>{BASE_URL}/{continent}.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.9</priority>
  </url>""")

# Ülke sayfaları
for country in COUNTRY_SLUGS:
    urls.append(f"""
  <url>
    <loc>{BASE_URL}/{country}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print("✅ sitemap.xml oluşturuldu.")
