import os

# ISO 3166-1 alpha-2 → Ülke adı eşleşmesi (boşluklar alt çizgiye dönüştürülmüş)
country_map = {
    "AF": "Afghanistan", "AL": "Albania", "DZ": "Algeria", "AD": "Andorra", "AO": "Angola",
    "AG": "Antigua_and_Barbuda", "AR": "Argentina", "AM": "Armenia", "AU": "Australia", "AT": "Austria",
    "AZ": "Azerbaijan", "BS": "Bahamas", "BH": "Bahrain", "BD": "Bangladesh", "BB": "Barbados",
    "BY": "Belarus", "BE": "Belgium", "BZ": "Belize", "BJ": "Benin", "BT": "Bhutan",
    "BO": "Bolivia", "BA": "Bosnia_and_Herzegovina", "BW": "Botswana", "BR": "Brazil", "BN": "Brunei",
    "BG": "Bulgaria", "BF": "Burkina_Faso", "BI": "Burundi", "KH": "Cambodia", "CM": "Cameroon",
    "CA": "Canada", "CV": "Cape_Verde", "CF": "Central_African_Republic", "TD": "Chad", "CL": "Chile",
    "CN": "China", "CO": "Colombia", "KM": "Comoros", "CD": "Congo_Democratic_Republic", "CG": "Congo_Republic",
    "CR": "Costa_Rica", "CI": "Cote_d'Ivoire", "HR": "Croatia", "CU": "Cuba", "CY": "Cyprus",
    "CZ": "Czech_Republic", "DK": "Denmark", "DJ": "Djibouti", "DM": "Dominica", "DO": "Dominican_Republic",
    "EC": "Ecuador", "EG": "Egypt", "SV": "El_Salvador", "GQ": "Equatorial_Guinea", "ER": "Eritrea",
    "EE": "Estonia", "ET": "Ethiopia", "FJ": "Fiji", "FI": "Finland", "FR": "France",
    "GA": "Gabon", "GM": "Gambia", "GE": "Georgia", "DE": "Germany", "GH": "Ghana",
    "GR": "Greece", "GD": "Grenada", "GT": "Guatemala", "GN": "Guinea", "GW": "Guinea_Bissau",
    "GY": "Guyana", "HT": "Haiti", "HN": "Honduras", "HU": "Hungary", "IS": "Iceland",
    "IN": "India", "ID": "Indonesia", "IR": "Iran", "IQ": "Iraq", "IE": "Ireland",
    "IL": "Israel", "IT": "Italy", "JM": "Jamaica", "JP": "Japan", "JO": "Jordan",
    "KZ": "Kazakhstan", "KE": "Kenya", "KI": "Kiribati", "KR": "South_Korea", "KW": "Kuwait",
    "KG": "Kyrgyzstan", "LA": "Laos", "LV": "Latvia", "LB": "Lebanon", "LS": "Lesotho",
    "LR": "Liberia", "LY": "Libya", "LI": "Liechtenstein", "LT": "Lithuania", "LU": "Luxembourg",
    "MG": "Madagascar", "MW": "Malawi", "MY": "Malaysia", "MV": "Maldives", "ML": "Mali",
    "MT": "Malta", "MH": "Marshall_Islands", "MR": "Mauritania", "MU": "Mauritius", "MX": "Mexico",
    "FM": "Micronesia", "MD": "Moldova", "MC": "Monaco", "MN": "Mongolia", "ME": "Montenegro",
    "MA": "Morocco", "MZ": "Mozambique", "MM": "Myanmar", "NA": "Namibia", "NR": "Nauru",
    "NP": "Nepal", "NL": "Netherlands", "NZ": "New_Zealand", "NI": "Nicaragua", "NE": "Niger",
    "NG": "Nigeria", "MK": "North_Macedonia", "NO": "Norway", "OM": "Oman", "PK": "Pakistan",
    "PW": "Palau", "PA": "Panama", "PG": "Papua_New_Guinea", "PY": "Paraguay", "PE": "Peru",
    "PH": "Philippines", "PL": "Poland", "PT": "Portugal", "QA": "Qatar", "RO": "Romania",
    "RU": "Russia", "RW": "Rwanda", "KN": "Saint_Kitts_and_Nevis", "LC": "Saint_Lucia", "VC": "Saint_Vincent_and_the_Grenadines",
    "WS": "Samoa", "SM": "San_Marino", "ST": "Sao_Tome_and_Principe", "SA": "Saudi_Arabia", "SN": "Senegal",
    "RS": "Serbia", "SC": "Seychelles", "SL": "Sierra_Leone", "SG": "Singapore", "SK": "Slovakia",
    "SI": "Slovenia", "SB": "Solomon_Islands", "SO": "Somalia", "ZA": "South_Africa", "SS": "South_Sudan",
    "ES": "Spain", "LK": "Sri_Lanka", "SD": "Sudan", "SR": "Suriname", "SZ": "Eswatini",
    "SE": "Sweden", "CH": "Switzerland", "SY": "Syria", "TW": "Taiwan", "TJ": "Tajikistan",
    "TZ": "Tanzania", "TH": "Thailand", "TL": "Timor_Leste", "TG": "Togo", "TO": "Tonga",
    "TT": "Trinidad_and_Tobago", "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan", "TV": "Tuvalu",
    "UG": "Uganda", "UA": "Ukraine", "AE": "United_Arab_Emirates", "GB": "United_Kingdom", "US": "United_States",
    "UY": "Uruguay", "UZ": "Uzbekistan", "VU": "Vanuatu", "VA": "Vatican_City", "VE": "Venezuela",
    "VN": "Vietnam", "YE": "Yemen", "ZM": "Zambia", "ZW": "Zimbabwe"
}

def rename_folders():
    for iso_code, country_name in country_map.items():
        if os.path.exists(iso_code) and os.path.isdir(iso_code):
            os.rename(iso_code, country_name)
            print(f"✅ {iso_code} → {country_name}")
        else:
            print(f"⚠️  {iso_code} klasörü bulunamadı.")

if __name__ == "__main__":
    rename_folders()
