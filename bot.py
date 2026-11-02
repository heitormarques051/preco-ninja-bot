import os
import json
import urllib.request

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHANNEL = os.environ["CHANNEL_USERNAME"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL,
    "text": "🥷 PREÇO NINJA\n\n🔥 Bot conectado com sucesso!\n⚡ O Ninja está online."
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

urllib.request.urlopen(request)

print("Mensagem enviada com sucesso!")
