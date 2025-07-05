from country_data import COUNTRY_INFO
from collections import defaultdict
import json
import os

buttons = []

for country, info in COUNTRY_INFO.items():
    entry = {
        "continent": info["continent"].lower(),
        "country": country.lower(),
        "label": country.replace("_", " ").title(),
        "url": f"/{country.lower()}"
    }
    buttons.append(entry)

# Çıktı klasörü
os.makedirs("output", exist_ok=True)

# JSON olarak yaz
with open("output/buttons.json", "w", encoding="utf-8") as f:
    json.dump(buttons, f, indent=2)

print("✔ 'buttons.json' başarıyla oluşturuldu.")
