# matcha

## Docker

В проекте используется `docker compose` для поднятия Postgres и pgAdmin.

### Требования

- Docker + Docker Compose plugin (`docker compose version`)

### Быстрый старт

Запуск БД и pgAdmin:

```bash
docker compose up -d db pgadmin
```

Проверить статус:

```bash
docker compose ps
```

Остановить:

```bash
docker compose down
```

### Порты

- Postgres наружу: `${DB_PORT:-5433}` → контейнерный `5432`
- pgAdmin наружу: `${PGADMIN_PORT:-8080}` → контейнерный `80`

Можно переопределить через переменные окружения или `.env` рядом с `docker-compose.yml`:

```bash
DB_PORT=5433
PGADMIN_PORT=8080
```

### Доступ к Postgres

Параметры (см. `docker-compose.yml`):

- DB: `matcha_test`
- User: `matcha`
- Password: `matcha_password`

Подключиться через psql внутри контейнера:

```bash
docker compose exec -T db psql -U matcha -d matcha_test
```

### Инициализация схемы и тестовых данных

Скрипты из `db/init` монтируются в контейнер как `/docker-entrypoint-initdb.d`.
Postgres выполняет их **только при первом создании** data volume (`pgdata`), когда БД ещё “пустая”.

Если вы изменили `db/init/*.sql`, но данные/таблицы не обновились — это нормально: volume уже существует.

#### Полный сброс БД (удалить volume и инициализировать заново)

```bash
docker compose down -v
docker compose up -d db pgadmin
```

#### Прогнать SQL вручную (без удаления volume)

Например, применить `00_schema.sql` к уже поднятой БД:

```bash
docker compose exec -T db psql -U matcha -d matcha_test -f /docker-entrypoint-initdb.d/00_schema.sql
```

### pgAdmin

Открыть в браузере: `http://localhost:${PGADMIN_PORT:-8080}`

Логин (см. `docker-compose.yml`):

- Email: `admin@matcha.local`
- Password: `admin_password`

Добавление сервера в pgAdmin:

- Host name/address: `db` (имя сервиса в compose)
- Port: `5432`
- Maintenance database: `matcha_test`
- Username: `matcha`
- Password: `matcha_password`

### Troubleshooting

- Если `db` “не видит” изменения в `db/init`: удалите volume (`docker compose down -v`) или прогоните SQL вручную через `psql -f`.
- Если порт занят: поменяйте `DB_PORT`/`PGADMIN_PORT`.


