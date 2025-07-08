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
    "north_america": {
        "name": "North America",
        "meta_description": "Viral YouTube content in USA, Canada and Mexico - Real-time trending videos"
    },
    "south_america": {
        "name": "South America",
        "meta_description": "Most watched YouTube videos in South American countries - Updated constantly"
    },
    "oceania": {
        "name": "Oceania",
        "meta_description": "Trending YouTube videos from Australia, New Zealand and Pacific Islands"
    },

    "worldwide": {
        "display_name": "Worldwide",
        "meta_description": "Trending YouTube videos globally - Most viewed content across all countries"
    }
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
                width="560" 
                height="315" 
                src="https://www.youtube.com/embed/{video_id}" 
                title="{title}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
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
    meta_description = info_dict.get(name, {}).get("meta_description", f"Trending YouTube videos in name - Updated every 3 hours")

    top_video_iframe = generate_top_video_iframe(videos_data)

    structured_block = ""
    if structured_data:
        structured_block = f'<script type="application/ld+json">\n{json.dumps(structured_data, indent=2)}\n</script>'

    current_date = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trending YouTube Videos in name | TopTubeList</title>
  <meta name="description" content="{meta_description}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://toptubelist.com/{name}.html">
  <link rel="stylesheet" href="style.css">
  {structured_block}
