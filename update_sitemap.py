import datetime
from country_info import COUNTRY_INFO, CONTINENT_INFO

BASE_URL = "https://www.toptubelist.com"
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

# Kıta sayfaları (örnek: /asia, /europe)
for continent_slug in CONTINENT_INFO.keys():
    urls.append(f"""
  <url>
    <loc>{BASE_URL}/{continent_slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.9</priority>
  </url>""")

# Ülke sayfaları (örnek: /turkey, /united-states)
for country_slug in COUNTRY_INFO.keys():
    urls.append(f"""
  <url>
    <loc>{BASE_URL}/{country_slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>""")

# XML dosyasını oluştur
sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print("✅ sitemap.xml oluşturuldu.")
