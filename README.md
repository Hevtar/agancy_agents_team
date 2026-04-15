# Agency Agents — Система AI-агентов маркетингового агентства

## 📖 Описание

**Agency Agents** — это сложная система AI-агентов, реализующая функционал маркетингового агентства полного цикла. Система построена на основе многоагентной архитектуры, где каждый агент отвечает за определённую область маркетинга и взаимодействует с другими агентами через событийную шину.

### Ключевые возможности

- **14 специализированных AI-агентов** (маркетинговый стратег, контент-менеджер, SEO-специалист, SMM-менеджер, таргетолог, аналитик, email-маркетолог, дизайнер, бренд-менеджер, CRO-специалист, поддержка, проектный менеджер, отчётный генератор)
- **Единая событийная шина** для координации между агентами
- **Интеграция с POLZA AI** для использования современных LLM-моделей
- **Управление проектами и задачами** с автоматическим распределением
- **Базы знаний** на основе векторных хранилищ (ChromaDB)
- **REST API + WebSocket** для реального времени
- **Веб-панель управления** на Next.js
- **Мониторинг и метрики** через Prometheus + Grafana
- **Контроль токенов** и бюджетирование
- **Асинхронные задачи** через Celery

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                       │
│                    Порт 3000                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                    │
│                    Порт 8000                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Auth  │  Projects  │  Tasks  │  Agents  │  Events  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PostgreSQL    │  │     Redis       │  │    ChromaDB     │
│   Порт 5432     │  │   Порт 6379     │  │   Порт 8000     │
│   (данные)      │  │  (кэш/очереди)  │  │  (векторы)      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Celery Workers                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Agent Workers  │  Scheduler (Beat)  │  Event Bus   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    POLZA AI API                             │
│              (LLM модели через Polza.ai)                    │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Структура проекта

```
agancy_agents_team/
├── agents/                 # AI-агенты
│   ├── base_agent.py       # Базовый класс агента
│   ├── marketing_strategist.py
│   ├── content_manager.py
│   ├── seo_copywriter.py
│   ├── social_media_manager.py
│   ├── data_analyst.py
│   ├── seo_specialist.py
│   ├── email_marketing_manager.py
│   ├── ppc_specialist.py
│   ├── ux_designer.py
│   ├── brand_manager.py
│   ├── cro_specialist.py
│   ├── customer_support_agent.py
│   ├── report_generator.py
│   └── project_manager.py
├── api/                    # FastAPI приложение
│   ├── app.py              # Основной файл приложения
│   ├── auth.py             # Аутентификация
│   ├── models.py           # Pydantic модели
│   ├── crud.py             # Операции с БД
│   ├── routes.py           # API маршруты
│   └── metrics.py          # Метрики Prometheus
├── core/                   # Ядро системы
│   ├── config.py           # Конфигурация
│   ├── base_agent.py       # Базовый класс агента
│   ├── event_bus.py        # Событийная шина
│   └── celery_app.py       # Celery конфигурация
├── tools/                  # Инструменты для агентов
│   ├── registry.py         # Реестр инструментов
│   ├── analytics_tools.py  # Инструменты аналитики
│   ├── marketing_tools.py  # Маркетинговые инструменты
│   └── technical_tools.py  # Технические инструменты
├── workflows/              # Рабочие процессы
│   ├── base_workflow.py    # Базовый класс воркфлоу
│   ├── integrated_campaign.py
│   └── content_production.py
├── memory/                 # Память и знания
│   └── knowledge_base.py   # Векторная база знаний
├── integrations/           # Интеграции
│   └── polza_ai/           # POLZA AI интеграция
│       ├── client.py       # Клиент API
│       └── model_routing.yaml
├── frontend/               # Next.js фронтенд
│   ├── app/                # App Router страницы
│   ├── components/         # React компоненты
│   ├── lib/                # Утилиты и API
│   ├── package.json
│   └── Dockerfile
├── infra/                  # Инфраструктура
│   ├── docker-compose.yml  # Docker Compose
│   ├── Dockerfile          # Dockerfile для API
│   └── prometheus.yml      # Конфигурация Prometheus
├── scripts/                # Скрипты
│   └── init_db.py          # Инициализация БД
├── examples/               # Примеры использования
│   └── sandbox_demo.py
├── requirements.txt        # Python зависимости
├── .env.example            # Пример переменных окружения
└── README.md               # Документация
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Python 3.10+
- Node.js 20+ (для разработки фронтенда)
- API ключ POLZA AI

### 1. Клонирование репозитория

```bash
git clone git@github.com:Hevtar/agancy_agents_team.git
cd agancy_agents_team
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
# Отредактируйте .env, добавив ваш POLZA_AI_API_KEY
```

### 3. Запуск через Docker Compose

```bash
cd infra
docker-compose up -d
```

После запуска сервисы будут доступны по адресам:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Grafana**: http://localhost:3001 (логин: admin, пароль: admin)
- **Prometheus**: http://localhost:9090

### 4. Инициализация базы данных

```bash
docker exec agency_api python scripts/init_db.py
```

### 5. Проверка работы

```bash
# Проверка API
curl http://localhost:8000/api/health

