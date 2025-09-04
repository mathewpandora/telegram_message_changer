import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY не найден в .env файле")

        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_message(self, message: str, model: str = "deepseek-chat") -> str:
        """
        Отправляет сообщение в DeepSeek API и возвращает ответ

        Args:
            message: Текст сообщения
            model: Модель для использования (по умолчанию deepseek-chat)

        Returns:
            Ответ от нейросети
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            # Проверяем статус ответа
            response.raise_for_status()

            # Парсим JSON ответ
            result = response.json()

            # Извлекаем текст ответа
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return "Не удалось получить ответ от нейросети"

        except requests.exceptions.RequestException as e:
            return f"Ошибка сети: {e}"
        except json.JSONDecodeError as e:
            return f"Ошибка парсинга JSON: {e}"
        except KeyError as e:
            return f"Ошибка в структуре ответа: {e}"
        except Exception as e:
            return f"Неизвестная ошибка: {e}"


# Пример использования
def main():
    # Инициализируем клиент
    client = DeepSeekClient()

    # Тестовое сообщение
    test_message = "Привет! Напиши короткое стихотворение о программировании"

    # Отправляем запрос
    print("Отправляю запрос...")
    response = client.send_message(test_message)

    # Выводим результат
    print("\nЗапрос:", test_message)
    print("\nОтвет нейросети:")
    print(response)

    # Еще один пример
    print("\n" + "=" * 50)
    response2 = client.send_message("Объясни квантовые вычисления простыми словами")
    print("Второй ответ:")
    print(response2)


if __name__ == "__main__":
    main()