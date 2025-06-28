import time
import subprocess

URL = "https://toptubelist.com"

print("⏳ Waiting 30 seconds before SSL check...")
time.sleep(30)

try:
    result = subprocess.check_output(
        ["curl", "-I", URL],
        stderr=subprocess.STDOUT
    ).decode()

    if "200 OK" in result:
        print("✅ Site is live and SSL certificate is valid.")
    else:
        print("⚠️ Unexpected response:\n", result)

except subprocess.CalledProcessError as e:
    output = e.output.decode()
    if "CERT" in output or "SSL" in output or "common name" in output.lower():
        print("🚨 SSL certificate error detected:")
        print(output)
    else:
        print("❌ Unknown error occurred:")
        print(output)