# Проверка фронтенда
open http://localhost:3000
```

## 🔧 Локальная разработка (без Docker)

### Backend

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Копирование .env
cp .env.example .env
# Отредактируйте .env

# Запуск API
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

# Запуск Celery Worker (в отдельном терминале)
celery -A core.celery_app worker --loglevel=info

# Запуск Celery Beat (в отдельном терминале)
celery -A core.celery_app beat --loglevel=info
```

### Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Копирование .env
cp .env.example .env.local

# Запуск dev-сервера
npm run dev
```

## 📊 Мониторинг

### Prometheus метрики

Система экспортирует следующие метрики:
- `agent_tasks_total` — общее количество задач по агентам
- `agent_tasks_created_total` — созданные задачи
- `agent_tasks_completed_total` — завершённые задачи
- `tokens_used_total` — использованные токены
- `tokens_budget_remaining` — оставшийся бюджет токенов
- `events_published_total` — опубликованные события
- `events_consumed_total` — потреблённые события
- `workflow_executions_total` — выполнения воркфлоу
- `api_requests_total` — HTTP запросы
- `api_request_duration_seconds` — длительность запросов

### Grafana дашборды

После входа в Grafana (http://localhost:3001) доступны дашборды:
- **System Overview** — общий обзор системы
- **Agent Performance** — производительность агентов
- **Token Usage** — использование токенов
- **Workflow Status** — статус воркфлоу

## 🤖 AI Агенты

### Список агентов

| Агент | Роль | Описание |
|-------|------|----------|
| Marketing Strategist | Маркетинговый стратег | Разработка стратегий, анализ рынка |
| Content Manager | Контент-менеджер | Планирование и управление контентом |
| SEO Copywriter | SEO-копирайтер | Написание SEO-оптимизированных текстов |
| Social Media Manager | SMM-менеджер | Управление соцсетями |
| Data Analyst | Дата-аналитик | Анализ данных и метрик |
| SEO Specialist | SEO-специалист | Техническая SEO-оптимизация |
| Email Marketing Manager | Email-маркетолог | Email-кампании и рассылки |
| PPC Specialist | Таргетолог | Контекстная реклама |
| UX Designer | UX-дизайнер | Проектирование пользовательского опыта |
| Brand Manager | Бренд-менеджер | Управление брендом |
| CRO Specialist | CRO-специалист | Оптимизация конверсии |
| Customer Support Agent | Поддержка клиентов | Ответы на вопросы клиентов |
| Report Generator | Генератор отчётов | Создание отчётов и аналитики |
| Project Manager | Проектный менеджер | Управление проектами |

### Взаимодействие агентов

Агенты взаимодействуют через событийную шину (Event Bus):

1. **Публикация событий**: Агент публикует событие при изменении состояния
2. **Подписка**: Другие агенты подписываются на релевантные события
3. **Обработка**: Получив событие, агент выполняет свои действия
4. **Координация**: Через события агенты координируют сложные воркфлоу

Пример потока:
```
Project Created → Marketing Strategist анализирует → 
Content Plan Created → Content Manager распределяет →
Tasks Created → SEO Copywriter пишет → 
Content Ready → Social Media Manager публикует
```

## 📝 API Документация

После запуска API документация доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные эндпоинты

#### Аутентификация
- `POST /api/auth/token` — получение JWT токена
- `GET /api/auth/me` — получение текущего пользователя

#### Проекты
- `GET /api/projects` — список проектов
- `POST /api/projects` — создание проекта
- `GET /api/projects/{id}` — детали проекта
- `PUT /api/projects/{id}` — обновление проекта
- `DELETE /api/projects/{id}` — удаление проекта

#### Задачи
- `GET /api/tasks` — список задач
- `POST /api/tasks` — создание задачи
- `PUT /api/tasks/{id}` — обновление задачи
- `DELETE /api/tasks/{id}` — удаление задачи

#### Блокеры
- `GET /api/blockers` — список блокеров
- `POST /api/blockers` — создание блокера
- `PUT /api/blockers/{id}` — обновление блокера
- `DELETE /api/blockers/{id}` — удаление блокера

#### Агенты
- `GET /api/agents` — список агентов и их статусы

#### Система
- `GET /api/system/status` — статус системы
- `GET /api/tokens/stats` — статистика использования токенов

## 🔐 Безопасность

- JWT аутентификация для API
- Ролевая модель (admin, manager, viewer)
- CORS настройка
- Rate limiting
- Валидация входных данных

## 📈 Масштабирование

### Горизонтальное масштабирование Celery Workers

```bash
# Запуск нескольких worker'ов
docker-compose up -d --scale celery_worker=4
```

### Настройка Celery

В `core/config.py` можно настроить:
- `CELERY_WORKER_CONCURRENCY` — количество одновременных задач
- `CELERY_WORKER_MAX_TASKS_PER_CHILD` — перезапуск worker'ов
- `CELERY_TASK_TIME_LIMIT` — лимит времени на задачу

## 🧪 Тестирование

```bash
# Запуск тестов
pytest tests/ -v

