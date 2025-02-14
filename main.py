import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from init_db import init_database

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
BOT_TOKEN = '7877054403:AAEl3brZHLAExXFr2PXq9sfVxPR82_scZBI'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Подключение к базе данных
conn = sqlite3.connect('college_info.db', check_same_thread=False)
cursor = conn.cursor()

# ID администраторов
ADMIN_IDS = [7940750902]


# Состояния FSM для админ-панели
class AdminStates(StatesGroup):
    # Состояния для новостей
    waiting_for_news_title = State()
    waiting_for_news_content = State()
    waiting_for_news_image = State()
    
    # Состояния для расписания
    waiting_for_schedule_group = State()
    waiting_for_schedule_day = State()
    waiting_for_schedule_lessons = State()
    
    # Состояния для мероприятий
    waiting_for_event_title = State()
    waiting_for_event_description = State()
    waiting_for_event_date = State()
    
    # Состояния для контактов
    waiting_for_contact_department = State()
    waiting_for_contact_name = State()
    waiting_for_contact_phone = State()
    waiting_for_contact_email = State()

# Состояния FSM для пользователей
class UserStates(StatesGroup):
    waiting_for_group = State()
    waiting_for_feedback = State()
    waiting_for_feedback_text = State()

# Клавиатуры
def get_main_keyboard():
    """Основная клавиатура пользователя"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📰 Новости")
    keyboard.add("📅 Расписание", "🎉 Мероприятия")
    keyboard.add("👥 Контакты", "📝 Оставить отзыв")
    return keyboard

def admin_keyboard():
    """Клавиатура администратора"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📰 Добавить новость")
    keyboard.add("📅 Добавить расписание")
    keyboard.add("🎉 Добавить мероприятие")
    keyboard.add("👥 Добавить контакт")
    keyboard.add("🗑 Удалить записи")
    keyboard.add("◀️ Вернуться в меню пользователя")
    return keyboard

def delete_keyboard():
    """Клавиатура для удаления записей"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Удалить новость")
    keyboard.add("Удалить расписание")
    keyboard.add("Удалить мероприятие")
    keyboard.add("Удалить контакт")
    keyboard.add("◀️ Назад")
    return keyboard

# Обработчики команд
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Добро пожаловать в бот Ижевского техникума экономики!\n"
        "Выберите нужный раздел:",
        reply_markup=get_main_keyboard()
    )

@dp.message_handler(commands=['admin'])
async def admin_start(message: types.Message):
    """Обработчик команды /admin"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            "👋 Добро пожаловать в панель администратора!\n"
            "Выберите действие:",
            reply_markup=admin_keyboard()
        )
    else:
        await message.answer("⛔️ У вас нет прав администратора")

# Пользовательские обработчики
@dp.message_handler(lambda message: message.text == "📰 Новости")
async def show_news(message: types.Message):
    """Показ новостей"""
    cursor.execute('SELECT title, content, date, image_url FROM news ORDER BY date DESC LIMIT 5')
    news = cursor.fetchall()
    if news:
        for title, content, date, image_url in news:
            if image_url:
                caption = f"📅 {date}\n📌 {title}\n\n{content}"
                try:
                    await message.answer_photo(photo=image_url, caption=caption)
                except Exception:
                    await message.answer(f"📅 {date}\n📌 {title}\n\n{content}")
            else:
                await message.answer(f"📅 {date}\n📌 {title}\n\n{content}")
    else:
        await message.answer("На данный момент новостей нет.")

@dp.message_handler(lambda message: message.text == "📅 Расписание")
async def show_schedule_groups(message: types.Message):
    """Показ списка групп для расписания"""
    cursor.execute('SELECT DISTINCT group_name FROM schedule')
    groups = cursor.fetchall()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        keyboard.add(group[0])
    keyboard.add("◀️ Назад")
    await message.answer("Выберите группу:", reply_markup=keyboard)
    await UserStates.waiting_for_group.set()

