# 📊 Аналитика вакансий с Superset

Сервис для сбора, хранения и визуализации данных о вакансиях с портала trudvsem.ru.

### Требования
- Docker Desktop
- Git

### Установка и запуск

```bash
# Клонируйте репозиторий
git clone https://github.com/siuresko-sk/study_docker/DC_project.git
cd DC_project

# Создайте файл с переменными окружения в корне проекта и добавьте в него настройки подключения (настройки описаны ниже)
touch .env

# Запустите проект
docker-compose up -d --build
```

---

## 🌐 Доступ к сервисам

| Сервис | Адрес | Логин | Пароль |
|--------|-------|-------|--------|
| **Веб-интерфейс** (вакансии) | http://localhost:8080 | - | - |
| **REST API** (данные) | http://localhost:3000/vacancies | - | - |
| **BI-платформа Superset** | http://localhost:8088 | `admin` | `admin_secret_pass_2026` |

---

## 🔧 Создание .env файла

Создайте файл `.env` в корне проекта:

```env
# Настройки базы данных PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret_password_123
POSTGRES_DB=vacancies_db

# Настройки Apache Superset
SUPERSET_SECRET_KEY=your-secret-key-change-in-production
SUPERSET_ADMIN_USER=admin
SUPERSET_ADMIN_PASSWORD=admin_secret_pass_2026
```

---

## 🏗️ Архитектура проекта

```
┌─────────────────────────────────────────────────────┐
│                    Парсер (ETL)                     │
│  Собирает вакансии с trudvsem.ru каждые 4 часа      │
│           vacancies_parser.py + requests            │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              PostgreSQL (База данных)               │
│  Хранит вакансии в таблице vacancies                │
│            postgres:15-alpine                       │
└─────────────────────┬───────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────────┐       ┌─────────────────────────┐
│  PostgREST        │       │  Superset               │
│  (REST API)       │       │  (BI-визуализация)      │
│  :3000            │       │  :8088                  │
│  Данные в JSON    │       │  Дашборды и графики     │
└───────┬───────────┘       └─────────────────────────┘
        │
        ▼
┌───────────────────┐
│   Nginx           │
│   Веб-сервер      │
│   :8080           │
│   HTML/JS-сайт   │
└───────────────────┘
```

### Компоненты системы:

| Компонент | Технология | Назначение |
|-----------|-----------|------------|
| **Парсер** | Python + requests | Сбор вакансий с trudvsem.ru |
| **База данных** | PostgreSQL 15 | Хранение данных |
| **API Gateway** | PostgREST 12.0 | REST API для данных |
| **BI-платформа** | Apache Superset | Визуализация и дашборды |
| **Веб-сервер** | Nginx Alpine | Фронтенд-приложение |

---

## 📁 Структура проекта

```
DC_project/
├── parser/                    # ETL-парсер
│   ├── Dockerfile
│   ├── requirements.txt
│   └── vacancies_parser.py    # Основной код парсера
├── superset/                  # BI-платформа
│   ├── Dockerfile
│   ├── init_superset.sh      # Скрипт инициализации
│   ├── superset_config.py
│   └── dashboards/           # Экспортированные дашборды - не состоялось
├── web/                       # Фронтенд
│   └── index.html
├── nginx/                     # Nginx конфиг
│   └── default.conf
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 📊 Дашборды Superset

Инициализирован Superset, позволяющий добавить дэшборды.

---

## 🐳 Docker Hub

Готовые образы доступны на Docker Hub:

```bash
# Скачать образы
docker push siuress/dc_project-parser:latest
docker push siuress/dc_project-superset:latest
docker push siuress/dc_project-superset-init:latest
```

---

## 👨‍💻 Автор

Светлана Кирильчук
