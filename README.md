# ToDo Telegram Bot

Это Telegram-бот для управления списком задач. Бот позволяет добавлять, просматривать и удалять задачи с помощью простых
команд. Проект реализован с использованием библиотеки [aiogram](https://docs.aiogram.dev/) и организован по модульному
принципу.

## Функциональность

- **Запуск бота:** Команда `/start` для инициализации и приветствия.
- **Добавление задачи:** Команда `/add` позволяет добавить новую задачу.
- **Просмотр задач:** Команда `/my_tasks` выводит список текущих задач.
- **Удаление задач:** Команда `/delete` удаляет выполненные задачи.

## Требования

- Python 3.8+
- [aiogram](https://pypi.org/project/aiogram/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [aiosqlite](https://pypi.org/project/aiosqlite/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

Все зависимости указаны в файле `requirements.txt`.

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/SsalLt/ToDo_telegram_bot.git
   cd ToDo_telegram_bot-main
   ```

2. **Создайте и активируйте виртуальное окружение (опционально):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка переменных окружения:**

   Создайте файл `.env` в корне проекта и добавьте в него ваш токен:

   ```env
   TOKEN=your_telegram_bot_token
   ```

## Запуск

После настройки переменных окружения и установки зависимостей, запустите бота командой:

```bash
python main.py
```

## Структура проекта

```
ToDo_telegram_bot-main/
├── .gitignore             # Файлы и папки, исключаемые из репозитория
├── README.md              # Документация проекта
├── app/
│   ├── database/
│   │   ├── models.py      # Модели и инициализация базы данных
│   │   └── requests_db.py # Функции для работы с базой данных
│   ├── handlers.py        # Обработчики команд и сообщений
│   └── keyboards.py       # Определения клавиатур для бота
├── config.py              # Конфигурация проекта (токен, команды, логирование)
├── main.py                # Точка входа в приложение
└── requirements.txt       # Список зависимостей
```
