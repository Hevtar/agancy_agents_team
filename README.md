# AI Marketing Agency - Multi-Agent System

Система агентов для автоматизации маркетингового агентства полного цикла на основе AI.

## 📋 Описание

Это система из 15 специализированных AI-агентов, работающих совместно для выполнения комплексных маркетинговых задач. Каждый агент имеет свою роль, инструменты и может взаимодействовать с другими агентами через шину событий.

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator Agent                     │
│                    (Управление workflow)                    │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Strategy Team  │ │  Creative Team  │ │ Analytics Team  │
│                 │ │                 │ │                 │
│ • Project Mgr   │ │ • Content Mgr   │ │ • Data Analyst  │
│ • Strategist    │ │ • Copywriter    │ │ • SEO Specialist│
│ • Research      │ │ • Designer      │ │ • Web Analyst   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Event Bus                            │
│              (Межагентное взаимодействие)                   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   PostgreSQL    │ │     Redis       │ │    ChromaDB     │
│   (Данные)      │ │  (Кэш/Сессии)   │ │(Векторная база) │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker & Docker Compose
- Python 3.10+
- API ключ Polza.Ai (или совместимого OpenAI-сервиса)

### Установка

1. Клонируйте репозиторий:
```bash
git clone git@github.com:Hevtar/agancy_agents_team.git
cd agancy_agents_team
```

2. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env, добавив POLZA_AI_API_KEY
```

3. Запустите инфраструктуру:
```bash
cd infra
docker-compose up -d
```

4. Установите зависимости Python:
```bash
pip install -r requirements.txt
```

5. Инициализируйте базу данных:
```bash
python scripts/init_db.py
```

## 👥 Агенты

### Стратегическая команда
1. **Project Manager** - Управление проектами, координация
2. **Marketing Strategist** - Разработка стратегий
3. **Market Researcher** - Исследование рынка

### Креативная команда
4. **Content Manager** - Планирование контента
5. **SEO Copywriter** - SEO-оптимизированные тексты
6. **Social Media Manager** - Социальные сети
7. **Designer** - Визуальный контент (описания)

### Аналитическая команда
8. **Data Analyst** - Анализ данных
9. **SEO Specialist** - Технический SEO
10. **Web Analytics Manager** - Веб-аналитика

### Команда автоматизации
11. **Email Marketing Manager** - Email кампании
12. **PPC Specialist** - Контекстная реклама
13. **CRM Manager** - Управление клиентами

### Команда интеграций
14. **API Integration Specialist** - Интеграции
15. **E-commerce Manager** - Электронная коммерция

## 🛠️ Инструменты

Система включает 40+ инструментов в категориях:
- **Analytics** - Анализ данных, тренды, конверсии
- **Content** - Генерация идей, SEO, читаемость
- **Social Media** - Посты для разных платформ
- **Marketing** - Расчет метрик кампаний
- **Development** - Генерация кода, валидация, документация

## 📁 Структура проекта

```
agancy_agents_team/
├── agents/             # 15 агентов маркетингового агентства
├── api/                # REST API (FastAPI)
├── core/               # Ядро системы
├── integrations/       # Интеграции (Polza.Ai)
├── memory/             # Система памяти (Knowledge Base)
├── tools/              # Инструменты (40+)
├── workflows/          # Рабочие процессы
├── examples/           # Примеры (Sandbox)
├── scripts/            # Скрипты
├── infra/              # Инфраструктура (Docker)
├── .env.example        # Пример переменных окружения
├── requirements.txt    # Зависимости Python
└── README.md
```

## 📊 Мониторинг

- **Prometheus** - Метрики системы
- **Grafana** - Визуализация метрик
- **Алерты** - Уведомления о проблемах

Доступ к Grafana: `http://localhost:3000`

## 🧪 Тестирование

### Запуск в Sandbox режиме
```bash
python examples/sandbox_demo.py
```

### Интеграционные тесты
```bash
pytest tests/integration/
```

## 📖 Документация

- [Полная документация](docs/README.md)
- [API Reference](docs/api_reference.md)
- [Руководство по агентам](docs/agents_guide.md)

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательно |
|------------|----------|-------------|
| `POLZA_AI_API_KEY` | API ключ Polza.Ai | Да |
| `POLZA_AI_BASE_URL` | Базовый URL API | Нет |
| `DATABASE_URL` | PostgreSQL connection | Нет |
| `REDIS_URL` | Redis connection | Нет |
| `CHROMA_DB_PATH` | Путь к ChromaDB | Нет |

### Маршрутизация моделей

Настройка в `integrations/polza_ai/model_routing.yaml`:
- Выбор модели для каждого агента
- Fallback модели
- Лимиты токенов

## 🤝 Вклад

1. Fork репозиторий
2. Создайте feature branch
3. Внесите изменения
4. Отправьте pull request

## 📄 Лицензия

MIT License

## 📞 Контакты

- GitHub: [Hevtar](https://github.com/Hevtar)
- Issues: [GitHub Issues](https://github.com/Hevtar/agancy_agents_team/issues)