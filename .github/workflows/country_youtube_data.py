name: Generate Country Data and HTML

on:
  push:
    branches:
      - main
  workflow_dispatch:
  schedule:
    - cron: '0 */3 * * *' # Her 3 saatte bir çalışır

jobs:
  update_content:
    runs-on: ubuntu-latest

    env:
      YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'

    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests

    - name: Fetch YouTube Data (videos.json, structured_data.json)
      run: |
        # country_youtube_data.py çalıştırılıyor
        python country_youtube_data.py

    - name: Generate Country HTML Files
      run: |
        python generate_country_html.py

    - name: Commit and Push generated files
      run: |
        git config user.name "GitHub Actions Bot"
        git config user.email "actions@github.github.com"

        # Oluşturulan veya güncellenen tüm .json ve .html dosyalarını ekle
        # Country_data klasörü altındaki tüm json dosyalarını ekle
        git add Country_data/**/*.json 
        # Ana dizin ve alt klasörlerdeki tüm html dosyalarını ekle (e.g., Turkey/index.html)
        git add **/*.html 
        
        git commit -m "feat: Automate country data and HTML generation" || echo "No changes to commit"
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
