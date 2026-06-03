# XMPP Мессенджер

Корпоративный Jabber-клиент для Windows с GUI и REST API.

## Для чего

- Общение через корпоративный XMPP/Jabber сервер (OpenFire, Ejabberd и др.)
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

## REST API

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/send_message` | Отправить сообщение |
| GET | `/health` | Проверка доступности |
| GET | `/stats` | Статистика |
| GET | `/get_messages` | История сообщений |
| POST | `/broadcast` | Рассылка |

Пример отправки:

```bash
curl -X POST http://127.0.0.1:8080/send_message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d "{\"to\": \"user@domain\", \"message\": \"Привет\"}"
```
