import requests
from get_env import get_env

TELEGRAM_TOKEN, CHAT_ID_LIST = get_env()


def send_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    results = []
    for chat_id in CHAT_ID_LIST:
        resp = requests.post(
            url,
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
        result = resp.json()
        if not result.get("ok"):
            raise RuntimeError(f"Telegram error for {chat_id}: {result}")
        results.append(result.get('ok', False))
    return all(results)


if __name__ == "__main__":
    send_telegram("Telegram bot is running.")
