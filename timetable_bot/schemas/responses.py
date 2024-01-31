class ErrorMessages(str):
    NO_GROUP = "выбери в /setgr свою группу"
    NO_SCHEDULE_FOR_GROUP = "пока для этой группы расписания нет..."
    GROUP_DOESNT_EXIST = "такой группы нет.. напиши моему автору!"
    EDIT_MISSING_PARAMS = "чего-то не хватает. /edit group day"
    EDIT_WRONG_DAY = "день введён неправильно. можно 0-6"

    @classmethod
    def no_such_group(group: str):
        return f"группы {group} нет."


class TextResponse(str):
    SEE_MENU = "посмотри в меню, там команды всякие. но пока можешь выбрать свою группу:"
    CHOOSE_DAY = "выбери день:"
    CHOOSE_GROUP = "надо выбрать группу:"
    CHOOSE_GROUP2 = "выбери группу из списка:"
    NO_SCHEDULE_FOR_DAY = "на этот день расписания нет"
    DAY_NOTHING = "НИЧЕГО!!! СВОБОДА!!!"
    CURR_CLASS_NONE = "кажется ничего не идёт..."
    NEXT_CLASS_NONE = "домой"
    SAME_GROUP_CHOSEN = "кажется ты уже выбрал эту группу..."
    USER_DELETED = "тебя больше (а может и не больше) нет в моей бд. (но в логах есть🙃)"
    CHOOSE_GROUP_POLITE = "к сожалению, я пока о тебе ничего не знаю. попробуй /setgr"
    YOU_ARE_NOT_ADMIN = "ты не админ..."
    NOTHING_SENT = "ничего не отправлено. сообщение пустое!"
    MESSAGE_SENT_SUCCESSFULLY = "сообщение отправлено"

    POLICY = "\n\nя храню только жизненно необходимую информацию, а именно: " + \
        "айди телеграма, имя в телеграме, номер группы, время обращения " + \
        "и все сообщения боту. Чтобы удалить себя из базы данных, пропишите /del ." + \
        "\nЧтобы получить расписание в pdf напишите /pdf или pdf ." + \
        "\nЧтобы отправить какое-либо сообщение админу напишите /send_admin *сообщение*" + \
        "\n\nрепа: github.com/lindy2076/tg_bot_spbau_schedule"

    @classmethod
    def greet(cls, username: str) -> str:
        return "ПРИВЕТ, {:s}!! 🤗🤗🤗".format(username)

    @classmethod
    def echo_and_dayselect(cls, username: str, msg: str) -> str:
        """
        Повторяет сообщение пользователя и предлагает выбрать день недели.
        """
        return "{:s} говорит: {:s}\nвыбери день: ".format(username, msg)

    @classmethod
    def curr_class(cls, class_name: str, class_room: str ) -> str:
        """
        Пишет, что текущая пара под названием class_name идёт в class_room
        """
        return "сейчас идёт {:s} в {:s}".format(class_name, class_room)

    @classmethod
    def future_class(cls, class_name: str, class_room: str, class_time: str) -> str:
        """
        Пишет, что следующая пара под названием class_name будет в class_room в class_time 
        """
        return "сейчас будет {:s} в {:s} в {:s}".format(class_name, class_time, class_room)

    @classmethod
    def new_group(cls, new_group: str) -> str:
        return "теперь {:s} - ваша группа".format(new_group)

    @classmethod
    def info_and_policy(cls, group: str) -> str:
        return "я выдаю для тебя расписание группы номер {:s}".format(group) + TextResponse.POLICY

    @classmethod
    def curr_time(cls, day: str, time: str) -> str:
        return "\n\nсейчас у меня {:s}, {:s}".format(day.lower(), time)

    @classmethod
    def echo_user_msg(cls, msg_obj) -> str:
        """Пишет имя отправителя и сообщение. Обрезается команда"""
        return f"{msg_obj.from_user.first_name} передаёт:\n{msg_obj.text[12:]}"

    @classmethod
    def sent_successfully_to(cls, count: int) -> str:
        """пишет, что отправилось + количество"""
        return f"вроде отправилось. Всего {count}"
    
    @classmethod
    def group_day_and_day_json(cls, group: str, day: str, day_json: dict):
        """выдает день, группу и словарь расписания дня"""
        return f"{group} {day} {day_json}\nОтправьте новый словарь. Или пишите /cancel для отмены"

    @classmethod
    def curr_week_odd_even(cls, week_is_odd: bool):
        """пишет неделя четная или нет"""
        return f"\nсейчас {('чётная', 'нечётная')[week_is_odd]} неделя"
