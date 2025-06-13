import random
import ipaddress
import time
import os
import requests
from datetime import datetime

# === CONFIGURATION ===
RATE_PER_MINUTE = 1000
BATCH_SIZE = 50000
TELEGRAM_TOKEN = 'TON_BOT_TOKEN_ICI'
TELEGRAM_CHAT_ID = 'TON_CHAT_ID_ICI'

# === GÉNÉRATION D'IP PUBLIQUES VALABLES ===
def generate_valid_ip():
    while True:
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            if not ip_obj.is_private and not ip_obj.is_reserved and not ip_obj.is_loopback and not ip_obj.is_multicast:
                return ip
        except ipaddress.AddressValueError:
            continue

# === ENVOI TELEGRAM ===
def send_file_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        response = requests.post(url, files=files, data=data)
        return response.status_code == 200

# === BOUCLE PRINCIPALE ===
def main():
    delay = 60 / RATE_PER_MINUTE
    ip_list = []
    counter = 0

    while True:
        ip = generate_valid_ip()
        ip_list.append(ip)
        counter += 1
        time.sleep(delay)

        if counter >= BATCH_SIZE:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ip_list_{timestamp}.txt"
            with open(filename, "w") as f:
                f.write("\n".join(ip_list))

            success = send_file_to_telegram(filename)
            print(f"[+] Batch envoyé : {filename} - Succès : {success}")

            os.remove(filename)
            ip_list = []
            counter = 0

if __name__ == "__main__":
    main()
