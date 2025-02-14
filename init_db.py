import sqlite3
import datetime

def init_database():
    conn = sqlite3.connect('college_info.db')
    cursor = conn.cursor()

    # Очистка существующих таблиц
    cursor.execute('DELETE FROM news')
    cursor.execute('DELETE FROM schedule')
    cursor.execute('DELETE FROM events')
    cursor.execute('DELETE FROM contacts')

    # Добавление актуальных новостей
    news_data = [
        ('Экскурсия в ООО «Баланс – сервис»', 
         'Студенты ПОЧУ «Ижевский техникум экономики, управления и права Удмуртпотребсоюза» 3 курса специальности 38.02.06 Финансы посетили с экскурсией ООО «Баланс – сервис». В ходе экскурсии студенты познакомились с работой компании, узнали о возможностях трудоустройства и прохождения практики. Руководитель отдела внедрения Шадрин Алексей Владимирович рассказал о преимуществах работы в компании, о требованиях к соискателям и возможностях карьерного роста.', 
         '2025-01-16',
         'https://koopteh.ru/sites/default/files/styles/news_image/public/news/image/ezt9qcqqf5fvtt9k3vpzzjmshuye6vzais9uwuavhmvttuqnuua9hawchrgccrufgs9fexisbyerzuz3nrzeqlir.jpg'),
        
        ('Что нужно знать о взяточничестве', 
         'В рамках Международного дня борьбы с коррупцией в техникуме проведены мероприятия, направленные на формирование у обучающихся антикоррупционного мировоззрения. Студенты узнали об ответственности за дачу и получение взятки, о том, как не стать жертвой коррупционных действий.', 
         '2024-12-13',
         'https://koopteh.ru/sites/default/files/styles/news_image/public/news/image/buklet-korrupciya_page-0001.jpg'),
        
        ('Ждем выпускников ВУЗов!', 
         'ПОЧУ «Ижевский техникум экономики, управления и права Удмуртпотребсоюза» приглашает на работу выпускников ВУЗов по направлениям подготовки: юриспруденция, экономика, менеджмент, информационные технологии. Мы предлагаем интересную работу, достойную заработную плату, возможность профессионального роста.', 
         '2024-12-16',
         'https://koopteh.ru/sites/default/files/styles/news_image/public/news/image/s9cbmutdiqy.jpg'),
    ]
    cursor.executemany('INSERT INTO news (title, content, date, image_url) VALUES (?, ?, ?, ?)', news_data)

    # Добавление актуального расписания
    schedule_data = [
        ('ИС-101', 'Понедельник', '1. Математика (каб. 201)\n2. Основы программирования (каб. 305)\n3. Базы данных (каб. 303)\n4. Английский язык (каб. 401)'),
        ('ИС-101', 'Вторник', '1. Физика (каб. 202)\n2. Веб-программирование (каб. 304)\n3. Операционные системы (каб. 302)\n4. Физкультура'),
        ('ИС-101', 'Среда', '1. Информационная безопасность (каб. 306)\n2. Компьютерные сети (каб. 301)\n3. Проектирование ИС (каб. 305)\n4. История (каб. 402)'),
        
        ('ИС-102', 'Понедельник', '1. Основы программирования (каб. 305)\n2. Математика (каб. 201)\n3. Английский язык (каб. 401)\n4. Базы данных (каб. 303)'),
        ('ИС-102', 'Вторник', '1. Веб-программирование (каб. 304)\n2. Физика (каб. 202)\n3. Физкультура\n4. Операционные системы (каб. 302)'),
        ('ИС-102', 'Среда', '1. Компьютерные сети (каб. 301)\n2. Информационная безопасность (каб. 306)\n3. История (каб. 402)\n4. Проектирование ИС (каб. 305)'),
        
        ('П-201', 'Понедельник', '1. Технология разработки ПО (каб. 304)\n2. Математика (каб. 201)\n3. Системное программирование (каб. 305)\n4. Английский язык (каб. 401)'),
        ('П-201', 'Вторник', '1. Базы данных (каб. 303)\n2. Компьютерные сети (каб. 301)\n3. Веб-программирование (каб. 304)\n4. Физкультура'),
        ('П-201', 'Среда', '1. Информационная безопасность (каб. 306)\n2. Операционные системы (каб. 302)\n3. Проектирование ИС (каб. 305)\n4. История (каб. 402)')
    ]
    cursor.executemany('INSERT INTO schedule (group_name, day, lessons) VALUES (?, ?, ?)', schedule_data)

    # Добавление предстоящих мероприятий
    events_data = [
        ('День открытых дверей', 'Приглашаем абитуриентов и их родителей познакомиться с техникумом, преподавателями и образовательными программами', '2024-04-15'),
        ('Хакатон "IT Skills"', 'Командные соревнования по разработке программных решений. Регистрация команд открыта!', '2024-04-20'),
        ('Мастер-класс по кибербезопасности', 'Приглашенный специалист из "Лаборатории Касперского" проведет практический семинар', '2024-04-25'),
        ('Ярмарка вакансий', 'Встреча с представителями IT-компаний региона. Возможность получить приглашение на стажировку', '2024-05-10'),
        ('Защита дипломных проектов', 'Публичная защита выпускных квалификационных работ студентов групп П-401 и ИС-402', '2024-06-15')
    ]
    cursor.executemany('INSERT INTO events (title, description, date) VALUES (?, ?, ?)', events_data)

    # Добавление контактной информации
    contacts_data = [
        ('Директор', 'Белова Елена Ивановна', '+7 (3412) 37-01-80', 'ikoopteh@mail.ru'),
        ('Заместитель директора по учебно-методической работе', 'Зуева Татьяна Петровна', '+7 (3412) 44-65-12', 'ikoopteh@mail.ru'),
        ('Заместитель директора по воспитательной работе', 'Морсеева Марина Николаевна', '+7 (3412) 37-74-90', 'ikoopteh@mail.ru'),
        ('Главный бухгалтер', 'Кузьмицкая Светлана Васильевна', '+7 (3412) 55-32-48', 'ikoopteh@mail.ru')
    ]
    cursor.executemany('INSERT INTO contacts (department, name, phone, email) VALUES (?, ?, ?, ?)', contacts_data)

    # Создание таблицы отзывов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        text TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')

    # Создание таблицы новостей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        image_url TEXT
    )
    ''')

    # Создание таблицы расписания
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL,
        day TEXT NOT NULL,
        lessons TEXT NOT NULL
    )
    ''')

    # Создание таблицы мероприятий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')

    # Создание таблицы контактов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT NOT NULL,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
    print("База данных успешно инициализирована актуальными данными!") 
