import ssl
import socket
import datetime

def check_ssl_expiry(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_date_str = cert['notAfter']
            expire_date = datetime.datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
            days_left = (expire_date - datetime.datetime.utcnow()).days
            return expire_date.strftime("%Y-%m-%d"), days_left

if __name__ == "__main__":
    domain = "toptubelist.com"  # kendi domaininle değiştir
    try:
        expire_date, days_left = check_ssl_expiry(domain)
        status = f"✅ SSL sertifikası geçerli.\n📅 Bitiş tarihi: {expire_date}\n⏳ Kalan gün: {days_left} gün"
    except Exception as e:
        status = f"❌ SSL kontrolü başarısız oldu.\nHata: {str(e)}"

    with open("reports/ssl_output.txt", "w") as f:
        f.write(status + "\n🕒 Güncelleme zamanı: " + datetime.datetime.now().isoformat())