@dp.message_handler(state=UserStates.waiting_for_group)
async def show_schedule(message: types.Message, state: FSMContext):
    """Показ расписания для выбранной группы"""
    if message.text == "◀️ Назад":
        await state.finish()
        await message.answer("Главное меню:", reply_markup=get_main_keyboard())
        return

    cursor.execute('SELECT day, lessons FROM schedule WHERE group_name = ? ORDER BY day', (message.text,))
    schedule = cursor.fetchall()
    if schedule:
        response = f"📅 Расписание группы {message.text}:\n\n"
        for day, lessons in schedule:
            response += f"📌 {day}:\n{lessons}\n\n"
        await message.answer(response, reply_markup=get_main_keyboard())
    else:
        await message.answer("Расписание для этой группы не найдено.", reply_markup=get_main_keyboard())
    await state.finish()

@dp.message_handler(lambda message: message.text == "🎉 Мероприятия")
async def show_events(message: types.Message):
    """Показ мероприятий"""
    cursor.execute('SELECT title, description, date FROM events WHERE date >= date("now") ORDER BY date')
    events = cursor.fetchall()
    if events:
        response = "🎉 Предстоящие мероприятия:\n\n"
        for title, description, date in events:
            response += f"📅 {date}\n📌 {title}\n{description}\n\n"
        await message.answer(response)
    else:
        await message.answer("На данный момент нет запланированных мероприятий.")

@dp.message_handler(lambda message: message.text == "👥 Контакты")
async def show_contacts(message: types.Message):
    """Показ контактов"""
    cursor.execute('SELECT department, name, phone, email FROM contacts')
    contacts = cursor.fetchall()
    if contacts:
        response = "👥 Контакты:\n\n"
        for department, name, phone, email in contacts:
            response += f"📌 {department}\n👤 {name}\n📞 {phone}\n📧 {email}\n\n"
        await message.answer(response)
    else:
        await message.answer("Список контактов пуст.")

@dp.message_handler(lambda message: message.text == "📝 Оставить отзыв")
async def feedback_start(message: types.Message):
    """Начало отправки отзыва"""
    await message.answer(
        "Пожалуйста, напишите ваш отзыв или предложение.\n"
        "Мы обязательно рассмотрим его!"
    )
    await UserStates.waiting_for_feedback_text.set()

@dp.message_handler(state=UserStates.waiting_for_feedback_text)
async def process_feedback(message: types.Message, state: FSMContext):
    """Обработка текста отзыва"""
    user_id = message.from_user.id
    username = message.from_user.username or "Неизвестный"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Сохраняем отзыв в базу данных
    cursor.execute(
        'INSERT INTO feedback (user_id, username, text, date) VALUES (?, ?, ?, ?)',
        (user_id, username, message.text, date)
    )
    conn.commit()
    
    # Пересылаем отзыв администраторам
    for admin_id in ADMIN_IDS:
        try:
            # Отправляем информацию о пользователе
            admin_info = (
                f"📬 Новый отзыв!\n"
                f"От: @{username}\n"
                f"ID пользователя: {user_id}\n"
                f"Дата: {date}\n"
                f"➖➖➖➖➖➖➖➖➖"
            )
            await bot.send_message(admin_id, admin_info)
            
            # Пересылаем само сообщение с отзывом
            await message.forward(admin_id)
        except Exception as e:
            logging.error(f"Ошибка отправки уведомления админу {admin_id}: {e}")
    
    await message.answer(
        "✅ Спасибо за ваш отзыв! Мы обязательно рассмотрим его.",
        reply_markup=get_main_keyboard()
    )
    await state.finish()

