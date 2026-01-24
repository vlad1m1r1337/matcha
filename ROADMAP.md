# Roadmap - Matcha Dating App Backend

## Общая концепция

Matcha - это backend для dating приложения, разрабатываемый как учебный проект для изучения Django и backend-разработки.

**Ключевые принципы:**
- N-слойная архитектура (endpoints → services → repositories)
- Без использования Django ORM (только raw SQL)
- RESTful API
- PostgreSQL как основная база данных

---

## Этап 1: Базовая архитектура ✅ (В процессе)

### Текущий статус
- [x] Настроена база данных PostgreSQL через Docker
- [x] Создана базовая схема БД (users, profiles, images)
- [x] Настроен Django проект с базовой конфигурацией
- [x] Написаны базовые тесты для работы с raw SQL
- [ ] Внедрить n-слойную архитектуру

### Задачи
1. **Создать структуру слоев:**
   - Repositories - слой доступа к данным (raw SQL)
   - Services - бизнес-логика
   - Views - обработчики HTTP запросов (endpoints)

2. **Базовые компоненты:**
   - Data classes для представления сущностей
   - Базовые исключения и обработка ошибок
   - Логирование

---

## Этап 2: Аутентификация и пользователи

### Функциональность
- Регистрация пользователя
- Логин/Логаут
- JWT токены для аутентификации
- Подтверждение email
- Восстановление пароля

### Эндпоинты
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/verify-email
POST /api/auth/reset-password
POST /api/auth/confirm-reset-password
```

### Компоненты
- `UserRepository` - CRUD операции с таблицей users
- `AuthService` - логика аутентификации, хеширование паролей, генерация токенов
- `EmailService` - отправка email уведомлений

---

## Этап 3: Профили пользователей

### Функциональность
- Создание и редактирование профиля
- Загрузка фотографий (до 5 шт, одна - аватар)
- Просмотр собственного профиля
- Указание интересов, био, геолокации

### Эндпоинты
```
GET    /api/profile/me
PUT    /api/profile/me
POST   /api/profile/me/images
DELETE /api/profile/me/images/{id}
PATCH  /api/profile/me/images/{id}/set-avatar
```

### Компоненты
- `ProfileRepository` - работа с таблицей profiles
- `ImageRepository` - работа с таблицей images
- `ProfileService` - валидация данных профиля, управление изображениями
- Валидация: один аватар на профиль, максимум 5 изображений

---

## Этап 4: Поиск и фильтрация

### Функциональность
- Поиск пользователей по критериям
- Фильтры: возраст, расстояние, интересы, fame rating
- Сортировка результатов
- Пагинация

### Эндпоинты
```
GET /api/users/search?age_min=18&age_max=30&distance=50&interests=hiking,coffee&sort=distance&page=1
GET /api/users/suggestions (рекомендации на основе совпадения интересов и предпочтений)
```

### Компоненты
- `SearchRepository` - сложные SQL запросы с фильтрацией
- `SearchService` - формирование поисковых критериев
- Расчет расстояния по координатам (геолокация)

---

## Этап 5: Взаимодействия (Matches & Likes)

### Функциональность
- Лайки (односторонние)
- Матчи (взаимные лайки)
- Просмотр истории лайков
- Блокировка пользователей
- Репорт пользователей

### Эндпоинты
```
POST   /api/likes/{user_id}
DELETE /api/likes/{user_id}
GET    /api/likes/received
GET    /api/likes/sent
GET    /api/matches
POST   /api/users/{user_id}/block
POST   /api/users/{user_id}/report
```

### Новые таблицы
```sql
CREATE TABLE likes (
  id SERIAL PRIMARY KEY,
  from_user_id INTEGER NOT NULL REFERENCES users(id),
  to_user_id INTEGER NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(from_user_id, to_user_id)
);

CREATE TABLE blocks (
  id SERIAL PRIMARY KEY,
  blocker_id INTEGER NOT NULL REFERENCES users(id),
  blocked_id INTEGER NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(blocker_id, blocked_id)
);
```

### Компоненты
- `LikeRepository`, `BlockRepository`
- `MatchService` - логика определения матчей, уведомления

---

## Этап 6: Чат и уведомления

### Функциональность
- Чат между пользователями (только при взаимном матче)
- Real-time сообщения (WebSockets или long polling)
- История сообщений
- Уведомления о новых матчах, лайках, сообщениях

### Эндпоинты
```
GET  /api/messages/{user_id}
POST /api/messages/{user_id}
GET  /api/notifications
PATCH /api/notifications/{id}/read
```

### Новые таблицы
```sql
CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  from_user_id INTEGER NOT NULL REFERENCES users(id),
  to_user_id INTEGER NOT NULL REFERENCES users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_read BOOLEAN DEFAULT FALSE
);

CREATE TABLE notifications (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  type TEXT NOT NULL,
  content JSONB,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Компоненты
- `MessageRepository`, `NotificationRepository`
- `ChatService` - валидация прав на отправку сообщений (только при матче)
- WebSocket handler или long polling endpoint

---

## Этап 7: Fame Rating и активность

### Функциональность
- Система рейтинга (fame rating)
- Учет просмотров профиля
- История посещений
- Влияние активности на видимость в поиске

### Логика Fame Rating
- +1 за полученный лайк
- +5 за матч
- +1 за отправленное сообщение
- -2 за анлайк
- Просмотры профиля влияют на рейтинг

### Новые таблицы
```sql
CREATE TABLE profile_views (
  id SERIAL PRIMARY KEY,
  viewer_id INTEGER NOT NULL REFERENCES users(id),
  viewed_id INTEGER NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Компоненты
- `FameService` - расчет и обновление fame rating
- `ProfileViewRepository` - логирование просмотров

---

## Этап 8: Тестирование и документация

### Задачи
- Юнит-тесты для всех слоев (repositories, services, views)
- Интеграционные тесты для основных сценариев
- API документация (OpenAPI/Swagger)
- Документация по архитектуре
- Code coverage > 80%

---

## Этап 9: Оптимизация и production-ready

### Задачи
- Индексы для оптимизации запросов
- Кеширование (Redis)
- Rate limiting
- CORS настройки
- Безопасность (HTTPS, CSRF, SQL injection защита)
- Логирование и мониторинг
- Docker-compose для полного стека

---

## Дополнительные возможности (опционально)

- [ ] Online статус пользователей
- [ ] Поддержка нескольких языков
- [ ] Верификация профилей
- [ ] Премиум-функции (boosted visibility, unlimited likes)
- [ ] Статистика для пользователя (кто просматривал профиль)
- [ ] Теги и расширенные интересы
- [ ] Интеграция с внешними сервисами (геолокация API)

---

## Технологический стек

**Backend:**
- Django 6.0
- PostgreSQL 16
- psycopg3 (PostgreSQL adapter)
- django-environ (environment variables)

**Планируется добавить:**
- JWT authentication (PyJWT)
- WebSockets (Django Channels) или long polling
- Redis (кеширование)
- Celery (асинхронные задачи, email)
- Docker (full-stack deployment)

**Тестирование:**
- Django TestCase / TransactionTestCase
- pytest (опционально)

---

## Текущий фокус

Сейчас идет работа над **Этапом 1** - внедрение n-слойной архитектуры:
1. Создать базовые repository классы
2. Создать базовые service классы
3. Рефакторить существующий код (`hello/views.py`) под новую архитектуру
4. Добавить тесты для каждого слоя

После завершения этапа 1 переходим к **Этапу 2** - аутентификация.
