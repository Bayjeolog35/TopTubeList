#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TopTubeList - All HTML GENERATOR
Bu script ülke-adi.html dosyalarını oluşturur.
"""

import os
import json
from datetime import datetime, UTC

#ülke ve kıta bilgileri

CONTINENT_INFO = {
    "asia": {
        "name": "Asia",
        "meta_description": "Trending YouTube videos in Asia - Most viewed content across Asian countries"
    },
    "europe": {
        "name": "Europe", 
        "meta_description": "Popular YouTube videos trending in European countries - Updated hourly"
    },
    "africa": {
        "name": "Africa",
        "meta_description": "Top viewed YouTube videos across African nations - Daily updated charts"
    },
    "north-america": {
        "name": "North America",
        "meta_description": "Viral YouTube content in USA, Canada and Mexico - Real-time trending videos"
    },
    "south-america": {
        "name": "South America",
        "meta_description": "Most watched YouTube videos in South American countries - Updated constantly"
    },
    "oceania": {
        "name": "Oceania",
        "meta_description": "Trending YouTube videos from Australia, New Zealand and Pacific Islands"
    },

}

COUNTRY_INFO = {
    "afghanistan": {
        "name": "Afghanistan",
        "meta_description": "Trending YouTube videos in Afghanistan - Most viewed content"
    },
    "albania": {
        "name": "Albania",
        "meta_description": "Trending YouTube videos in Albania - Most viewed content"
    },
    "algeria": {
        "name": "Algeria",
        "meta_description": "Trending YouTube videos in Algeria - Most viewed content"
    },
    "andorra": {
        "name": "Andorra",
        "meta_description": "Trending YouTube videos in Andorra - Most viewed content"
    },
    "angola": {
        "name": "Angola",
        "meta_description": "Trending YouTube videos in Angola - Most viewed content"
    },
    "antigua-and-barbuda": {
        "name": "Antigua and Barbuda",
        "meta_description": "Trending YouTube videos in Antigua and Barbuda - Most viewed content"
    },
    "argentina": {
        "name": "Argentina",
        "meta_description": "Trending YouTube videos in Argentina - Most viewed content"
    },
    "armenia": {
        "name": "Armenia",
        "meta_description": "Trending YouTube videos in Armenia - Most viewed content"
    },
    "australia": {
        "name": "Australia",
        "meta_description": "Trending YouTube videos in Australia - Most viewed content"
    },
    "austria": {
        "name": "Austria",
        "meta_description": "Trending YouTube videos in Austria - Most viewed content"
    },
    "azerbaijan": {
        "name": "Azerbaijan",
        "meta_description": "Trending YouTube videos in Azerbaijan - Most viewed content"
    },
    "bahamas": {
        "name": "Bahamas",
        "meta_description": "Trending YouTube videos in Bahamas - Most viewed content"
    },
    "bahrain": {
        "name": "Bahrain",
        "meta_description": "Trending YouTube videos in Bahrain - Most viewed content"
    },
    "bangladesh": {
        "name": "Bangladesh",
        "meta_description": "Trending YouTube videos in Bangladesh - Most viewed content"
    },
    "barbados": {
        "name": "Barbados",
        "meta_description": "Trending YouTube videos in Barbados - Most viewed content"
    },
    "belarus": {
        "name": "Belarus",
        "meta_description": "Trending YouTube videos in Belarus - Most viewed content"
    },
    "belgium": {
        "name": "Belgium",
        "meta_description": "Trending YouTube videos in Belgium - Most viewed content"
    },
    "belize": {
        "name": "Belize",
        "meta_description": "Trending YouTube videos in Belize - Most viewed content"
    },
    "benin": {
        "name": "Benin",
        "meta_description": "Trending YouTube videos in Benin - Most viewed content"
    },
    "bhutan": {
        "name": "Bhutan",
        "meta_description": "Trending YouTube videos in Bhutan - Most viewed content"
    },
    "bolivia": {
        "name": "Bolivia",
        "meta_description": "Trending YouTube videos in Bolivia - Most viewed content"
    },
    "bosnia-and-herzegovina": {
        "name": "Bosnia and Herzegovina",
        "meta_description": "Trending YouTube videos in Bosnia and Herzegovina - Most viewed content"
    },
    "botswana": {
        "name": "Botswana",
        "meta_description": "Trending YouTube videos in Botswana - Most viewed content"
    },
    "brazil": {
        "name": "Brazil",
        "meta_description": "Trending YouTube videos in Brazil - Most viewed content"
    },
    "brunei": {
        "name": "Brunei",
        "meta_description": "Trending YouTube videos in Brunei - Most viewed content"
    },
    "bulgaria": {
        "name": "Bulgaria",
        "meta_description": "Trending YouTube videos in Bulgaria - Most viewed content"
    },
    "burkina-faso": {
        "name": "Burkina Faso",
        "meta_description": "Trending YouTube videos in Burkina Faso - Most viewed content"
    },
    "burundi": {
        "name": "Burundi",
        "meta_description": "Trending YouTube videos in Burundi - Most viewed content"
    },
    "cabo-verde": {
        "name": "Cabo Verde",
        "meta_description": "Trending YouTube videos in Cabo Verde - Most viewed content"
    },
    "cambodia": {
        "name": "Cambodia",
        "meta_description": "Trending YouTube videos in Cambodia - Most viewed content"
    },
    "cameroon": {
        "name": "Cameroon",
        "meta_description": "Trending YouTube videos in Cameroon - Most viewed content"
    },
    "canada": {
        "name": "Canada",
        "meta_description": "Trending YouTube videos in Canada - Most viewed content"
    },
    "central-african-republic": {
        "name": "Central African Republic",
        "meta_description": "Trending YouTube videos in Central African Republic - Most viewed content"
    },
    "chad": {
        "name": "Chad",
        "meta_description": "Trending YouTube videos in Chad - Most viewed content"
    },
    "chile": {
        "name": "Chile",
        "meta_description": "Trending YouTube videos in Chile - Most viewed content"
    },
    "china": {
        "name": "China",
        "meta_description": "Trending YouTube videos in China - Most viewed content"
    },
    "colombia": {
        "name": "Colombia",
        "meta_description": "Trending YouTube videos in Colombia - Most viewed content"
    },
    "comoros": {
        "name": "Comoros",
        "meta_description": "Trending YouTube videos in Comoros - Most viewed content"
    },
    "congo-democratic-republic-of-the": {
        "name": "Congo (Democratic Republic of the)",
        "meta_description": "Trending YouTube videos in Congo (Democratic Republic of the) - Most viewed content"
    },
    "congo-republic-of-the": {
        "name": "Congo (Republic of the)",
        "meta_description": "Trending YouTube videos in Congo (Republic of the) - Most viewed content"
    },
    "costa-rica": {
        "name": "Costa Rica",
        "meta_description": "Trending YouTube videos in Costa Rica - Most viewed content"
    },
    "cote-d-ivoire": {
        "name": "Cote d'Ivoire",
        "meta_description": "Trending YouTube videos in Cote d'Ivoire - Most viewed content"
    },
    "croatia": {
        "name": "Croatia",
        "meta_description": "Trending YouTube videos in Croatia - Most viewed content"
    },
    "cuba": {
        "name": "Cuba",
        "meta_description": "Trending YouTube videos in Cuba - Most viewed content"
    },
    "cyprus": {
        "name": "Cyprus",
        "meta_description": "Trending YouTube videos in Cyprus - Most viewed content"
    },
    "czech-republic": {
        "name": "Czech Republic",
        "meta_description": "Trending YouTube videos in Czech Republic - Most viewed content"
    },
    "denmark": {
        "name": "Denmark",
        "meta_description": "Trending YouTube videos in Denmark - Most viewed content"
    },
    "djibouti": {
        "name": "Djibouti",
        "meta_description": "Trending YouTube videos in Djibouti - Most viewed content"
    },
    "dominica": {
        "name": "Dominica",
        "meta_description": "Trending YouTube videos in Dominica - Most viewed content"
    },
    "dominican-republic": {
        "name": "Dominican Republic",
        "meta_description": "Trending YouTube videos in Dominican Republic - Most viewed content"
    },
    "east-timor": {
        "name": "East Timor",
        "meta_description": "Trending YouTube videos in East Timor - Most viewed content"
    },
    "ecuador": {
        "name": "Ecuador",
        "meta_description": "Trending YouTube videos in Ecuador - Most viewed content"
    },
    "egypt": {
        "name": "Egypt",
        "meta_description": "Trending YouTube videos in Egypt - Most viewed content"
    },
    "el-salvador": {
        "name": "El Salvador",
        "meta_description": "Trending YouTube videos in El Salvador - Most viewed content"
    },
    "equatorial-guinea": {
        "name": "Equatorial Guinea",
        "meta_description": "Trending YouTube videos in Equatorial Guinea - Most viewed content"
    },
    "eritrea": {
        "name": "Eritrea",
        "meta_description": "Trending YouTube videos in Eritrea - Most viewed content"
    },
    "estonia": {
        "name": "Estonia",
        "meta_description": "Trending YouTube videos in Estonia - Most viewed content"
    },
    "eswatini": {
        "name": "Eswatini",
        "meta_description": "Trending YouTube videos in Eswatini - Most viewed content"
    },
    "ethiopia": {
        "name": "Ethiopia",
        "meta_description": "Trending YouTube videos in Ethiopia - Most viewed content"
    },
    "fiji": {
        "name": "Fiji",
        "meta_description": "Trending YouTube videos in Fiji - Most viewed content"
    },
    "finland": {
        "name": "Finland",
        "meta_description": "Trending YouTube videos in Finland - Most viewed content"
    },
    "france": {
        "name": "France",
        "meta_description": "Trending YouTube videos in France - Most viewed content"
    },
    "gabon": {
        "name": "Gabon",
        "meta_description": "Trending YouTube videos in Gabon - Most viewed content"
    },
    "gambia": {
        "name": "Gambia",
        "meta_description": "Trending YouTube videos in Gambia - Most viewed content"
    },
    "georgia": {
        "name": "Georgia",
        "meta_description": "Trending YouTube videos in Georgia - Most viewed content"
    },
    "germany": {
        "name": "Germany",
        "meta_description": "Trending YouTube videos in Germany - Most viewed content"
    },
    "ghana": {
        "name": "Ghana",
        "meta_description": "Trending YouTube videos in Ghana - Most viewed content"
    },
    "greece": {
        "name": "Greece",
        "meta_description": "Trending YouTube videos in Greece - Most viewed content"
    },
    "grenada": {
        "name": "Grenada",
        "meta_description": "Trending YouTube videos in Grenada - Most viewed content"
    },
    "guatemala": {
        "name": "Guatemala",
        "meta_description": "Trending YouTube videos in Guatemala - Most viewed content"
    },
    "guinea": {
        "name": "Guinea",
        "meta_description": "Trending YouTube videos in Guinea - Most viewed content"
    },
    "guinea-bissau": {
        "name": "Guinea-Bissau",
        "meta_description": "Trending YouTube videos in Guinea-Bissau - Most viewed content"
    },
    "guyana": {
        "name": "Guyana",
        "meta_description": "Trending YouTube videos in Guyana - Most viewed content"
    },
    "haiti": {
        "name": "Haiti",
        "meta_description": "Trending YouTube videos in Haiti - Most viewed content"
    },
    "honduras": {
        "name": "Honduras",
        "meta_description": "Trending YouTube videos in Honduras - Most viewed content"
    },
    "hungary": {
        "name": "Hungary",
        "meta_description": "Trending YouTube videos in Hungary - Most viewed content"
    },
    "iceland": {
        "name": "Iceland",
        "meta_description": "Trending YouTube videos in Iceland - Most viewed content"
    },
    "india": {
        "name": "India",
        "meta_description": "Trending YouTube videos in India - Most viewed content"
    },
    "indonesia": {
        "name": "Indonesia",
        "meta_description": "Trending YouTube videos in Indonesia - Most viewed content"
    },
    "iran": {
        "name": "Iran",
        "meta_description": "Trending YouTube videos in Iran - Most viewed content"
    },
    "iraq": {
        "name": "Iraq",
        "meta_description": "Trending YouTube videos in Iraq - Most viewed content"
    },
    "ireland": {
        "name": "Ireland",
        "meta_description": "Trending YouTube videos in Ireland - Most viewed content"
    },
    "israel": {
        "name": "Israel",
        "meta_description": "Trending YouTube videos in Israel - Most viewed content"
    },
    "italy": {
        "name": "Italy",
        "meta_description": "Trending YouTube videos in Italy - Most viewed content"
    },
    "jamaica": {
        "name": "Jamaica",
        "meta_description": "Trending YouTube videos in Jamaica - Most viewed content"
    },
    "japan": {
        "name": "Japan",
        "meta_description": "Trending YouTube videos in Japan - Most viewed content"
    },
    "jordan": {
        "name": "Jordan",
        "meta_description": "Trending YouTube videos in Jordan - Most viewed content"
    },
    "kazakhstan": {
        "name": "Kazakhstan",
        "meta_description": "Trending YouTube videos in Kazakhstan - Most viewed content"
    },
    "kenya": {
        "name": "Kenya",
        "meta_description": "Trending YouTube videos in Kenya - Most viewed content"
    },
    "kiribati": {
        "name": "Kiribati",
        "meta_description": "Trending YouTube videos in Kiribati - Most viewed content"
    },
    "korea-north": {
        "name": "Korea (North)",
        "meta_description": "Trending YouTube videos in North Korea - Most viewed content"
    },
    "korea-south": {
        "name": "Korea (South)",
        "meta_description": "Trending YouTube videos in South Korea - Most viewed content"
    },
    "kosovo": {
        "name": "Kosovo",
        "meta_description": "Trending YouTube videos in Kosovo - Most viewed content"
    },
    "kuwait": {
        "name": "Kuwait",
        "meta_description": "Trending YouTube videos in Kuwait - Most viewed content"
    },
    "kyrgyzstan": {
        "name": "Kyrgyzstan",
        "meta_description": "Trending YouTube videos in Kyrgyzstan - Most viewed content"
    },
    "laos": {
        "name": "Laos",
        "meta_description": "Trending YouTube videos in Laos - Most viewed content"
    },
    "latvia": {
        "name": "Latvia",
        "meta_description": "Trending YouTube videos in Latvia - Most viewed content"
    },
    "lebanon": {
        "name": "Lebanon",
        "meta_description": "Trending YouTube videos in Lebanon - Most viewed content"
    },
    "lesotho": {
        "name": "Lesotho",
        "meta_description": "Trending YouTube videos in Lesotho - Most viewed content"
    },
    "liberia": {
        "name": "Liberia",
        "meta_description": "Trending YouTube videos in Liberia - Most viewed content"
    },
    "libya": {
        "name": "Libya",
        "meta_description": "Trending YouTube videos in Libya - Most viewed content"
    },
    "liechtenstein": {
        "name": "Liechtenstein",
        "meta_description": "Trending YouTube videos in Liechtenstein - Most viewed content"
    },
    "lithuania": {
        "name": "Lithuania",
        "meta_description": "Trending YouTube videos in Lithuania - Most viewed content"
    },
    "luxembourg": {
        "name": "Luxembourg",
        "meta_description": "Trending YouTube videos in Luxembourg - Most viewed content"
    },
    "madagascar": {
        "name": "Madagascar",
        "meta_description": "Trending YouTube videos in Madagascar - Most viewed content"
    },
    "malawi": {
        "name": "Malawi",
        "meta_description": "Trending YouTube videos in Malawi - Most viewed content"
    },
    "malaysia": {
        "name": "Malaysia",
        "meta_description": "Trending YouTube videos in Malaysia - Most viewed content"
    },
    "maldives": {
        "name": "Maldives",
        "meta_description": "Trending YouTube videos in Maldives - Most viewed content"
    },
    "mali": {
        "name": "Mali",
        "meta_description": "Trending YouTube videos in Mali - Most viewed content"
    },
    "malta": {
        "name": "Malta",
        "meta_description": "Trending YouTube videos in Malta - Most viewed content"
    },
    "marshall-islands": {
        "name": "Marshall Islands",
        "meta_description": "Trending YouTube videos in Marshall Islands - Most viewed content"
    },
    "mauritania": {
        "name": "Mauritania",
        "meta_description": "Trending YouTube videos in Mauritania - Most viewed content"
    },
    "mauritius": {
        "name": "Mauritius",
        "meta_description": "Trending YouTube videos in Mauritius - Most viewed content"
    },
    "mexico": {
        "name": "Mexico",
        "meta_description": "Trending YouTube videos in Mexico - Most viewed content"
    },
    "micronesia": {
        "name": "Micronesia",
        "meta_description": "Trending YouTube videos in Micronesia - Most viewed content"
    },
    "moldova": {
        "name": "Moldova",
        "meta_description": "Trending YouTube videos in Moldova - Most viewed content"
    },
    "monaco": {
        "name": "Monaco",
        "meta_description": "Trending YouTube videos in Monaco - Most viewed content"
    },
    "mongolia": {
        "name": "Mongolia",
        "meta_description": "Trending YouTube videos in Mongolia - Most viewed content"
    },
    "montenegro": {
        "name": "Montenegro",
        "meta_description": "Trending YouTube videos in Montenegro - Most viewed content"
    },
    "morocco": {
        "name": "Morocco",
        "meta_description": "Trending YouTube videos in Morocco - Most viewed content"
    },
    "mozambique": {
        "name": "Mozambique",
        "meta_description": "Trending YouTube videos in Mozambique - Most viewed content"
    },
    "myanmar": {
        "name": "Myanmar",
        "meta_description": "Trending YouTube videos in Myanmar - Most viewed content"
    },
    "namibia": {
        "name": "Namibia",
        "meta_description": "Trending YouTube videos in Namibia - Most viewed content"
    },
    "nauru": {
        "name": "Nauru",
        "meta_description": "Trending YouTube videos in Nauru - Most viewed content"
    },
    "nepal": {
        "name": "Nepal",
        "meta_description": "Trending YouTube videos in Nepal - Most viewed content"
    },
    "netherlands": {
        "name": "Netherlands",
        "meta_description": "Trending YouTube videos in Netherlands - Most viewed content"
    },
    "new-zealand": {
        "name": "New Zealand",
        "meta_description": "Trending YouTube videos in New Zealand - Most viewed content"
    },
    "nicaragua": {
        "name": "Nicaragua",
        "meta_description": "Trending YouTube videos in Nicaragua - Most viewed content"
    },
    "niger": {
        "name": "Niger",
        "meta_description": "Trending YouTube videos in Niger - Most viewed content"
    },
    "nigeria": {
        "name": "Nigeria",
        "meta_description": "Trending YouTube videos in Nigeria - Most viewed content"
    },
    "north-macedonia": {
        "name": "North Macedonia",
        "meta_description": "Trending YouTube videos in North Macedonia - Most viewed content"
    },
    "norway": {
        "name": "Norway",
        "meta_description": "Trending YouTube videos in Norway - Most viewed content"
    },
    "oman": {
        "name": "Oman",
        "meta_description": "Trending YouTube videos in Oman - Most viewed content"
    },
    "pakistan": {
        "name": "Pakistan",
        "meta_description": "Trending YouTube videos in Pakistan - Most viewed content"
    },
    "palau": {
        "name": "Palau",
        "meta_description": "Trending YouTube videos in Palau - Most viewed content"
    },
    "palestine": {
        "name": "Palestine",
        "meta_description": "Trending YouTube videos in Palestine - Most viewed content"
    },
    "panama": {
        "name": "Panama",
        "meta_description": "Trending YouTube videos in Panama - Most viewed content"
    },
    "papua-new-guinea": {
        "name": "Papua New Guinea",
        "meta_description": "Trending YouTube videos in Papua New Guinea - Most viewed content"
    },
    "paraguay": {
        "name": "Paraguay",
        "meta_description": "Trending YouTube videos in Paraguay - Most viewed content"
    },
    "peru": {
        "name": "Peru",
        "meta_description": "Trending YouTube videos in Peru - Most viewed content"
    },
    "philippines": {
        "name": "Philippines",
        "meta_description": "Trending YouTube videos in Philippines - Most viewed content"
    },
    "poland": {
        "name": "Poland",
        "meta_description": "Trending YouTube videos in Poland - Most viewed content"
    },
    "portugal": {
        "name": "Portugal",
        "meta_description": "Trending YouTube videos in Portugal - Most viewed content"
    },
    "qatar": {
        "name": "Qatar",
        "meta_description": "Trending YouTube videos in Qatar - Most viewed content"
    },
    "romania": {
        "name": "Romania",
        "meta_description": "Trending YouTube videos in Romania - Most viewed content"
    },
    "russia": {
        "name": "Russia",
        "meta_description": "Trending YouTube videos in Russia - Most viewed content"
    },
    "rwanda": {
        "name": "Rwanda",
        "meta_description": "Trending YouTube videos in Rwanda - Most viewed content"
    },
    "saint-kitts-and-nevis": {
        "name": "Saint Kitts and Nevis",
        "meta_description": "Trending YouTube videos in Saint Kitts and Nevis - Most viewed content"
    },
    "saint-lucia": {
        "name": "Saint Lucia",
        "meta_description": "Trending YouTube videos in Saint Lucia - Most viewed content"
    },
    "saint-vincent-and-the-grenadines": {
        "name": "Saint Vincent and the Grenadines",
        "meta_description": "Trending YouTube videos in Saint Vincent and the Grenadines - Most viewed content"
    },
    "samoa": {
        "name": "Samoa",
        "meta_description": "Trending YouTube videos in Samoa - Most viewed content"
    },
    "san-marino": {
        "name": "San Marino",
        "meta_description": "Trending YouTube videos in San Marino - Most viewed content"
    },
    "sao-tome-and-principe": {
        "name": "Sao Tome and Principe",
        "meta_description": "Trending YouTube videos in Sao Tome and Principe - Most viewed content"
    },
    "saudi-arabia": {
        "name": "Saudi Arabia",
        "meta_description": "Trending YouTube videos in Saudi Arabia - Most viewed content"
    },
    "senegal": {
        "name": "Senegal",
        "meta_description": "Trending YouTube videos in Senegal - Most viewed content"
    },
    "serbia": {
        "name": "Serbia",
        "meta_description": "Trending YouTube videos in Serbia - Most viewed content"
    },
    "seychelles": {
        "name": "Seychelles",
        "meta_description": "Trending YouTube videos in Seychelles - Most viewed content"
    },
    "sierra-leone": {
        "name": "Sierra Leone",
        "meta_description": "Trending YouTube videos in Sierra Leone - Most viewed content"
    },
    "singapore": {
        "name": "Singapore",
        "meta_description": "Trending YouTube videos in Singapore - Most viewed content"
    },
    "slovakia": {
        "name": "Slovakia",
        "meta_description": "Trending YouTube videos in Slovakia - Most viewed content"
    },
    "slovenia": {
        "name": "Slovenia",
        "meta_description": "Trending YouTube videos in Slovenia - Most viewed content"
    },
    "solomon-islands": {
        "name": "Solomon Islands",
        "meta_description": "Trending YouTube videos in Solomon Islands - Most viewed content"
    },
    "somalia": {
        "name": "Somalia",
        "meta_description": "Trending YouTube videos in Somalia - Most viewed content"
    },
    "south-africa": {
        "name": "South Africa",
        "meta_description": "Trending YouTube videos in South Africa - Most viewed content"
    },
    "south-sudan": {
        "name": "South Sudan",
        "meta_description": "Trending YouTube videos in South Sudan - Most viewed content"
    },
    "spain": {
        "name": "Spain",
        "meta_description": "Trending YouTube videos in Spain - Most viewed content"
    },
    "sri-lanka": {
        "name": "Sri Lanka",
        "meta_description": "Trending YouTube videos in Sri Lanka - Most viewed content"
    },
    "sudano": {
        "name": "Sudan",
        "meta_description": "Trending YouTube videos in Sudan - Most viewed content"
    },
    "suriname": {
        "name": "Suriname",
        "meta_description": "Trending YouTube videos in Suriname - Most viewed content"
    },
    "sweden": {
        "name": "Sweden",
        "meta_description": "Trending YouTube videos in Sweden - Most viewed content"
    },
    "switzerland": {
        "name": "Switzerland",
        "meta_description": "Trending YouTube videos in Switzerland - Most viewed content"
    },
    "syria": {
        "name": "Syria",
        "meta_description": "Trending YouTube videos in Syria - Most viewed content"
    },
    "taiwan": {
        "name": "Taiwan",
        "meta_description": "Trending YouTube videos in Taiwan - Most viewed content"
    },
    "tajikistan": {
        "name": "Tajikistan",
        "meta_description": "Trending YouTube videos in Tajikistan - Most viewed content"
    },
    "tanzania": {
        "name": "Tanzania",
        "meta_description": "Trending YouTube videos in Tanzania - Most viewed content"
    },
    "thailand": {
        "name": "Thailand",
        "meta_description": "Trending YouTube videos in Thailand - Most viewed content"
    },
    "togo": {
        "name": "Togo",
        "meta_description": "Trending YouTube videos in Togo - Most viewed content"
    },
    "tonga": {
        "name": "Tonga",
        "meta_description": "Trending YouTube videos in Tonga - Most viewed content"
    },
    "trinidad-and-tobago": {
        "name": "Trinidad and Tobago",
        "meta_description": "Trending YouTube videos in Trinidad and Tobago - Most viewed content"
    },
    "tunisia": {
        "name": "Tunisia",
        "meta_description": "Trending YouTube videos in Tunisia - Most viewed content"
    },
    "turkey": {
        "name": "Turkey",
        "meta_description": "Trending YouTube videos in Turkey - Most viewed content"
    },
    "turkmenistan": {
        "name": "Turkmenistan",
        "meta_description": "Trending YouTube videos in Turkmenistan - Most viewed content"
    },
    "tuvalu": {
        "name": "Tuvalu",
        "meta_description": "Trending YouTube videos in Tuvalu - Most viewed content"
    },
    "uganda": {
        "name": "Uganda",
        "meta_description": "Trending YouTube videos in Uganda - Most viewed content"
    },
    "ukraine": {
        "name": "Ukraine",
        "meta_description": "Trending YouTube videos in Ukraine - Most viewed content"
    },
    "united-arab-emirates": {
        "name": "United Arab Emirates",
        "meta_description": "Trending YouTube videos in United Arab Emirates - Most viewed content"
    },
    "united-kingdom": {
        "name": "United Kingdom",
        "meta_description": "Trending YouTube videos in United Kingdom - Most viewed content"
    },
    "united-states": {
        "name": "United States",
        "meta_description": "Trending YouTube videos in United States - Most viewed content"
    },
    "uruguay": {
        "name": "Uruguay",
        "meta_description": "Trending YouTube videos in Uruguay - Most viewed content"
    },
    "uzbekistan": {
        "name": "Uzbekistan",
        "meta_description": "Trending YouTube videos in Uzbekistan - Most viewed content"
    },
    "vanuatu": {
        "name": "Vanuatu",
        "meta_description": "Trending YouTube videos in Vanuatu - Most viewed content"
    },
    "vatican-city": {
        "name": "Vatican City",
        "meta_description": "Trending YouTube videos in Vatican City - Most viewed content"
    },
    "venezuela": {
        "name": "Venezuela",
        "meta_description": "Trending YouTube videos in Venezuela - Most viewed content"
    },
    "vietnam": {
        "name": "Vietnam",
        "meta_description": "Trending YouTube videos in Vietnam - Most viewed content"
    },
    "yemen": {
        "name": "Yemen",
        "meta_description": "Trending YouTube videos in Yemen - Most viewed content"
    },
    "zambia": {
        "name": "Zambia",
        "meta_description": "Trending YouTube videos in Zambia - Most viewed content"
    },
    "zimbabwe": {
        "name": "Zimbabwe",
        "meta_description": "Trending YouTube videos in Zimbabwe - Most viewed content"
    }
}

def load_json_data(file_path):
    """JSON dosyasını yükler ve veriyi döndürür."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Uyarı: {file_path} bulunamadı. Boş veri kullanılıyor.")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️ Uyarı: {file_path} okunurken hata oluştu: {str(e)}")
        return []

