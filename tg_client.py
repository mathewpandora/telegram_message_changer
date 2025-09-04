import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from giga_client import GigaChatTextCorrector

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

client = TelegramClient("my_session", API_ID, API_HASH)


def change_message(message: str) -> str:
    giga_client = GigaChatTextCorrector()
    response = giga_client.send_request(message)
    return response


@client.on(events.NewMessage(outgoing=True))  # ловим исходящие сообщения
async def handler(event):
    original = event.raw_text
    modified = change_message(original)

    if modified != original:
        await event.delete()
        await client.send_message(event.chat_id, modified)
        print(f"Сообщение заменено на: {modified}")


async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Клиент запущен. Теперь все твои сообщения будут автоматически отправляться с точками 😎")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
