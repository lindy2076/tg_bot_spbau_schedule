# Это бот Расписание СПбАУ

Бот написан на aiogram с помощью pydantic и sqlalchemy. Выдаёт всякую всячину. Фичи:

- расписание на неделю (/week)
- расписание на конкретный день (/day)
- расписание на сегодня (/today)
- расписание на завтра (/tomorrow)
- текущая пара (/now)
- следующая пара (/next)
- расписание в виде pdf (/pdf)
- послать админу сообщение (/send_admin)
- помощь (/help, /me)

админские фичи:

- разослать сообщение всем (/send_all)
- отредактировать расписание на какой-то день для какой-то группы (/edit)
- обновить пдфку с расписанием (/pdfupd)

Расписание выдаётся на основе выбранной группы (/setgr).

[tg: @schedule_spbau_bot](https://t.me/schedule_spbau_bot)

# Как запустить у себя?

Написан под линукс, т.к. прод обычно крутится на нём. 

1. Пропиши `make env` для создания **.env** файла

2. Поменяй в **.env** дефолтное значение токена бота на токен бота, айди админа на свой айди
3. Настрой название файла для хранения `file_id` пдфки с расписанием в `timetable_bot/config.py`, а также timeoffset.

4. (Этот шаг нужен, если ты будешь дальше чёта править локально у себя.) Создай виртуальное окружение `python3 -m venv venv`, активируй его `. venv/bin/activate` и поставь зависимости `pip install -r requirements.txt`.

5. Пропиши `make build` для сборки докер образов **базы, бота** и **админки бд**. Админка крутится на `8081` порту.
   
6. Пропиши `make revision` для создания миграции бд.

7. Пропиши `make migrate head` для накатывания созданной миграции.

8. Протестируй бота в телеге. 

Пропиши `make down`, чтобы выключить бота, бд и админку. В следующий раз приложение можно поднять командой `make up`. Оно запустится быстрее, т.к. не собирает докер образы.

# В целом

В январе 2024 переписал с aiogram2 на aiogram3, добавил фичи. Старая версия осталась в ветке `aiogram2`.

Расписания лежат в `/schedule_json` в формате json

Логи пишутся в `spbau_sch.log`. В базе одна таблица, в которой хранятся время обновления группы юзера, тг имя, тг айди, номер группы. База постгрес.

Когда-нибудь я напишу тесты...