def get_html_output_path(name):
    """
    Verilen isim (ülke ya da kıta) için HTML dosyasının tam yolunu döndürür.
    Örnek: "africa" → /path/to/project/africa.html
           "united-states" → /path/to/project/united-states.html
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f"{name}.html"
    return os.path.join(script_dir, file_name)

def generate_top_video_iframe(videos_data):
    """En çok izlenen video için iframe kodu oluşturur. Eksik verilerde kırılmaz."""
    if not videos_data or len(videos_data) == 0:
        return "<!-- No video data available -->"

    top_video = videos_data[0]

    # Güvenli veri çekimi
    video_id = top_video.get("videoId")
    title = top_video.get("title", "Untitled")
    views_str = top_video.get("views_str", "N/A")
    duration = top_video.get("duration", "N/A")

    if not video_id:
        return "<!-- videoId missing for top video -->"

    return f"""
    <div class="featured-video">
        <h2>🔥 Most Viewed Video</h2>
        <div class="video-container">
            <iframe 
                loading="lazy"
                src="https://www.youtube.com/embed/{video_id}" 
                title="{title}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
            </iframe>
        </div>
        <div class="video-info">
            <h3>{title}</h3>
            <p>👀 {views_str} views | ⏱️ {duration}</p>
        </div>
    </div>
    """

def generate_html_content(name, videos_data, structured_data, is_country=True):
    info_dict = COUNTRY_INFO if is_country else CONTINENT_INFO
    readable_name = info_dict.get(name, {}).get("name", name.replace("_", " ").title())
    meta_description = info_dict.get(name, {}).get("meta_description", f"Trending YouTube videos in {readable_name} - Updated every 3 hours")

      # Tag Manager head kodu
    gtm_head = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-N865S9W3');</script>
<!-- End Google Tag Manager -->"""

    # GTM noscript body başlangıcı için
    gtm_noscript = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-N865S9W3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""
    
    # 🎯 IFRAME: en çok izlenen videoyu al
    top_video_iframe = generate_top_video_iframe(videos_data)

    # 🎯 STRUCTURED: sadece ilk structured item’ı al
    structured_block = ""
