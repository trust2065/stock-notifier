import os
from dotenv import load_dotenv


def get_env() -> tuple[str, list[str]]:
    """Load and return the Telegram token and normalized chat IDs."""
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHANNEL_ID")
    if not telegram_token:
        raise EnvironmentError("Missing environment variable: TELEGRAM_TOKEN")
    if not chat_id:
        raise EnvironmentError("Missing environment variable: CHANNEL_ID")

    chat_id_list = [
        "@" + cid.split("t.me/")[-1].strip("/") if "t.me/" in cid else cid
        for cid in (item.strip() for item in chat_id.split(","))
        if cid
    ]
    return telegram_token, chat_id_list


# Example usage:
# telegram_token, chat_id_list = get_env()
