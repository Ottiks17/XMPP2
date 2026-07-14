# XMPP Мессенджер

Корпоративный Jabber-клиент для Windows с GUI и REST API.

## Для чего

- Общение через корпоративный XMPP/Jabber сервер (OpenFire)
- Отправка сообщений из внешних систем через REST API
- Статусы доставки и прочтения сообщений
- Автоматическое обновление клиента

## Возможности

- Подключение к XMPP серверу по TLS
- Чат с историей, статусами доставки (✓) и прочтения (✓✓)
- REST API для интеграции с внешними системами
- SQLite-логи сообщений
- Автообновление через GitHub Releases

## Установка

Скачать последний релиз: [Releases](../../releases/latest)

Распаковать архив и запустить `XMPPClient.exe`.

## Настройка

Заполнить `config/config.json`:

```json
{
  "xmpp": {
    "server": "192.168.1.1",
    "port": 5222,
    "username": "user@domain",
    "password": "password",
    "use_tls": true
  },
  "rest_api": {
    "host": "0.0.0.0",
    "port": 8080,
    "endpoint": "/send_message"
  }
}
```

Или через `.env` файл (приоритет над config.json):

```env
XMPP_SERVER=192.168.1.1
XMPP_USERNAME=user@domain
XMPP_PASSWORD=password
REST_API_KEY=your-secret-key
```

## REST API

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/send_message` | Отправить сообщение |
| GET | `/health` | Проверка доступности |
| GET | `/stats` | Статистика |
| GET | `/get_messages` | История сообщений |
| POST | `/broadcast` | Рассылка |

**Rate Limiting:** 100 запросов в минуту на IP

**Security Headers:** 
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security

Пример отправки:

```bash
curl -X POST http://127.0.0.1:8080/send_message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d "{\"to\": \"user@domain\", \"message\": \"Привет\"}"
```

## Kafka

Для интеграции Kafka включите настройки в `config/config.json`:

```json
"kafka": {
  "enabled": true,
  "bootstrap_servers": "localhost:9092",
  "topics": {
    "messages": "xmpp-messages",
    "api_requests": "xmpp-api-requests",
    "events": "xmpp-events"
  },
  "consumer_group": "xmpp-client",
  "use_for_api_queue": true,
  "consume_api_requests": true,
  "auto_offset_reset": "latest",
  "publish_all_messages": true,
  "publish_api_requests": true
}
```

Как работает Kafka в этом проекте:

- `use_for_api_queue`: если включено, REST API будет публиковать входящие `/send_message` запросы в Kafka топик `api_requests` вместо немедленной отправки по XMPP.
- `consume_api_requests`: если включено, сервис запускает consumer, который читает `api_requests` и вызывает XMPP отправку через внутренний message handler.
- При успешной отправке через REST API или consumer проект публикует событие в Kafka топик `messages`.

Пример использования:

1. Запустите Kafka и создайте топики `xmpp-api-requests` и `xmpp-messages`.
2. Включите `kafka.enabled` и `use_for_api_queue`.
3. Отправьте запрос на API `/send_message`.
4. Если consumer запущен, сообщение будет прочитано из Kafka и отправлено по XMPP.

## Запуск из исходников

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Тестирование

Запустить все тесты:

```bash
pytest tests/ -v
```

Запустить с покрытием кода:

```bash
pytest tests/ --cov=app --cov=. --cov-report=html
```

Тесты включают:

- **test_validation.py**: Валидация конфига и JID
- **test_config.py**: Загрузка конфигурации
- **test_storage.py**: SQLite сохранение сообщений
- **test_rest_api.py**: REST API endpoints (rate limiting, security)
- **test_kafka_consumer.py**: Kafka producer/consumer и retry logic

## Безопасность

- **Rate Limiting**: 100 req/min на IP адрес
- **API Key**: X-API-Key header требуется для POST запросов
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- **TLS/SSL**: Поддержка XMPP TLS соединений
- **Thread Safety**: Lock-based synchronization для shared state
- **Kafka Retry**: Экспоненциальная задержка (1, 2, 4 сек) при ошибках

## Production Deployment

Запуск с gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8080 rest_server:app
```

Или через Waitress (встроенный):

```bash
python -c "from rest_server import RESTServer; from app.config import Config; c=Config(); s=RESTServer(c.config); s.start()"
```

## Лицензия

MIT License