</head>
<body>
    <header>
        <div class="container">
            <a href="../../index.html" class="logo">
                <img src="TopTubeListLogo.webp" alt="TopTubeList" width="120">
            </a>
            <h1>Trending in {name}</h1>
        </div>
        

  <nav id="continentNav">
    <a href="index.html">Worldwide</a>
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
<button onclick="location.href='afghanistan.html'" data-letter="A">Afghanistan</button>
  <button onclick="location.href='albania.html'" data-letter="A">Albania</button>
  <button onclick="location.href='algeria.html'" data-letter="A">Algeria</button>
  <button onclick="location.href='andorra.html'" data-letter="A">Andorra</button>
  <button onclick="location.href='angola.html'" data-letter="A">Angola</button>
  <button onclick="location.href='antigua-and-barbuda.html'" data-letter="A">Antigua and Barbuda</button>
  <button onclick="location.href='argentina.html'" data-letter="A">Argentina</button>
  <button onclick="location.href='armenia.html'" data-letter="A">Armenia</button>
  <button onclick="location.href='australia.html'" data-letter="A">Australia</button>
  <button onclick="location.href='austria.html'" data-letter="A">Austria</button>
  <button onclick="location.href='azerbaijan.html'" data-letter="A">Azerbaijan</button>

  <button onclick="location.href='bahamas.html'" data-letter="B">Bahamas</button>
  <button onclick="location.href='bahrain.html'" data-letter="B">Bahrain</button>
  <button onclick="location.href='bangladesh.html'" data-letter="B">Bangladesh</button>
  <button onclick="location.href='barbados.html'" data-letter="B">Barbados</button>
  <button onclick="location.href='belarus.html'" data-letter="B">Belarus</button>
  <button onclick="location.href='belgium.html'" data-letter="B">Belgium</button>
  <button onclick="location.href='belize.html'" data-letter="B">Belize</button>
  <button onclick="location.href='benin.html'" data-letter="B">Benin</button>
  <button onclick="location.href='bhutan.html'" data-letter="B">Bhutan</button>
  <button onclick="location.href='bolivia.html'" data-letter="B">Bolivia</button>
  <button onclick="location.href='bosnia-and-herzegovina.html'" data-letter="B">Bosnia and Herzegovina</button>
  <button onclick="location.href='botswana.html'" data-letter="B">Botswana</button>
  <button onclick="location.href='brazil.html'" data-letter="B">Brazil</button>
  <button onclick="location.href='brunei.html'" data-letter="B">Brunei</button>
  <button onclick="location.href='bulgaria.html'" data-letter="B">Bulgaria</button>
  <button onclick="location.href='burkina-faso.html'" data-letter="B">Burkina Faso</button>
  <button onclick="location.href='burundi.html'" data-letter="B">Burundi</button>

  <button onclick="location.href='cabo-verde.html'" data-letter="C">Cabo Verde</button>
  <button onclick="location.href='cambodia.html'" data-letter="C">Cambodia</button>
  <button onclick="location.href='cameroon.html'" data-letter="C">Cameroon</button>
  <button onclick="location.href='canada.html'" data-letter="C">Canada</button>
  <button onclick="location.href='central-african-republic.html'" data-letter="C">Central African Republic</button>
  <button onclick="location.href='chad.html'" data-letter="C">Chad</button>
  <button onclick="location.href='chile.html'" data-letter="C">Chile</button>
  <button onclick="location.href='china.html'" data-letter="C">China</button>
  <button onclick="location.href='colombia.html'" data-letter="C">Colombia</button>
  <button onclick="location.href='comoros.html'" data-letter="C">Comoros</button>
  <button onclick="location.href='congo-democratic-republic-of-the.html'" data-letter="C">Congo (Democratic Republic of the)</button>
  <button onclick="location.href='congo-republic-of-the.html'" data-letter="C">Congo (Republic of the)</button>
  <button onclick="location.href='costa-rica.html'" data-letter="C">Costa Rica</button>
  <button onclick="location.href='cote-d-ivoire.html'" data-letter="C">Cote d'Ivoire</button>
  <button onclick="location.href='croatia.html'" data-letter="C">Croatia</button>
  <button onclick="location.href='cuba.html'" data-letter="C">Cuba</button>
  <button onclick="location.href='cyprus.html'" data-letter="C">Cyprus</button>
  <button onclick="location.href='czech-republic.html'" data-letter="C">Czech Republic</button>

  <button onclick="location.href='denmark.html'" data-letter="D">Denmark</button>
  <button onclick="location.href='djibouti.html'" data-letter="D">Djibouti</button>
  <button onclick="location.href='dominica.html'" data-letter="D">Dominica</button>
  <button onclick="location.href='dominican-republic.html'" data-letter="D">Dominican Republic</button>

  <button onclick="location.href='east-timor.html'" data-letter="E">East Timor</button>
  <button onclick="location.href='ecuador.html'" data-letter="E">Ecuador</button>
  <button onclick="location.href='egypt.html'" data-letter="E">Egypt</button>
  <button onclick="location.href='el-salvador.html'" data-letter="E">El Salvador</button>
  <button onclick="location.href='equatorial-guinea.html'" data-letter="E">Equatorial Guinea</button>
  <button onclick="location.href='eritrea.html'" data-letter="E">Eritrea</button>
  <button onclick="location.href='estonia.html'" data-letter="E">Estonia</button>
  <button onclick="location.href='eswatini.html'" data-letter="E">Eswatini</button>
  <button onclick="location.href='ethiopia.html'" data-letter="E">Ethiopia</button>

  <button onclick="location.href='fiji.html'" data-letter="F">Fiji</button>
  <button onclick="location.href='finland.html'" data-letter="F">Finland</button>
  <button onclick="location.href='france.html'" data-letter="F">France</button>

  <button onclick="location.href='gabon.html'" data-letter="G">Gabon</button>
  <button onclick="location.href='gambia.html'" data-letter="G">Gambia</button>
  <button onclick="location.href='georgia.html'" data-letter="G">Georgia</button>
  <button onclick="location.href='germany.html'" data-letter="G">Germany</button>
  <button onclick="location.href='ghana.html'" data-letter="G">Ghana</button>
  <button onclick="location.href='greece.html'" data-letter="G">Greece</button>
  <button onclick="location.href='grenada.html'" data-letter="G">Grenada</button>
  <button onclick="location.href='guatemala.html'" data-letter="G">Guatemala</button>
  <button onclick="location.href='guinea.html'" data-letter="G">Guinea</button>
  <button onclick="location.href='guinea-bissau.html'" data-letter="G">Guinea-Bissau</button>
  <button onclick="location.href='guyana.html'" data-letter="G">Guyana</button>

  <button onclick="location.href='haiti.html'" data-letter="H">Haiti</button>
  <button onclick="location.href='honduras.html'" data-letter="H">Honduras</button>
  <button onclick="location.href='hungary.html'" data-letter="H">Hungary</button>

  <button onclick="location.href='iceland.html'" data-letter="I">Iceland</button>
  <button onclick="location.href='india.html'" data-letter="I">India</button>
  <button onclick="location.href='indonesia.html'" data-letter="I">Indonesia</button>
  <button onclick="location.href='iran.html'" data-letter="I">Iran</button>
  <button onclick="location.href='iraq.html'" data-letter="I">Iraq</button>
  <button onclick="location.href='ireland.html'" data-letter="I">Ireland</button>
  <button onclick="location.href='israel.html'" data-letter="I">Israel</button>
  <button onclick="location.href='italy.html'" data-letter="I">Italy</button>

  <button onclick="location.href='jamaica.html'" data-letter="J">Jamaica</button>
  <button onclick="location.href='japan.html'" data-letter="J">Japan</button>
  <button onclick="location.href='jordan.html'" data-letter="J">Jordan</button>

  <button onclick="location.href='kazakhstan.html'" data-letter="K">Kazakhstan</button>
  <button onclick="location.href='kenya.html'" data-letter="K">Kenya</button>
  <button onclick="location.href='kiribati.html'" data-letter="K">Kiribati</button>
  <button onclick="location.href='korea-north.html'" data-letter="K">Korea (North)</button>
  <button onclick="location.href='korea-south.html'" data-letter="K">Korea (South)</button>
  <button onclick="location.href='kosovo.html'" data-letter="K">Kosovo</button>
  <button onclick="location.href='kuwait.html'" data-letter="K">Kuwait</button>
  <button onclick="location.href='kyrgyzstan.html'" data-letter="K">Kyrgyzstan</button>

  <button onclick="location.href='laos.html'" data-letter="L">Laos</button>
  <button onclick="location.href='latvia.html'" data-letter="L">Latvia</button>
  <button onclick="location.href='lebanon.html'" data-letter="L">Lebanon</button>
  <button onclick="location.href='lesotho.html'" data-letter="L">Lesotho</button>
  <button onclick="location.href='liberia.html'" data-letter="L">Liberia</button>
  <button onclick="location.href='libya.html'" data-letter="L">Libya</button>
  <button onclick="location.href='liechtenstein.html'" data-letter="L">Liechtenstein</button>
  <button onclick="location.href='lithuania.html'" data-letter="L">Lithuania</button>
  <button onclick="location.href='luxembourg.html'" data-letter="L">Luxembourg</button>

  <button onclick="location.href='madagascar.html'" data-letter="M">Madagascar</button>
  <button onclick="location.href='malawi.html'" data-letter="M">Malawi</button>
  <button onclick="location.href='malaysia.html'" data-letter="M">Malaysia</button>
  <button onclick="location.href='maldives.html'" data-letter="M">Maldives</button>
  <button onclick="location.href='mali.html'" data-letter="M">Mali</button>
  <button onclick="location.href='malta.html'" data-letter="M">Malta</button>
  <button onclick="location.href='marshall-islands.html'" data-letter="M">Marshall Islands</button>
  <button onclick="location.href='mauritania.html'" data-letter="M">Mauritania</button>
  <button onclick="location.href='mauritius.html'" data-letter="M">Mauritius</button>
  <button onclick="location.href='mexico.html'" data-letter="M">Mexico</button>
  <button onclick="location.href='micronesia.html'" data-letter="M">Micronesia</button>
  <button onclick="location.href='moldova.html'" data-letter="M">Moldova</button>
  <button onclick="location.href='monaco.html'" data-letter="M">Monaco</button>
  <button onclick="location.href='mongolia.html'" data-letter="M">Mongolia</button>
  <button onclick="location.href='montenegro.html'" data-letter="M">Montenegro</button>
  <button onclick="location.href='morocco.html'" data-letter="M">Morocco</button>
  <button onclick="location.href='mozambique.html'" data-letter="M">Mozambique</button>
  <button onclick="location.href='myanmar.html'" data-letter="M">Myanmar</button>

  <button onclick="location.href='namibia.html'" data-letter="N">Namibia</button>
  <button onclick="location.href='nauru.html'" data-letter="N">Nauru</button>
  <button onclick="location.href='nepal.html'" data-letter="N">Nepal</button>
  <button onclick="location.href='netherlands.html'" data-letter="N">Netherlands</button>
  <button onclick="location.href='new-zealand.html'" data-letter="N">New Zealand</button>
  <button onclick="location.href='nicaragua.html'" data-letter="N">Nicaragua</button>
  <button onclick="location.href='niger.html'" data-letter="N">Niger</button>
  <button onclick="location.href='nigeria.html'" data-letter="N">Nigeria</button>
  <button onclick="location.href='north-macedonia.html'" data-letter="N">North Macedonia</button>
  <button onclick="location.href='norway.html'" data-letter="N">Norway</button>

  <button onclick="location.href='oman.html'" data-letter="O">Oman</button>

  <button onclick="location.href='pakistan.html'" data-letter="P">Pakistan</button>
  <button onclick="location.href='palau.html'" data-letter="P">Palau</button>
  <button onclick="location.href='palestine.html'" data-letter="P">Palestine</button>
  <button onclick="location.href='panama.html'" data-letter="P">Panama</button>
  <button onclick="location.href='papua-new-guinea.html'" data-letter="P">Papua New Guinea</button>
  <button onclick="location.href='paraguay.html'" data-letter="P">Paraguay</button>
  <button onclick="location.href='peru.html'" data-letter="P">Peru</button>
  <button onclick="location.href='philippines.html'" data-letter="P">Philippines</button>
  <button onclick="location.href='poland.html'" data-letter="P">Poland</button>
  <button onclick="location.href='portugal.html'" data-letter="P">Portugal</button>

  <button onclick="location.href='qatar.html'" data-letter="Q">Qatar</button>

  <button onclick="location.href='romania.html'" data-letter="R">Romania</button>
  <button onclick="location.href='russia.html'" data-letter="R">Russia</button>
  <button onclick="location.href='rwanda.html'" data-letter="R">Rwanda</button>

  <button onclick="location.href='saint-kitts-and-nevis.html'" data-letter="S">Saint Kitts and Nevis</button>
  <button onclick="location.href='saint-lucia.html'" data-letter="S">Saint Lucia</button>
  <button onclick="location.href='saint-vincent-and-the-grenadines.html'" data-letter="S">Saint Vincent and the Grenadines</button>
  <button onclick="location.href='samoa.html'" data-letter="S">Samoa</button>
  <button onclick="location.href='san-marino.html'" data-letter="S">San Marino</button>
  <button onclick="location.href='sao-tome-and-principe.html'" data-letter="S">Sao Tome and Principe</button>
  <button onclick="location.href='saudi-arabia.html'" data-letter="S">Saudi Arabia</button>
  <button onclick="location.href='senegal.html'" data-letter="S">Senegal</button>
  <button onclick="location.href='serbia.html'" data-letter="S">Serbia</button>
  <button onclick="location.href='seychelles.html'" data-letter="S">Seychelles</button>
  <button onclick="location.href='sierra-leone.html'" data-letter="S">Sierra Leone</button>
  <button onclick="location.href='singapore.html'" data-letter="S">Singapore</button>
  <button onclick="location.href='slovakia.html'" data-letter="S">Slovakia</button>
  <button onclick="location.href='slovenia.html'" data-letter="S">Slovenia</button>
  <button onclick="location.href='solomon-islands.html'" data-letter="S">Solomon Islands</button>
  <button onclick="location.href='somalia.html'" data-letter="S">Somalia</button>
  <button onclick="location.href='south-africa.html'" data-letter="S">South Africa</button>
  <button onclick="location.href='south-sudan.html'" data-letter="S">South Sudan</button>
  <button onclick="location.href='spain.html'" data-letter="S">Spain</button>
  <button onclick="location.href='sri-lanka.html'" data-letter="S">Sri Lanka</button>
  <button onclick="location.href='sudan.html'" data-letter="S">Sudan</button>
  <button onclick="location.href='suriname.html'" data-letter="S">Suriname</button>
  <button onclick="location.href='sweden.html'" data-letter="S">Sweden</button>
  <button onclick="location.href='switzerland.html'" data-letter="S">Switzerland</button>
  <button onclick="location.href='syria.html'" data-letter="S">Syria</button>

  <button onclick="location.href='taiwan.html'" data-letter="T">Taiwan</button>
  <button onclick="location.href='tajikistan.html'" data-letter="T">Tajikistan</button>
  <button onclick="location.href='tanzania.html'" data-letter="T">Tanzania</button>
  <button onclick="location.href='thailand.html'" data-letter="T">Thailand</button>
  <button onclick="location.href='togo.html'" data-letter="T">Togo</button>
  <button onclick="location.href='tonga.html'" data-letter="T">Tonga</button>
  <button onclick="location.href='trinidad-and-tobago.html'" data-letter="T">Trinidad and Tobago</button>
  <button onclick="location.href='tunisia.html'" data-letter="T">Tunisia</button>
  <button onclick="location.href='turkey.html'" data-letter="T">Turkey</button>
  <button onclick="location.href='turkmenistan.html'" data-letter="T">Turkmenistan</button>
  <button onclick="location.href='tuvalu.html'" data-letter="T">Tuvalu</button>

  <button onclick="location.href='uganda.html'" data-letter="U">Uganda</button>
  <button onclick="location.href='ukraine.html'" data-letter="U">Ukraine</button>
  <button onclick="location.href='united-arab-emirates.html'" data-letter="U">United Arab Emirates</button>
  <button onclick="location.href='united-kingdom.html'" data-letter="U">United Kingdom</button>
  <button onclick="location.href='united-states.html'" data-letter="U">United States</button>
  <button onclick="location.href='uruguay.html'" data-letter="U">Uruguay</button>
  <button onclick="location.href='uzbekistan.html'" data-letter="U">Uzbekistan</button>

  <button onclick="location.href='vanuatu.html'" data-letter="V">Vanuatu</button>
  <button onclick="location.href='vatican-city.html'" data-letter="V">Vatican City</button>
  <button onclick="location.href='venezuela.html'" data-letter="V">Venezuela</button>
  <button onclick="location.href='vietnam.html'" data-letter="V">Vietnam</button>

  <button onclick="location.href='yemen.html'" data-letter="Y">Yemen</button>

  <button onclick="location.href='zambia.html'" data-letter="Z">Zambia</button>
  <button onclick="location.href='zimbabwe.html'" data-letter="Z">Zimbabwe</button>
  </div> 
  <div id="videoList" class="video-list"></div>
  <button id="loadMoreBtn" class="site-button">Load More</button>
 </div>