if structured_data and isinstance(structured_data, list):
    structured_block = (
        '<script type="application/ld+json">\n'
        + json.dumps(structured_data, ensure_ascii=False, indent=2)
        + '\n</script>'
    )

    current_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")


    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  {gtm_head}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trending YouTube Videos in name | TopTubeList</title>
  <meta name="description" content="{meta_description}">
  <meta name="robots" content="index, follow">
  <meta name="google-adsense-account" content="ca-pub-6698104628153103">
  <link rel="canonical" href="https://toptubelist.com/{name}.html">
  <link rel="stylesheet" href="style.css">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6698104628153103" crossorigin="anonymous"></script>
  {structured_block}
</script>
</head>
<body>
    {gtm_noscript}
    <header>
        <div class="container">
            <a href="../../index.html" class="logo">
                <img src="TopTubeListLogo.webp" alt="TopTubeList" width="120">
            </a>
            <h1 id="pageTitle">Trending in {readable_name}</h1>
            <button id="darkModeToggle" title="Toggle Dark Mode">🌓</button>
        </div>
        

  <nav id="continentNav">
    <a href="index.html" class="{ 'active' if name == 'index' else '' }">Worldwide</a>
    <a href="asia.html" class="{ 'active' if name == 'asia' else '' }">Asia</a>
    <a href="europe.html" class="{ 'active' if name == 'europe' else '' }">Europe</a>
    <a href="africa.html" class="{ 'active' if name == 'africa' else '' }">Africa</a>
    <a href="north-america.html" class="{ 'active' if name == 'north-america' else '' }">North America</a>
    <a href="south-america.html" class="{ 'active' if name == 'south-america' else '' }">South America</a>
    <a href="oceania.html" class="{ 'active' if name == 'oceania' else '' }">Oceania</a>
  </nav>
