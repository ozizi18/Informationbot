# Бот Информации о Техникуме

Этот бот является простым инструментом для получения информации о техникуме. Он разработан с использованием библиотеки **aiogram** для Telegram и позволяет пользователю получать актуальную информацию о учебном заведении.

## 🚀 Функциональность

Бот предоставляет следующие возможности:

* **Просмотр новостей** техникума.
* **Получение расписания** занятий.
* **Информация о предстоящих мероприятиях**.
* **Контактные данные** сотрудников.
* **Отправка отзывов и предложений**.
* **Административная панель** для управления контентом.

## 🛠️ Технологии

* **aiogram**: асинхронная библиотека для работы с Telegram API.
* **SQLite3**: для хранения данных.
* **asyncio**: для асинхронного программирования.

## 📝 Установка

1. Клонируйте репозиторий:  
   `git clone https://github.com/ozizi18/Informationbot.git`  
   `cd Informationbot`
   
2. Создайте виртуальное окружение:  
   `python -m venv venv`  
   `source venv/bin/activate` # Linux/macOS  
   `venv\Scripts\activate` # Windows

3. Установите зависимости:  
   `pip install -r requirements.txt`

4. Запустите бота:  
   `python bot.py`

## 💡 Использование

### Основные команды:

* **/start** — Запуск бота и отображение главного меню.
* **Просмотр новостей** — Получение последних новостей техникума.
* **Получить расписание** — Отображение расписания занятий.
* **Информация о мероприятиях** — Получение информации о предстоящих мероприятиях.
* **Контактные данные** — Получение контактной информации сотрудников.
* **Отправить отзыв** — Возможность отправить отзыв или предложение.

## ⚙️ Примечания

Бот использует асинхронные функции для обработки запросов, что позволяет ему эффективно работать с большим количеством пользователей одновременно.