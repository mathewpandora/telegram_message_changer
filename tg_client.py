import asyncio
import os
from xml.sax.saxutils import escape

from dotenv import load_dotenv
from telethon import TelegramClient, events
from giga_client import GigaChatTextCorrector
from logger_config import logger

load_dotenv()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

client = TelegramClient("sessions/my_session", API_ID, API_HASH)


def change_message(message: str) -> str:
    logger.info(f"Обработка сообщения: {message}")
    
    if not message or not message.strip():
        logger.info("Пустое сообщение, пропускаем обработку")
        return message
    
    if len(message.strip()) < 2:
        logger.info("Слишком короткое сообщение, пропускаем обработку")
        return message
    
    try:
        giga_client = GigaChatTextCorrector()
        response = giga_client.send_request(message)
        logger.info(f"Получен ответ от GigaChat: {response}")
        return response
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        return message


@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    original = event.raw_text
    logger.info(f"Получено исходящее сообщение: {original}")
    
    if not original or not original.strip():
        logger.info("Сообщение без текста (медиа-контент), пропускаем обработку")
        return
    
    try:
        modified = change_message(original)

        if modified != original:
            await event.delete()
            await client.send_message(event.chat_id, modified)
            logger.info(f"Сообщение заменено на: {modified}")
        else:
            logger.info("Сообщение не изменилось")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")


async def main():
    try:
        logger.info("Запуск Telegram клиента...")
        await client.start(phone=PHONE_NUMBER)
        logger.info("Клиент успешно запущен")
        print("Клиент запущен. Теперь все твои сообщения будут автоматически отправляться с точками 😎")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Ошибка при запуске клиента: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
