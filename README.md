# Это бот Расписание СПбАУ

Написан на aiogram с помощью pydantic и sqlalchemy. Выдаёт всякую всячину, в основном расписание на неделю, на день и что идёт (или будет идти) в данный момент. 

Можно выбрать группу, на основании этого выбора потом выдаётся расписание.

# Как запустить у себя?

Написан под линукс, т.к. прод обычно крутится на нём. 

1. Пропиши `make env` для создания **.env** файла

2. Поменяй в **.env** дефолтное значение токена бота на токен бота.

3. Создай виртуальное окружение `python3 -m venv venv`, активируй его `. venv/bin/activate` и поставь зависимости `pip install -r requirements.txt`.

4. Пропиши `make build` для сборки докер образов **базы, бота** и **админки бд**. Админка крутится на `8081` порту.
   
5. Пропиши `make revision` для создания миграции бд.

6. Пропиши `make migrate head` для накатывания созданной миграции.

7. Протестируй бота в телеге. 

Пропиши `make down`, чтобы выключить бота, бд и админку.

# В целом

Логи пишутся в `spbau_sch.log`. В базе одна таблица, в которой хранятся время обновления группы юзера, тг имя, тг айди, номер группы. База постгрес.

Надо бы прикрутить жсоны с расписанием к докер контейнеру приложения, а то пересобирать его ради одной-двух правок в расписании не очень идея.

Когда-нибудь я напишу тесты...
