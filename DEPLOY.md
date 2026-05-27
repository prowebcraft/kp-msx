# Деплой kp-msx (Docker Compose + GitHub Actions)

Сборка образа идёт в GitHub Actions, образ публикуется в GHCR
(`ghcr.io/<owner>/kp-msx`), затем по SSH на сервере выполняется
`docker compose pull && up -d`. Состояние хранится в MongoDB
(контейнер `mongo` с volume `mongo-data`).

Примечание: имя образа в GHCR должно быть в нижнем регистре. Если владелец
репозитория содержит заглавные буквы, замените `${{ github.repository }}`
на нижний регистр в `.github/workflows/deploy.yml` и `APP_IMAGE`.

## 1. Подготовка сервера (один раз)

1. Установить Docker и compose plugin:
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```
2. Создать каталог проекта:
   ```bash
   sudo mkdir -p /opt/docker/kp-msx && sudo chown "$USER" /opt/docker/kp-msx
   ```
3. Создать в `/opt/docker/kp-msx` файл `.env` (сам `docker-compose.yml`
   доставляется автоматически в процессе деплоя):
   ```bash
   cp .env.example /opt/docker/kp-msx/.env
   ```
   Заполнить в `.env`:
   - `MSX_HOST=http://<IP_или_домен>:<HOST_PORT>` — внешний адрес сервера (критично).
   - `HOST_PORT` — публикуемый порт (например `1234`).
   - `MONGO_INITDB_ROOT_USERNAME` / `MONGO_INITDB_ROOT_PASSWORD` — креды Mongo.
   - `MONGODB_URL=mongodb://<user>:<pass>@mongo:27017/?authSource=admin`.
   - `APP_IMAGE=ghcr.io/<owner>/kp-msx:latest`.
4. Создать SSH-ключ для CI и добавить публичную часть в `~/.ssh/authorized_keys`
   deploy-пользователя:
   ```bash
   ssh-keygen -t ed25519 -f kp-msx-deploy -N ""
   ```
5. Открыть порт `HOST_PORT` в фаерволе.

## 2. Настройка GitHub (один раз)

В **Settings → Secrets and variables → Actions** добавить:

| Secret | Значение |
|--------|----------|
| `SSH_HOST` | IP/домен сервера |
| `SSH_USER` | deploy-пользователь |
| `SSH_KEY` | приватный ключ (`kp-msx-deploy`) |
| `SSH_PORT` | порт SSH (опционально, по умолчанию 22) |
| `GHCR_PAT` | PAT с областью `read:packages` — для `docker login` на сервере |

`GHCR_PAT` нужен, так как образ по умолчанию приватный. Альтернатива: сделать
пакет публичным (страница пакета → Package settings → Change visibility) и
убрать строку `docker login` из workflow.

В **Settings → Actions → General → Workflow permissions** включить
**Read and write permissions** (для push в GHCR через `GITHUB_TOKEN`).

## 3. Публикация

1. `git push` в ветку `master` (или вручную — **Actions → Build and Deploy → Run workflow**).
2. Workflow соберёт образ, запушит в GHCR и по SSH выполнит на сервере
   `docker compose pull && docker compose up -d`.
3. Проверка:
   ```bash
   curl http://<MSX_HOST>/msx/start.json
   ```
   и на сервере: `docker compose ps`, `docker compose logs app`.

## 4. Локальный запуск для проверки

```bash
cp .env.example .env   # заполнить значения
docker compose up --build
# открыть http://localhost:1234/msx/start.json
```