# Запуск с покрытием
pytest tests/ --cov=. --cov-report=html
```

## 🚀 Развёртывание на VPS

### Требования к VPS

- **ОС**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **CPU**: минимум 2 ядра (рекомендуется 4+)
- **RAM**: минимум 4GB (рекомендуется 8GB+)
- **Диск**: минимум 40GB SSD
- **Доступ**: root или пользователь с sudo правами

### Шаг 1: Подготовка сервера

```bash
# Подключение к серверу
ssh root@your-server-ip

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y git curl wget software-properties-common apt-transport-https ca-certificates

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker --version
docker-compose --version

# Выход и повторный вход для применения изменений групп
exit
```

### Шаг 2: Клонирование репозитория

```bash
# Подключение к серверу
ssh user@your-server-ip

# Клонирование проекта
git clone git@github.com:Hevtar/agancy_agents_team.git
cd agancy_agents_team

# Или через HTTPS (если нет SSH ключа)
git clone https://github.com/Hevtar/agancy_agents_team.git
cd agancy_agents_team
```

### Шаг 3: Настройка переменных окружения

```bash
# Копирование примера
cp .env.example .env

# Редактирование .env файла
nano .env
```

Пример содержимого `.env` для production:
```bash
# Приложение
APP_ENV=production
APP_DEBUG=false

# POLZA AI (получите ключ на polza.ai)
POLZA_AI_API_KEY=your-polza-ai-api-key-here
POLZA_AI_BASE_URL=https://polza.ai/api/v1

