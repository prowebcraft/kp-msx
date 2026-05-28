# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Что это

Сервер-прокси на FastAPI между телевизором (Media Station X / MSX) и API кинопаба (`https://api.service-kp.com/v1`). Сервер запрашивает данные у кинопаба и преобразует их в нативный JSON-формат MSX. Смысл — вынести общение с кинопабом туда, где он не заблокирован, и отдавать переработанные данные в MSX по заведомо рабочему каналу телевизор↔сервер.

## Запуск

```bash
python3.12 -m venv venv
./venv/bin/pip install -r requirements.txt
# Прод/локально через uvicorn (порт указывается отдельно):
MONGODB_URL="..." MSX_HOST="http://IP:1234" ./venv/bin/uvicorn --host 0.0.0.0 --port 1234 api:app
# Либо напрямую (берёт config.PORT, по умолчанию 10000):
MONGODB_URL="..." MSX_HOST="..." python api.py
```

Проверка: `http://{HOST}/msx/start.json` должен отвечать. Тестов и линтера в репозитории нет.

### Локально в Docker

```bash
cp .env.example .env        # заполнить MSX_HOST, креды Mongo, MONGODB_URL
docker compose up --build   # поднимет app + mongo
```

Compose состоит из двух файлов: `docker-compose.yml` (используется и на сервере — только `image:` из GHCR + сервис `mongo:7` с volume `mongo-data`) и `docker-compose.override.yml` (только локально, добавляет `build: .`). На сервер копируется лишь основной файл, поэтому там сборки нет — только `pull`. Подробнее про деплой — в `DEPLOY.md`.

Состояние Mongo живёт в volume `mongo-data`; `kp-sqlite.db` в docker-режиме не используется (MONGODB_URL задан → `config.IS_SQLITE=False`).

## Конфигурация (env vars, см. config.py)

- `MSX_HOST` — базовый адрес сервера, подставляется во все ссылки MSX. На render.com автоматически берётся `RENDER_EXTERNAL_URL`. **Без него ссылки сломаны.**
- `MONGODB_URL` — строка подключения к Mongo. Если пуста — автоматически включается SQLite (`SQLITE_URL`, по умолчанию `./kp-sqlite.db`). См. `config.IS_SQLITE`.
- `PLAYER` / `ALTERNATIVE_PLAYER` — URL плагина-плеера MSX (HLS/HTTP). `PROTOCOL` (`hls4`/`hls`/`http`), `QUALITY`, `TIZEN`.
- `KP_CLIENT_ID` / `KP_CLIENT_SECRET` — OAuth-креды кинопаба (есть дефолты).

Полная таблица переменных — в README.md.

## Архитектура

Поток запроса: TV → `api.py` (эндпоинты под `/msx/...`) → `Device.kp` (`models/KinoPub.py`, HTTP-клиент кинопаба) → данные оборачиваются в доменные модели (`models/`) → каждая модель сериализуется в MSX через `to_msx*()` методы и хелперы `util/msx.py` → JSON в TV.

Ключевые узлы:

- **`api.py`** — все маршруты FastAPI. HTTP-middleware `auth` на каждом запросе достаёт `device_id` из query-параметра `id`, грузит/создаёт `Device` и кладёт в `request.state.device`. Эндпоинты из списка `UNAUTHORIZED` пропускаются без `id`. Все исключения ловятся middleware и превращаются в MSX-экран ошибки (`msx.handle_exception`).

- **`models/Device.py`** — устройство = единица состояния, хранится в БД по `id` (приходит от MSX). Держит OAuth-токены кинопаба, `DeviceSettings` и экземпляр `KinoPub`. Все `toggle_*` меняют настройки локально и/или дёргают `/device/{id}/settings` кинопаба, затем `update_settings()` пишет в БД.

- **`models/KinoPub.py`** — асинхронный клиент API кинопаба. Метод `api()` при ответе `401` сам рефрешит токены (`refresh_tokens` → `db.update_tokens`) и повторяет запрос. Регистрация устройства — через OAuth device flow (`get_codes` / `check_registration`).

- **`util/msx.py`** — конструкторы MSX-JSON (меню, списки, панели, экраны настроек/ошибок). Центральная функция `format_action()` строит MSX-action-строки (`module:request:interaction:...@...`) и подставляет `MSX_HOST` + `{ID}`. Доменные модели вызывают эти хелперы из своих `to_msx*()`.

- **`util/db.py`** — фасад над БД, по `config.IS_SQLITE` делегирует в `db_mongo.py` или `db_sqlite.py` (одинаковый интерфейс). SQLite-схема версионируется списком в `sqlite_migrations.py` (применяется при импорте модуля; добавление миграции = новый элемент в списке).

- **`util/proxy.py`** — опциональный прокси видео/HLS через сам сервер (`/msx/proxy?url=...`), включается настройкой устройства `proxy`. `check_url` пускает только домены из таблицы `domains` (антиоткрытый-прокси); домены запоминаются в `make_proxy_url`/`rewrite_domain` при отдаче ссылок. `rewrite_domain` переписывает относительные пути в HLS-манифестах на проксированные.

### Соглашения

- Каждая доменная модель в `models/` оборачивает сырой dict ответа кинопаба и имеет методы `to_msx*()`, отдающие готовый фрагмент MSX-JSON. Логику представления держим в модели, а не в `api.py`.
- ID элементов настроек (`FOURK_ID`, `PROXY_ID` и т.д.) определены в `util/msx.py` и используются и при отрисовке, и в `/settings/toggle/{setting}` — менять согласованно.
- `LENNY` / `SAD_LENNY` в `util/msx.py` — текстовые заглушки экранов ошибки/пустоты.
