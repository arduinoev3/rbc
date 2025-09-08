# Сборка и развёртывание

Развёртывание бота возможно несколькими способами: запуск в фоне на сервере, systemd-сервис или Docker.

## Развёртывание как systemd-сервис

В репозитории уже есть пример `bot.service`. Примерный порядок действий:

1. Скопируйте `bot.service` в `/etc/systemd/system/`.
2. Отредактируйте пути в `bot.service`, чтобы они указывали на виртуальное окружение и `bot.py`.
3. Запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl start bot.service
sudo systemctl status bot.service
```

## Docker (рекомендация)

Можно собрать лёгкий Docker-образ, чтобы запуск был изолированным. Примерный Dockerfile:

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
```

Сборка и запуск:

```bash
docker build -t rbc-bot .
docker run -d --name rbc-bot --restart unless-stopped rbc-bot
```

При использовании Docker не забудьте передавать `param.py` через секреты или переменные окружения и обеспечить безопасное хранение токена.
