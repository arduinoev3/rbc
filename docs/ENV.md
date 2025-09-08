# Переменные окружения и конфигурация

Текущая реализация использует локальный файл `param.py` для хранения секретов и параметров. Рекомендуемые переменные/поля:

- TELEGRAM_TOKEN — токен бота (альтернатива `param.py`)
- CHECK_NAME — имя канала/чата для проверки членства
- BACKUP_ID — chat_id для отправки резервной копии `data.csv`

Пример использования через переменные окружения (в `bot.py` можно заменить импорт `param` на чтение os.environ):

```python
import os
token = os.environ.get("TELEGRAM_TOKEN")
check_name = os.environ.get("CHECK_NAME")
backup_id = int(os.environ.get("BACKUP_ID", "5677083753"))
```

Для локальной разработки можно использовать файл `.env` и пакет `python-dotenv`.
