# XMPP Messaging Client

Профессиональный клиент Jabber (XMPP) для Windows: GUI на PyQt5, надёжный протокол на **slixmpp**, REST API на Flask + Waitress.

## Возможности

- Подключение к XMPP (TLS, опциональная проверка сертификата)
- Чат с историей, статусами доставки и прочтения
- REST API для внешних систем (POST, API-ключ)
- SQLite-логи, экспорт JSON, автоочистка
- In-band регистрация пользователей (если сервер поддерживает)
- Переменные окружения (`.env`) для секретов

## Быстрый старт

```bat
run.bat
```

Или вручную:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Конфигурация

Скопируйте `config/config.example.json` → `config/config.json` и заполните поля.

Опционально создайте `.env` (см. `.env.example`):

```env
XMPP_PASSWORD=secret
REST_API_KEY=long-random-key
```

Приоритет: `.env` → `config.json` → значения по умолчанию.

## REST API

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/send_message` | Отправить сообщение |
| GET | `/health` | Проверка (без ключа) |
| GET | `/stats` | Статистика (с ключом) |
| GET | `/get_messages` | История (с ключом) |
| POST | `/broadcast` | Рассылка (с ключом) |

Пример:

```bash
curl -X POST http://127.0.0.1:8080/send_message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d "{\"to\": \"user@domain\", \"message\": \"Привет\"}"
```

По умолчанию **GET для отправки отключён** (`allow_get: false`).

Документация: `http://127.0.0.1:8080/apidocs`

## Тесты

```bat
venv\Scripts\activate
pytest -q
```

## Структура проекта

```
app/
  config.py       # загрузка конфигурации
  storage.py      # SQLite логгер
  validation.py   # валидация JID и сообщений
  xmpp/
    service.py    # slixmpp-клиент
gui_app.py        # PyQt интерфейс
rest_server.py    # REST API
main.py           # точка входа
tests/            # автотесты
```

## Безопасность

- Используйте `api_key` при доступе из сети
- Не храните пароли в git (`config.json` в `.gitignore`)
- Предпочтительно: пароль только в `.env`
- `verify_tls: true` для продакшена с валидным сертификатом

## Логи

- `logs/app.log` — текст
- `logs/messages.db` — SQLite
- `logs/chat_history.json` — чаты GUI