</header>

<main class="main-content">

  <button id="hamburgerBtn" class="hamburger">&#9776;</button>
  <div class="layout-wrapper">
<div class="country-panel">
  <div class="alphabet-column"> <a href="#" class="alphabet-letter" data-letter="all">All</a>
    <a href="#" class="alphabet-letter" data-letter="A">A</a>
    <a href="#" class="alphabet-letter" data-letter="B">B</a>
    <a href="#" class="alphabet-letter" data-letter="C">C</a>
    <a href="#" class="alphabet-letter" data-letter="D">D</a>
    <a href="#" class="alphabet-letter" data-letter="E">E</a>
    <a href="#" class="alphabet-letter" data-letter="F">F</a>
    <a href="#" class="alphabet-letter" data-letter="G">G</a>
    <a href="#" class="alphabet-letter" data-letter="H">H</a>
    <a href="#" class="alphabet-letter" data-letter="I">I</a>
    <a href="#" class="alphabet-letter" data-letter="J">J</a>
    <a href="#" class="alphabet-letter" data-letter="K">K</a>
    <a href="#" class="alphabet-letter" data-letter="L">L</a>
    <a href="#" class="alphabet-letter" data-letter="M">M</a>
    <a href="#" class="alphabet-letter" data-letter="N">N</a>
    <a href="#" class="alphabet-letter" data-letter="O">O</a>
    <a href="#" class="alphabet-letter" data-letter="P">P</a>
    <a href="#" class="alphabet-letter" data-letter="Q">Q</a>
    <a href="#" class="alphabet-letter" data-letter="R">R</a>
    <a href="#" class="alphabet-letter" data-letter="S">S</a>
    <a href="#" class="alphabet-letter" data-letter="T">T</a>
    <a href="#" class="alphabet-letter" data-letter="U">U</a>
    <a href="#" class="alphabet-letter" data-letter="V">V</a>
    <a href="#" class="alphabet-letter" data-letter="W">W</a>
    <a href="#" class="alphabet-letter" data-letter="X">X</a>
    <a href="#" class="alphabet-letter" data-letter="Y">Y</a>
    <a href="#" class="alphabet-letter" data-letter="Z">Z</a>


