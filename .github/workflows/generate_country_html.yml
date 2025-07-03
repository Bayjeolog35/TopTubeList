name: Generate Country Data and HTML

on:
  push:
    branches:
      - main # main branch'ine push yapıldığında tetikle
  schedule:
    - cron: '0 */3 * * *' # Her 3 saatte bir tetikle (Örn: 03:00, 06:00, 09:00, ...)

jobs:
  update_content:
    runs-on: ubuntu-latest # İş akışını Ubuntu işletim sistemi üzerinde çalıştır

    permissions:
      contents: write # Dosyaları depoya geri yazma izni ver

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4 # Depo kodunu çek

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x' # En son Python 3 sürümünü kullan

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests # requests kütüphanesini yükle

    - name: Fetch YouTube Data (videos.json, structured_data.json)
      env:
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }} # GitHub Secret'tan API anahtarını ortam değişkeni olarak ayarla
      run: |
        python country_youtube_data.py
      # working-directory: ./ # Betiğin proje kök dizininde çalıştığından emin olun (Zaten varsayılan olarak kökte çalışır, gereksiz olabilir)

    - name: Generate Country HTML Pages
      run: |
        python generate_country_html.py
      # working-directory: ./ # Betiğin proje kök dizininde çalıştığından emin olun (Zaten varsayılan olarak kökte çalışır, gereksiz olabilir)

    - name: Commit and Push generated files
      run: |
        git config user.name "GitHub Actions Bot" # Git kullanıcı adını ayarla
        git config user.email "github-actions-bot@example.com" # Git e-posta adresini ayarla
        git add Country_data/ # Ülke verisi JSON dosyalarını ekle
        git add */index.html # Tüm ülke klasörlerindeki index.html dosyalarını ekle (örn: Turkey/index.html)
        git status # Hata ayıklama için git status çıktısını görmek faydalı olabilir
        if ! git diff --quiet --cached; then # --cached sadece stage edilmiş dosyaları kontrol eder
          git commit -m "feat: Automate country data and HTML generation [skip ci]" # Değişiklik varsa commit yap
          git push # Değişiklikleri push yap
        else
          echo "No changes to commit."
        fi
