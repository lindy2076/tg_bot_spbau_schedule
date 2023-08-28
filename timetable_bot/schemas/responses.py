# from enum import Enum

class ErrorMessages(str):
    NO_GROUP = "выбери в /setgr свою группу"
    NO_SCHEDULE = "расписания нет."


class TextResponse(str):
    SEE_MENU = "посмотри в меню, там команды всякие. но пока можешь выбрать свою группу:"
    CHOOSE_DAY = "выбери день:"
    CHOOSE_GROUP = "надо выбрать группу:"
    NO_SCHEDULE_FOR_GROUP = "пока для этой группы расписания нет..."
    NO_SCHEDULE_FOR_DAY = "на этот день расписания нет..."
    DAY_NOTHING = "НИЧЕГО!!! СВОБОДА!!!"
    NEXT_CLASS_NONE = "кажется ничего не идёт..."
    SAME_GROUP_CHOSEN = "кажется ты уже выбрал эту группу..."
    USER_DELETED = "тебя больше (а может и не больше) нет в моей бд. (но в логах есть🙃)"
    CHOOSE_GROUP_POLITE = "к сожалению, я пока о тебе ничего не знаю. попробуй /setgr *номер_группы*"

    POLICY = "\n\nя храню только жизненно необходимую информацию, а именно: " + \
        "айди телеграма, имя в телеграме, номер группы, время обращения, " + \
        "все сообщения боту, время онлайна в телеграме, фамилию в телеграме, " + \
        "вашу платёжную информацию, местоположение, а также номер телефона.\n" + \
        "шучу😁. я храню только ваш тг айди, тг имя, номер группы и время " + \
        "обращения к боту. чтобы удалить себя из базы данных, пропишите /del"

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