</div>
     <div class="country-column">
  <a href="/afghanistan" class="country-link">Afghanistan</a>
  <a href="/albania" class="country-link">Albania</a>
  <a href="/algeria" class="country-link">Algeria</a>
  <a href="/andorra" class="country-link">Andorra</a>
  <a href="/angola" class="country-link">Angola</a>
  <a href="/antigua-and-barbuda" class="country-link">Antigua and Barbuda</a>
  <a href="/argentina" class="country-link">Argentina</a>
  <a href="/armenia" class="country-link">Armenia</a>
  <a href="/australia" class="country-link">Australia</a>
  <a href="/austria" class="country-link">Austria</a>
  <a href="/azerbaijan" class="country-link">Azerbaijan</a>

  <a href="/bahamas" class="country-link">Bahamas</a>
  <a href="/bahrain" class="country-link">Bahrain</a>
  <a href="/bangladesh" class="country-link">Bangladesh</a>
  <a href="/barbados" class="country-link">Barbados</a>
  <a href="/belarus" class="country-link">Belarus</a>
  <a href="/belgium" class="country-link">Belgium</a>
  <a href="/belize" class="country-link">Belize</a>
  <a href="/benin" class="country-link">Benin</a>
  <a href="/bhutan" class="country-link">Bhutan</a>
  <a href="/bolivia" class="country-link">Bolivia</a>
  <a href="/bosnia-and-herzegovina" class="country-link">Bosnia and Herzegovina</a>
  <a href="/botswana" class="country-link">Botswana</a>
  <a href="/brazil" class="country-link">Brazil</a>
  <a href="/brunei" class="country-link">Brunei</a>
  <a href="/bulgaria" class="country-link">Bulgaria</a>
  <a href="/burkina-faso" class="country-link">Burkina Faso</a>
  <a href="/burundi" class="country-link">Burundi</a>

  <a href="/cabo-verde" class="country-link">Cabo Verde</a>
  <a href="/cambodia" class="country-link">Cambodia</a>
  <a href="/cameroon" class="country-link">Cameroon</a>
  <a href="/canada" class="country-link">Canada</a>
  <a href="/central-african-republic" class="country-link">Central African Republic</a>
  <a href="/chad" class="country-link">Chad</a>
  <a href="/chile" class="country-link">Chile</a>
  <a href="/china" class="country-link">China</a>
  <a href="/colombia" class="country-link">Colombia</a>
  <a href="/comoros" class="country-link">Comoros</a>
  <a href="/congo-democratic-republic-of-the" class="country-link">Congo (Democratic Republic of the)</a>
  <a href="/congo-republic-of-the" class="country-link">Congo (Republic of the)</a>
  <a href="/costa-rica" class="country-link">Costa Rica</a>
  <a href="/cote-d-ivoire" class="country-link">Cote d'Ivoire</a>
  <a href="/croatia" class="country-link">Croatia</a>
  <a href="/cuba" class="country-link">Cuba</a>
  <a href="/cyprus" class="country-link">Cyprus</a>
  <a href="/czech-republic" class="country-link">Czech Republic</a>

  <a href="/denmark" class="country-link">Denmark</a>
  <a href="/djibouti" class="country-link">Djibouti</a>
  <a href="/dominica" class="country-link">Dominica</a>
  <a href="/dominican-republic" class="country-link">Dominican Republic</a>

  <a href="/east-timor" class="country-link">East Timor</a>
  <a href="/ecuador" class="country-link">Ecuador</a>
  <a href="/egypt" class="country-link">Egypt</a>
  <a href="/el-salvador" class="country-link">El Salvador</a>
  <a href="/equatorial-guinea" class="country-link">Equatorial Guinea</a>
  <a href="/eritrea" class="country-link">Eritrea</a>
  <a href="/estonia" class="country-link">Estonia</a>
  <a href="/eswatini" class="country-link">Eswatini</a>
  <a href="/ethiopia" class="country-link">Ethiopia</a>

  <a href="/fiji" class="country-link">Fiji</a>
  <a href="/finland" class="country-link">Finland</a>
  <a href="/france" class="country-link">France</a>

  <a href="/gabon" class="country-link">Gabon</a>
  <a href="/gambia" class="country-link">Gambia</a>
  <a href="/georgia" class="country-link">Georgia</a>
  <a href="/germany" class="country-link">Germany</a>
  <a href="/ghana" class="country-link">Ghana</a>
  <a href="/greece" class="country-link">Greece</a>
  <a href="/grenada" class="country-link">Grenada</a>
  <a href="/guatemala" class="country-link">Guatemala</a>
  <a href="/guinea" class="country-link">Guinea</a>
  <a href="/guinea-bissau" class="country-link">Guinea-Bissau</a>
  <a href="/guyana" class="country-link">Guyana</a>

  <a href="/haiti" class="country-link">Haiti</a>
  <a href="/honduras" class="country-link">Honduras</a>
  <a href="/hungary" class="country-link">Hungary</a>

  <a href="/iceland" class="country-link">Iceland</a>
  <a href="/india" class="country-link">India</a>
  <a href="/indonesia" class="country-link">Indonesia</a>
  <a href="/iran" class="country-link">Iran</a>
  <a href="/iraq" class="country-link">Iraq</a>
  <a href="/ireland" class="country-link">Ireland</a>
  <a href="/israel" class="country-link">Israel</a>
  <a href="/italy" class="country-link">Italy</a>

  <a href="/jamaica" class="country-link">Jamaica</a>
  <a href="/japan" class="country-link">Japan</a>
  <a href="/jordan" class="country-link">Jordan</a>

  <a href="/kazakhstan" class="country-link">Kazakhstan</a>
  <a href="/kenya" class="country-link">Kenya</a>
  <a href="/kiribati" class="country-link">Kiribati</a>
  <a href="/korea-north" class="country-link">Korea (North)</a>
  <a href="/korea-south" class="country-link">Korea (South)</a>
  <a href="/kosovo" class="country-link">Kosovo</a>
  <a href="/kuwait" class="country-link">Kuwait</a>
  <a href="/kyrgyzstan" class="country-link">Kyrgyzstan</a>

  <a href="/laos" class="country-link">Laos</a>
  <a href="/latvia" class="country-link">Latvia</a>
  <a href="/lebanon" class="country-link">Lebanon</a>
  <a href="/lesotho" class="country-link">Lesotho</a>
  <a href="/liberia" class="country-link">Liberia</a>
  <a href="/libya" class="country-link">Libya</a>
  <a href="/liechtenstein" class="country-link">Liechtenstein</a>
  <a href="/lithuania" class="country-link">Lithuania</a>
  <a href="/luxembourg" class="country-link">Luxembourg</a>

  <a href="/madagascar" class="country-link">Madagascar</a>
  <a href="/malawi" class="country-link">Malawi</a>
  <a href="/malaysia" class="country-link">Malaysia</a>
  <a href="/maldives" class="country-link">Maldives</a>
  <a href="/mali" class="country-link">Mali</a>
  <a href="/malta" class="country-link">Malta</a>
  <a href="/marshall-islands" class="country-link">Marshall Islands</a>
  <a href="/mauritania" class="country-link">Mauritania</a>
  <a href="/mauritius" class="country-link">Mauritius</a>
  <a href="/mexico" class="country-link">Mexico</a>
  <a href="/micronesia" class="country-link">Micronesia</a>
  <a href="/moldova" class="country-link">Moldova</a>
  <a href="/monaco" class="country-link">Monaco</a>
  <a href="/mongolia" class="country-link">Mongolia</a>
  <a href="/montenegro" class="country-link">Montenegro</a>
  <a href="/morocco" class="country-link">Morocco</a>
  <a href="/mozambique" class="country-link">Mozambique</a>
  <a href="/myanmar" class="country-link">Myanmar</a>

  <a href="/namibia" class="country-link">Namibia</a>
  <a href="/nauru" class="country-link">Nauru</a>
  <a href="/nepal" class="country-link">Nepal</a>
  <a href="/netherlands" class="country-link">Netherlands</a>
  <a href="/new-zealand" class="country-link">New Zealand</a>
  <a href="/nicaragua" class="country-link">Nicaragua</a>
  <a href="/niger" class="country-link">Niger</a>
  <a href="/nigeria" class="country-link">Nigeria</a>
  <a href="/north-macedonia" class="country-link">North Macedonia</a>
  <a href="/norway" class="country-link">Norway</a>

  <a href="/oman" class="country-link">Oman</a>

  <a href="/pakistan" class="country-link">Pakistan</a>
  <a href="/palau" class="country-link">Palau</a>
  <a href="/palestine" class="country-link">Palestine</a>
  <a href="/panama" class="country-link">Panama</a>
  <a href="/papua-new-guinea" class="country-link">Papua New Guinea</a>
  <a href="/paraguay" class="country-link">Paraguay</a>
  <a href="/peru" class="country-link">Peru</a>
  <a href="/philippines" class="country-link">Philippines</a>
  <a href="/poland" class="country-link">Poland</a>
  <a href="/portugal" class="country-link">Portugal</a>

  <a href="/qatar" class="country-link">Qatar</a>

  <a href="/romania" class="country-link">Romania</a>
  <a href="/russia" class="country-link">Russia</a>
  <a href="/rwanda" class="country-link">Rwanda</a>

  <a href="/saint-kitts-and-nevis" class="country-link">Saint Kitts and Nevis</a>
  <a href="/saint-lucia" class="country-link">Saint Lucia</a>
  <a href="/saint-vincent-and-the-grenadines" class="country-link">Saint Vincent and the Grenadines</a>
  <a href="/samoa" class="country-link">Samoa</a>
  <a href="/san-marino" class="country-link">San Marino</a>
  <a href="/sao-tome-and-principe" class="country-link">Sao Tome and Principe</a>
  <a href="/saudi-arabia" class="country-link">Saudi Arabia</a>
  <a href="/senegal" class="country-link">Senegal</a>
  <a href="/serbia" class="country-link">Serbia</a>
  <a href="/seychelles" class="country-link">Seychelles</a>
  <a href="/sierra-leone" class="country-link">Sierra Leone</a>
  <a href="/singapore" class="country-link">Singapore</a>
  <a href="/slovakia" class="country-link">Slovakia</a>
  <a href="/slovenia" class="country-link">Slovenia</a>
  <a href="/solomon-islands" class="country-link">Solomon Islands</a>
  <a href="/somalia" class="country-link">Somalia</a>
  <a href="/south-africa" class="country-link">South Africa</a>
  <a href="/south-sudan" class="country-link">South Sudan</a>
  <a href="/spain" class="country-link">Spain</a>
  <a href="/sri-lanka" class="country-link">Sri Lanka</a>
  <a href="/sudan" class="country-link">Sudan</a>
  <a href="/suriname" class="country-link">Suriname</a>
  <a href="/sweden" class="country-link">Sweden</a>
  <a href="/switzerland" class="country-link">Switzerland</a>
  <a href="/syria" class="country-link">Syria</a>

  <a href="/taiwan" class="country-link">Taiwan</a>
  <a href="/tajikistan" class="country-link">Tajikistan</a>
  <a href="/tanzania" class="country-link">Tanzania</a>
  <a href="/thailand" class="country-link">Thailand</a>
  <a href="/togo" class="country-link">Togo</a>
  <a href="/tonga" class="country-link">Tonga</a>
  <a href="/trinidad-and-tobago" class="country-link">Trinidad and Tobago</a>
  <a href="/tunisia" class="country-link">Tunisia</a>
  <a href="/turkey" class="country-link">Turkey</a>
  <a href="/turkmenistan" class="country-link">Turkmenistan</a>
  <a href="/tuvalu" class="country-link">Tuvalu</a>

  <a href="/uganda" class="country-link">Uganda</a>
  <a href="/ukraine" class="country-link">Ukraine</a>
  <a href="/united-arab-emirates" class="country-link">United Arab Emirates</a>
  <a href="/united-kingdom" class="country-link">United Kingdom</a>
  <a href="/united-states" class="country-link">United States</a>
  <a href="/uruguay" class="country-link">Uruguay</a>
  <a href="/uzbekistan" class="country-link">Uzbekistan</a>

  <a href="/vanuatu" class="country-link">Vanuatu</a>
  <a href="/vatican-city" class="country-link">Vatican City</a>
  <a href="/venezuela" class="country-link">Venezuela</a>
  <a href="/vietnam" class="country-link">Vietnam</a>

  <a href="/yemen" class="country-link">Yemen</a>

  <a href="/zambia" class="country-link">Zambia</a>
  <a href="/zimbabwe" class="country-link">Zimbabwe</a>