# База данных
POSTGRES_DB=agency_db
POSTGRES_USER=agency_user
POSTGRES_PASSWORD=secure-random-password-here

# Redis
REDIS_PASSWORD=secure-redis-password-here

# Grafana
GRAFANA_ADMIN_PASSWORD=secure-grafana-password-here

# API URL для фронтенда (укажите ваш домен или IP)
NEXT_PUBLIC_API_URL=https://api.your-domain.com/api
```

### Шаг 4: Настройка домена и SSL (опционально, но рекомендуется)

```bash
# Установка Nginx
sudo apt install -y nginx

# Создание конфигурации Nginx
sudo nano /etc/nginx/sites-available/agency-agents
```

Пример конфигурации Nginx:
```nginx
# Frontend
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# API
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
}
```

```bash
# Включение конфигурации
sudo ln -s /etc/nginx/sites-available/agency-agents /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Установка SSL сертификата (Let's Encrypt)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d api.your-domain.com
```

### Шаг 5: Запуск через Docker Compose

```bash
cd infra

# Запуск всех сервисов
sudo docker-compose up -d

# Проверка статуса
sudo docker-compose ps

# Просмотр логов
sudo docker-compose logs -f
```

### Шаг 6: Инициализация базы данных

```bash
# Запуск миграций
sudo docker exec agency_api python scripts/init_db.py

# Создание администратора (если есть скрипт)
sudo docker exec agency_api python scripts/create_admin.py --username admin --password your-secure-password
```

### Шаг 7: Проверка работы

```bash
# Проверка API
curl https://api.your-domain.com/api/health

# Проверка фронтенда
curl https://your-domain.com

# Проверка через браузер
# Откройте https://your-domain.com
```

### Шаг 8: Мониторинг и обслуживание

```bash
# Просмотр логов конкретного сервиса
sudo docker-compose logs -f api
sudo docker-compose logs -f frontend
sudo docker-compose logs -f celery_worker

# Перезапуск сервиса
sudo docker-compose restart api

# Остановка всех сервисов
sudo docker-compose down

# Обновление проекта
cd /path/to/agancy_agents_team
git pull origin master
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
```

### Автоматический перезапуск при сбоях

Docker Compose автоматически перезапускает контейнеры при сбоях благодаря настройкам в docker-compose.yml:

```yaml
restart: unless-stopped
```

### Резервное копирование базы данных

```bash
# Создание бэкапа
sudo docker exec agency_postgres pg_dump -U agency_user agency_db > backup_$(date +%Y%m%d).sql

# Восстановление из бэкапа
cat backup_20260415.sql | sudo docker exec -i agency_postgres psql -U agency_user -d agency_db
```

### Настройка файрвола (UFW)

```bash
# Установка UFW
sudo apt install -y ufw

# Настройка правил
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Включение файрвола
sudo ufw enable
sudo ufw status
```

## 📊 Troubleshooting

### Проблемы с подключением к базе данных

```bash
# Проверка статуса PostgreSQL
sudo docker-compose ps postgres

# Просмотр логов
sudo docker-compose logs postgres

# Перезапуск
sudo docker-compose restart postgres
```

### Проблемы с памятью

Если серверу не хватает памяти:

```bash
# Уменьшение количества worker'ов
# Отредактируйте docker-compose.yml, уменьшив CELERY_WORKER_CONCURRENCY

# Или отключите неиспользуемые сервисы
sudo docker-compose stop grafana prometheus
```

### Проблемы с SSL

```bash
# Проверка сертификата
sudo certbot certificates

# Обновление сертификата
sudo certbot renew --dry-run
```

## 📄 Лицензия

MIT License

## 🤝 Вклад

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📞 Контакты

- GitHub: https://github.com/Hevtar/agancy_agents_team
- Документация: https://github.com/Hevtar/agancy_agents_team/wiki
