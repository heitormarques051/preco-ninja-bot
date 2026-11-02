import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHANNEL = os.environ["CHANNEL_USERNAME"]
OFFERS_FILE = Path("ofertas.json")


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": CHANNEL, "text": text, "disable_web_page_preview": "false"}).encode()
    request = urllib.request.Request(url, data=payload, method="POST")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def main():
    if not OFFERS_FILE.exists():
        raise SystemExit("Crie ofertas.json antes de executar.")
    offers = json.loads(OFFERS_FILE.read_text(encoding="utf-8"))
    if not isinstance(offers, list):
        raise SystemExit("ofertas.json deve conter uma lista.")
    sent = 0
    for offer in offers:
        if offer.get("publicada", False):
            continue
        title = str(offer.get("produto", "")).strip()
        price = str(offer.get("preco", "")).strip()
        link = str(offer.get("link_afiliado", "")).strip()
        if not title or not price or not link.startswith("https://"):
            print("Oferta incompleta ignorada.")
            continue
        text = f"🥷 PREÇO NINJA | OFERTA\n\n🔥 {title}\n💰 Preço anunciado: {price}\n\n🛒 {link}\n\n🔗 Link de afiliado. Preço sujeito a alteração."
        send_message(text)
        offer["publicada"] = True
        OFFERS_FILE.write_text(json.dumps(offers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sent += 1
    print(f"Ofertas publicadas: {sent}")


if __name__ == "__main__":
    main()