</div>
</main>

<!-- VIDEO_DATA_START -->
<script>
    window.embeddedVideoData = [];
</script>
<!-- VIDEO_DATA_END -->

  <div id="videoList" class="video-list"></div>
  <button id="loadMoreBtn" class="site-button">Load More</button>
 </div>
<section class="about-section">
  <button id="aboutToggle" class="site-button">About Us</button>
  <div id="aboutContent" style="display: none;">
<p><strong>What is TopTubeList?</strong><br>
    TopTubeList helps you quickly see what people are watching on YouTube. You can explore videos by continent or country. No clutter, no fancy talk. Just a clean snapshot of the most viewed videos — updated every 3 hours.</p>

    <p><strong>Why did we build this site?</strong><br>
    My wife was in the kitchen cooking. My mission was clear: to answer that sacred question… <em>“What should we watch while eating?”</em><br>
    Then suddenly, I found myself thinking: <em>“What do other couples watch during dinner?”</em> So, like anyone else, I turned to Google.</p>

    <p><strong>And what did I find?</strong><br>
    “Most watched videos in June”…<br>
    “Top videos of 2025”…<br>
    Basically, just a highlight reel of the past.<br>
    But I wasn’t looking for nostalgia — I wanted to know what’s trending <strong>right now</strong>.</p>

    <p>That day, we may not have found the perfect video to watch...<br>
    But I realized we weren’t alone.<br>
    There must be thousands of people wondering the exact same thing.<br>
    And that’s when the idea of TopTubeList was born.</p>

    <p><strong>And the cherry on top?</strong><br>
    For creators who make “compilation videos” using trending clips, this site is basically a goldmine.</p>

    <p><strong>How does it work?</strong><br>
    Every 3 hours, we pull the most popular videos using YouTube’s official Data API. Then we sort them by country and continent, so you can easily see what’s trending anywhere in the world.</p>

    <p><strong>This is TopTubeList.</strong><br>
    If it’s trending, chances are… we’ve already listed it. 😉</p>
  </div>
