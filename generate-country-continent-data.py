# generate_json.py
import json
from country_continent_data import COUNTRY_INFO # country_data.py dosyasından COUNTRY_INFO'yu içe aktar

# JSON için formatı dönüştürelim
# Display name varsa onu, yoksa anahtarı (country_slug) kullanacağız
# Link için country_slug.html formatını kullanacağız
# Harf için display name veya country_slug'ın ilk harfini kullanacağız

formatted_countries_for_js = []
for country_slug, data in COUNTRY_INFO.items():
    display_name = data.get("display-name", country_slug.replace("-", " ")).title() # Baş harfleri büyük yap
    formatted_countries_for_js.append({
        "name": display_name,
        "link": f"{country_slug}.html", # Link formatı: country-slug.html
        "letter": display_name[0].upper(), # Görünen adın ilk harfi
        "code": data["code"],
        "continent": data["continent"]
    })

# JSON dosyasını yazma
output_filename = "countries.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(formatted_countries_for_js, f, indent=2, ensure_ascii=False)

print(f"{output_filename} dosyası başarıyla oluşturuldu.")
