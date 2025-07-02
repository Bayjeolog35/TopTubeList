name: Update Country Data Every 3 Hours

on:
  schedule:
    - cron: "0 */3 * * *"  # Her 3 saatte bir UTC
  workflow_dispatch:       # Manuel tetikleme seçeneği
  push:
    paths:
      - "Country_automation.py"
      - "country_data.py"

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Install dependencies
      run: pip install requests

    - name: Run country automation script
      env:
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
      run: python Country_automation.py

    - name: Commit updated data
      run: |
        git config user.name "github-actions"
        git config user.email "github-actions@github.com"
        git add Country_data/*
        git commit -m "Update country video and structured data [CI]" || echo "No changes to commit"
        git push