</section>

<!-- IFRAME_VIDEO_HERE -->
<!-- IFRAME_VIDEO_HERE_END -->
 
<footer>
  <div class="contact-section">
    <button id="contactToggle" class="site-button">Contact Us</button>
    <div id="contactContent" style="display: none;">
      <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="contact" />
        <p hidden><label>Don’t fill this out: <input name="bot-field" /></label></p>
        <p><label>Your Name<br /><input type="text" name="name" required /></label></p>
        <p><label>Your Email<br /><input type="email" name="email" required /></label></p>
        <p><label>Your Message<br /><textarea name="message" rows="5" required></textarea></label></p>
        <p><button type="submit">Send Message</button></p>
      </form>
      <div id="formStatus" style="display: none;"></div>
    </div>
  </div>
  <p>© 2025 TopTubeList.com</p>
</footer>
<script src="dynamic.js"></script>
</body>
</html>
"""

def generate_html_page(name, is_country=True, output_folder="."):
    print(f"\n🔨 {name} sayfası oluşturuluyor...")

    videos_file = f"{name}.vid.data.json"
    structured_file = f"{name}.str.data.json"

    videos_data = load_json_data(videos_file)
    structured_data = load_json_data(structured_file)

    html_content = generate_html_content(name, videos_data, structured_data)

    output_path = os.path.join(output_folder, f"{name}.html")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Oluşturuldu: {output_path}")
        return True
    except IOError as e:
        print(f"❌ Yazma hatası: {str(e)}")
        return False

def main():
    print("""
    #######################################
    # TopTubeList - Sayfa Oluşturucu
    # Tüm kıta ve ülke sayfaları oluşturuluyor...
    #######################################
    """)

    success_count = 0
    total_items = len(CONTINENT_INFO) + len(COUNTRY_INFO)

    # Kıtaları oluştur
    for continent_name in CONTINENT_INFO:
        if generate_html_page(continent_name, is_country=False, output_folder="."):
            success_count += 1

    # Ülkeleri oluştur
    for country_name in COUNTRY_INFO:
        if generate_html_page(country_name, is_country=True, output_folder="."):
            success_count += 1

    print(f"\n🏁 İşlem tamamlandı: {success_count}/{total_items} sayfa başarıyla oluşturuldu")

    if success_count < total_items:
        print("⚠️ Bazı sayfalar oluşturulamadı. Lütfen hata mesajlarını kontrol edin.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"\n💥 Kritik hata: {str(e)}")
