# Telegram Service

Сервис для автоматической коррекции текста в Telegram сообщениях с использованием GigaChat.

## Возможности

- Автоматическая коррекция исходящих сообщений в Telegram
- Использование GigaChat для исправления грамматических ошибок
- Логирование всех операций
- Docker контейнеризация

## Требования

- Docker и Docker Compose
- Telegram API ключи (API_ID, API_HASH)
- Номер телефона для авторизации
- GigaChat API ключ

## Настройка

1. Создайте файл `.env` в корне проекта:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE_NUMBER=your_phone_number
GIGACHAT_AUTH_KEY=your_gigachat_auth_key
```

2. Получите Telegram API ключи:
   - Перейдите на https://my.telegram.org
   - Войдите в аккаунт
   - Создайте новое приложение
   - Скопируйте API_ID и API_HASH

3. Получите GigaChat API ключ:
   - Зарегистрируйтесь на https://developers.sber.ru/
   - Создайте проект и получите ключ авторизации

## Запуск

### С помощью Docker Compose (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### С помощью Docker

```bash
# Сборка образа
docker build -t telegram-service .

# Запуск контейнера
docker run -d \
  --name telegram-service \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/my_session.session:/app/my_session.session \
  -v $(pwd)/session.session:/app/session.session \
  telegram-service
```

## Структура проекта

```
telegram_service/
├── tg_client.py          # Основной клиент Telegram
├── giga_client.py        # Клиент GigaChat
├── logger_config.py      # Конфигурация логгера
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose конфигурация
├── requirements.txt      # Python зависимости
├── .env                  # Переменные окружения (создать)
└── logs/                 # Папка с логами
```

## Логи

Логи сохраняются в папке `logs/` и включают:
- Информацию о запуске/остановке сервиса
- Обработку сообщений
- Ошибки и исключения
- Взаимодействие с GigaChat

## Управление контейнером

```bash
# Просмотр статуса
docker-compose ps

# Перезапуск сервиса
docker-compose restart

# Обновление и перезапуск
docker-compose up --build -d

# Просмотр логов в реальном времени
docker-compose logs -f telegram-service

# Вход в контейнер
docker-compose exec telegram-service bash
```

## Безопасность

- Никогда не коммитьте файл `.env` в репозиторий
- Файлы сессий Telegram содержат конфиденциальную информацию
- Регулярно обновляйте зависимости

## Устранение неполадок

1. **Ошибка авторизации Telegram**: Проверьте правильность API_ID, API_HASH и номера телефона
2. **Ошибка GigaChat**: Убедитесь, что API ключ действителен
3. **Проблемы с Docker**: Проверьте, что Docker запущен и доступен
4. **Логи**: Проверьте логи в папке `logs/` для диагностики проблем
