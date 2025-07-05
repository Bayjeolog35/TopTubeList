# ... yukarıdaki kod aynı kalıyor

def deduplicate(videos):
    seen = set()
    unique = []
    for v in videos:
        vid = v["id"]
        if vid not in seen:
            seen.add(vid)
            unique.append(v)
    return unique

# main içinde güncellemeler:
def main():
    from country_info import COUNTRY_INFO
    from collections import defaultdict

    CONTINENT_GROUPS = defaultdict(list)
    for country_name, info in COUNTRY_INFO.items():
        continent = info.get("continent")
        if continent:
            CONTINENT_GROUPS[continent].append(country_name)

    videos_by_country = {}

    # Ülke verilerini çek
    for country, info in COUNTRY_INFO.items():
        code = info["code"]
        print(f"İşleniyor: {country} ({code})")
        data = get_trending_videos(code)
        if not data or 'items' not in data:
            print(f"Veri yok: {country}")
            continue
        videos = [process_video_data(item) for item in data["items"]]
        videos = deduplicate(videos)
        videos_by_country[country] = videos
        save_json(country, videos)

    # Kıtasal veriler
    for continent, country_list in CONTINENT_GROUPS.items():
        continent_videos = []
        for country in country_list:
            continent_videos.extend(videos_by_country.get(country, []))
        continent_videos = deduplicate(continent_videos)
        continent_videos.sort(key=lambda x: x["views"], reverse=True)
        save_json(continent, continent_videos[:50])

    # Dünya geneli
    all_videos = []
    for vids in videos_by_country.values():
        all_videos.extend(vids)
    all_videos = deduplicate(all_videos)
    all_videos.sort(key=lambda x: x["views"], reverse=True)
    save_json("worldwide", all_videos[:50])

if __name__ == "__main__":
    main()