# Административные обработчики
@dp.message_handler(lambda message: message.text == "📰 Добавить новость")
async def add_news_start(message: types.Message):
    """Начало добавления новости"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Введите заголовок новости:")
        await AdminStates.waiting_for_news_title.set()

@dp.message_handler(state=AdminStates.waiting_for_news_title)
async def process_news_title(message: types.Message, state: FSMContext):
    """Обработка заголовка новости"""
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите текст новости:")
    await AdminStates.waiting_for_news_content.set()

@dp.message_handler(state=AdminStates.waiting_for_news_content)
async def process_news_content(message: types.Message, state: FSMContext):
    """Обработка содержания новости"""
    async with state.proxy() as data:
        data['content'] = message.text
    await message.answer("Отправьте изображение для новости (или отправьте /skip для пропуска):")
    await AdminStates.waiting_for_news_image.set()

@dp.message_handler(commands=['skip'], state=AdminStates.waiting_for_news_image)
@dp.message_handler(content_types=['photo'], state=AdminStates.waiting_for_news_image)
async def process_news_image(message: types.Message, state: FSMContext):
    """Обработка изображения новости"""
    async with state.proxy() as data:
        if message.photo:
            photo = message.photo[-1]
            data['image_url'] = photo.file_id
        else:
            data['image_url'] = None
        
        cursor.execute(
            'INSERT INTO news (title, content, date, image_url) VALUES (?, ?, ?, ?)',
            (data['title'], data['content'], datetime.now().strftime("%Y-%m-%d"), data['image_url'])
        )
        conn.commit()
        
    await message.answer("✅ Новость успешно добавлена!", reply_markup=admin_keyboard())
    await state.finish()

@dp.message_handler(lambda message: message.text == "📅 Добавить расписание")
async def add_schedule_start(message: types.Message):
    """Начало добавления расписания"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Введите название группы (например, 'ИС-101'):")
        await AdminStates.waiting_for_schedule_group.set()

@dp.message_handler(state=AdminStates.waiting_for_schedule_group)
async def process_schedule_group(message: types.Message, state: FSMContext):
    """Обработка группы расписания"""
    async with state.proxy() as data:
        data['group_name'] = message.text
    await message.answer("Введите день недели:")
    await AdminStates.waiting_for_schedule_day.set()

@dp.message_handler(state=AdminStates.waiting_for_schedule_day)
async def process_schedule_day(message: types.Message, state: FSMContext):
    """Обработка дня недели"""
    async with state.proxy() as data:
        data['day'] = message.text
    await message.answer("Введите расписание занятий:")
    await AdminStates.waiting_for_schedule_lessons.set()

@dp.message_handler(state=AdminStates.waiting_for_schedule_lessons)
async def process_schedule_lessons(message: types.Message, state: FSMContext):
    """Обработка занятий расписания"""
    async with state.proxy() as data:
        cursor.execute(
            'INSERT INTO schedule (group_name, day, lessons) VALUES (?, ?, ?)',
            (data['group_name'], data['day'], message.text)
        )
        conn.commit()
    
    await message.answer("✅ Расписание успешно добавлено!", reply_markup=admin_keyboard())
    await state.finish()

@dp.message_handler(lambda message: message.text == "🎉 Добавить мероприятие")
async def add_event_start(message: types.Message):
    """Начало добавления мероприятия"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Введите название мероприятия:")
        await AdminStates.waiting_for_event_title.set()

@dp.message_handler(state=AdminStates.waiting_for_event_title)
async def process_event_title(message: types.Message, state: FSMContext):
    """Обработка названия мероприятия"""
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите описание мероприятия:")
    await AdminStates.waiting_for_event_description.set()

@dp.message_handler(state=AdminStates.waiting_for_event_description)
async def process_event_description(message: types.Message, state: FSMContext):
    """Обработка описания мероприятия"""
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer("Введите дату мероприятия (формат: ГГГГ-ММ-ДД):")
    await AdminStates.waiting_for_event_date.set()

@dp.message_handler(state=AdminStates.waiting_for_event_date)
async def process_event_date(message: types.Message, state: FSMContext):
    """Обработка даты мероприятия"""
    async with state.proxy() as data:
        try:
            datetime.strptime(message.text, "%Y-%m-%d")
            cursor.execute(
                'INSERT INTO events (title, description, date) VALUES (?, ?, ?)',
                (data['title'], data['description'], message.text)
            )
            conn.commit()
            await message.answer("✅ Мероприятие успешно добавлено!", reply_markup=admin_keyboard())
        except ValueError:
            await message.answer("❌ Неверный формат даты. Используйте формат ГГГГ-ММ-ДД")
            return
    await state.finish()

@dp.message_handler(lambda message: message.text == "👥 Добавить контакт")
async def add_contact_start(message: types.Message):
    """Начало добавления контакта"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Введите название отдела:")
        await AdminStates.waiting_for_contact_department.set()

