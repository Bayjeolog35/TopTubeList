@echo off
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Python ortamı kontrol ediliyor...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Python bulunamadi veya PATH'e eklenmedi.
    echo Lutfen Python'u kurun veya PATH'inize ekleyin.
    echo.
    pause
    exit /b 1
)

echo Gerekli kütüphaneler kontrol ediliyor ve yukleniyor...
pip install requests python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Gerekli kütüphaneler yüklenirken hata olustu.
    echo Internet baglantinizi kontrol edin veya manuel olarak yuklemeyi deneyin:
    echo     pip install requests python-dotenv
    echo.
    pause
    exit /b 1
)

echo.
echo YouTube veri cekme ve HTML guncelleme baslatiliyor...
python generate_youtube_data.py

if %errorlevel% equ 0 (
    echo.
    echo Islem basariyla tamamlandi!
) else (
    echo.
    echo Hata: generate_youtube_data.py betigi calisirken bir sorun olustu.
)

echo.
pause