</main>
{top_video_iframe}
<section class="about-section">
  <button id="aboutToggle" class="site-button">About Us</button>
  <div id="aboutContent" style="display: none;">
<p><strong>Who are we?</strong><br>
  Welcome to <strong>TopTubeList</strong> — the home of global <strong>YouTube video rankings</strong>. We're a data-driven platform created for trend-seekers, content creators, marketers, and everyday fans who want to know exactly what’s trending on YouTube — country by country, continent by continent. Our mission is to provide open and accurate access to the <strong>most viewed YouTube videos</strong> from every corner of the world.</p>

  <p><strong>Why does this matter?</strong><br>
  In the digital age, YouTube is more than entertainment — it’s culture. It shapes opinions, sparks conversations, and launches careers. Whether it's a viral short, an explosive music video, or a game-changing documentary, millions turn to YouTube every day. By tracking the <strong>top trending YouTube videos</strong>, we give you a real-time pulse on what people are watching — not just locally, but globally.</p>

  <p><strong>How does it work?</strong><br>
  Using the official <strong>YouTube Data API</strong>, we monitor and update statistics for the most-watched videos in over 190 countries and across all continents. Every <strong>3 hours</strong>, our system fetches fresh data — no manual updates, no guesswork. This ensures that you're always seeing the most accurate and up-to-date information. We categorize and sort content so you can explore the most popular YouTube videos by region, discover regional trends, and see how global content performs across borders.</p>

  <p><strong>Who is this for?</strong><br>
  Whether you're a digital marketer analyzing trends, a creator seeking inspiration, or just a curious browser, TopTubeList gives you an easy way to discover what’s hot on YouTube <em>right now</em>. We provide a clean, ad-light experience with no paywalls, no accounts required, and no fluff — just pure insights.</p>

  <p><strong>What makes us different?</strong><br>
  Unlike generic trend charts, we focus on clarity, speed, and geographical accuracy. Our lists are updated frequently, and we don’t limit ourselves to just one country or genre. From <strong>North America</strong> to <strong>Asia</strong>, from viral <strong>YouTube Shorts</strong> to high-budget movie trailers, we showcase what the world is watching — all in one place.</p>

  <p><strong>How can you help?</strong><br>
  We’re not asking for donations. But if you find our platform valuable, consider sharing it with others. Every visit, link, and mention helps us grow — and keeps the platform free and open to everyone. Supporting TopTubeList means supporting transparency in digital culture.</p>

  <p><strong>What’s next?</strong><br>
  In the near future, we’ll be adding features like historical trend charts, creator spotlight pages, and region-based comparison tools. Our goal is to become the go-to archive for <strong>YouTube trends</strong> — from breakout hits to long-term legends.</p>

  <p><strong>Trending. Refreshed. Tracked.</strong><br>
  That’s TopTubeList. Stay curious. Stay informed.</p>

    </p>
  </div>
</section>

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
return html_start + script_block
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


def generate_index_from_worldwide():
    src = "worldwide.html"
    dst = "index.html"
    if os.path.exists(src):
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
        with open(dst, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ index.html, worldwide.html'den üretildi.")
    else:
        print("❌ worldwide.html bulunamadı, index.html üretilemedi.")


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

    # ✅ En son index.html üretilsin
    generate_index_from_worldwide()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"\n💥 Kritik hata: {str(e)}")