@dp.message_handler(state=AdminStates.waiting_for_contact_department)
async def process_contact_department(message: types.Message, state: FSMContext):
    """Обработка отдела контакта"""
    async with state.proxy() as data:
        data['department'] = message.text
    await message.answer("Введите ФИО:")
    await AdminStates.waiting_for_contact_name.set()

@dp.message_handler(state=AdminStates.waiting_for_contact_name)
async def process_contact_name(message: types.Message, state: FSMContext):
    """Обработка имени контакта"""
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Введите номер телефона:")
    await AdminStates.waiting_for_contact_phone.set()

@dp.message_handler(state=AdminStates.waiting_for_contact_phone)
async def process_contact_phone(message: types.Message, state: FSMContext):
    """Обработка телефона контакта"""
    async with state.proxy() as data:
        data['phone'] = message.text
    await message.answer("Введите email:")
    await AdminStates.waiting_for_contact_email.set()

@dp.message_handler(state=AdminStates.waiting_for_contact_email)
async def process_contact_email(message: types.Message, state: FSMContext):
    """Обработка email контакта"""
    async with state.proxy() as data:
        cursor.execute(
            'INSERT INTO contacts (department, name, phone, email) VALUES (?, ?, ?, ?)',
            (data['department'], data['name'], data['phone'], message.text)
        )
        conn.commit()
    
    await message.answer("✅ Контакт успешно добавлен!", reply_markup=admin_keyboard())
    await state.finish()

