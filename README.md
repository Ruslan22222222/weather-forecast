# Weather Forecast Project

Проект прогноза погоды, разработанный на Django с использованием HTMX для динамического обновления интерфейса.

## 🚀 Технологии

- Python 3.11
- Django 5.2.1
- HTMX
- Tailwind CSS
- daisyUI
- PostgreSQL
- Docker & Docker Compose

## 📋 Требования

- Docker
- Docker Compose

## 🛠 Установка и запуск

1. **Клонирование репозитория**
   ```bash
   git clone <url-репозитория>
   cd weather-forecast
   ```

2. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   ```
   Отредактируйте `.env` файл:
   ```env
   DEBUG=True
   SECRET_KEY='your-secret-key-here'
   DATABASE_URL=postgres://weather_user:weather_password@db:5432/weather_db
   ```

3. **Запуск проекта**
   ```bash
   # Сборка и запуск контейнеров
   docker-compose up --build
   ```

4. **Выполнение миграций**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Создание суперпользователя**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 📁 Структура проекта

weather-forecast/
├── config/ # Конфигурационные файлы
├── static/ # Статические файлы
├── staticfiles/ # Собранные статические файлы
├── templates/ # HTML шаблоны
├── weather/ # Основное приложение
├── manage.py # Скрипт управления Django
├── requirements.txt # Зависимости проекта
└── docker-compose.yml # Конфигурация Docker

## 🔐 Доступ к проекту

- Веб-интерфейс: http://localhost:8000
- Админ-панель: http://localhost:8000/admin

## 🛠 Основные команды

```bash
# Запуск проекта
docker-compose up

# Остановка проекта
docker-compose down

# Просмотр логов
docker-compose logs -f

# Выполнение команд Django
docker-compose exec web python manage.py <command>
```

## 📚 Документация

- [Django Documentation](https://docs.djangoproject.com/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Docker Documentation](https://docs.docker.com/)

## 👥 Автор

- Руслан Малофеев

## 📞 Контакты

TG-Russlanovv

Если у вас возникли вопросы по проекту или положительные эмоции, пожалуйста, свяжитесь со мной.