@dp.message_handler(lambda message: message.text == "🗑 Удалить записи")
async def delete_menu(message: types.Message):
    """Меню удаления записей"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Выберите, что хотите удалить:", reply_markup=delete_keyboard())

@dp.message_handler(lambda message: message.text == "◀️ Назад")
async def back_to_admin_menu(message: types.Message):
    """Возврат в админ-меню"""
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Панель администратора:", reply_markup=admin_keyboard())

@dp.message_handler(lambda message: message.text == "◀️ Вернуться в меню пользователя")
async def back_to_user_menu(message: types.Message):
    """Возврат в пользовательское меню"""
    await message.answer("Вы вернулись в меню пользователя", reply_markup=get_main_keyboard())

# Обработчики удаления записей
@dp.message_handler(lambda message: message.text == "Удалить новость")
async def delete_news(message: types.Message):
    """Удаление новостей"""
    if message.from_user.id in ADMIN_IDS:
        cursor.execute('SELECT id, title, date FROM news ORDER BY date DESC')
        news = cursor.fetchall()
        if news:
            keyboard = types.InlineKeyboardMarkup()
            for news_id, title, date in news:
                keyboard.add(types.InlineKeyboardButton(
                    text=f"{date}: {title}",
                    callback_data=f"del_news_{news_id}"
                ))
            await message.answer("Выберите новость для удаления:", reply_markup=keyboard)
        else:
            await message.answer("Нет доступных новостей для удаления")

@dp.message_handler(lambda message: message.text == "Удалить расписание")
async def delete_schedule(message: types.Message):
    """Удаление расписания"""
    if message.from_user.id in ADMIN_IDS:
        cursor.execute('SELECT id, group_name, day FROM schedule ORDER BY group_name, day')
        schedules = cursor.fetchall()
        if schedules:
            keyboard = types.InlineKeyboardMarkup()
            for schedule_id, group, day in schedules:
                keyboard.add(types.InlineKeyboardButton(
                    text=f"{group} - {day}",
                    callback_data=f"del_schedule_{schedule_id}"
                ))
            await message.answer("Выберите расписание для удаления:", reply_markup=keyboard)
        else:
            await message.answer("Нет доступных расписаний для удаления")

@dp.message_handler(lambda message: message.text == "Удалить мероприятие")
async def delete_event(message: types.Message):
    """Удаление мероприятий"""
    if message.from_user.id in ADMIN_IDS:
        cursor.execute('SELECT id, title, date FROM events ORDER BY date DESC')
        events = cursor.fetchall()
        if events:
            keyboard = types.InlineKeyboardMarkup()
            for event_id, title, date in events:
                keyboard.add(types.InlineKeyboardButton(
                    text=f"{date}: {title}",
                    callback_data=f"del_event_{event_id}"
                ))
            await message.answer("Выберите мероприятие для удаления:", reply_markup=keyboard)
        else:
            await message.answer("Нет доступных мероприятий для удаления")

@dp.message_handler(lambda message: message.text == "Удалить контакт")
async def delete_contact(message: types.Message):
    """Удаление контактов"""
    if message.from_user.id in ADMIN_IDS:
        cursor.execute('SELECT id, department, name FROM contacts ORDER BY department')
        contacts = cursor.fetchall()
        if contacts:
            keyboard = types.InlineKeyboardMarkup()
            for contact_id, department, name in contacts:
                keyboard.add(types.InlineKeyboardButton(
                    text=f"{department}: {name}",
                    callback_data=f"del_contact_{contact_id}"
                ))
            await message.answer("Выберите контакт для удаления:", reply_markup=keyboard)
        else:
            await message.answer("Нет доступных контактов для удаления")

# Обработчики callback-запросов для удаления
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_news_'))
async def process_delete_news(callback_query: types.CallbackQuery):
    """Обработка удаления новости"""
    news_id = int(callback_query.data.split('_')[2])
    cursor.execute('DELETE FROM news WHERE id = ?', (news_id,))
    conn.commit()
    await callback_query.answer("Новость удалена!")
    await callback_query.message.edit_text("✅ Новость успешно удалена!")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_schedule_'))
async def process_delete_schedule(callback_query: types.CallbackQuery):
    """Обработка удаления расписания"""
    schedule_id = int(callback_query.data.split('_')[2])
    cursor.execute('DELETE FROM schedule WHERE id = ?', (schedule_id,))
    conn.commit()
    await callback_query.answer("Расписание удалено!")
    await callback_query.message.edit_text("✅ Расписание успешно удалено!")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_event_'))
async def process_delete_event(callback_query: types.CallbackQuery):
    """Обработка удаления мероприятия"""
    event_id = int(callback_query.data.split('_')[2])
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    await callback_query.answer("Мероприятие удалено!")
    await callback_query.message.edit_text("✅ Мероприятие успешно удалено!")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_contact_'))
async def process_delete_contact(callback_query: types.CallbackQuery):
    """Обработка удаления контакта"""
    contact_id = int(callback_query.data.split('_')[2])
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    await callback_query.answer("Контакт удален!")
    await callback_query.message.edit_text("✅ Контакт успешно удален!")

def create_tables():
    """Создание всех необходимых таблиц"""
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            image_url TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            day TEXT NOT NULL,
            lessons TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            date TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        logging.info("Таблицы базы данных успешно созданы")
    except Exception as e:
        logging.error(f"Ошибка при создании таблиц: {e}")

if __name__ == '__main__':
    from aiogram import executor
    
    # Создаем таблицы перед запуском бота
    create_tables()
    
    # Инициализируем данные
    try:
        init_database()
        logging.info("База данных успешно инициализирована")
    except Exception as e:
        logging.error(f"Ошибка при инициализации данных: {e}")
    
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
