class ErrorMessages(str):
    NO_GROUP = "🥀 выбери в /setgr свою группу"
    NO_SCHEDULE_FOR_GROUP = "🥀 пока для этой группы расписания нет..."
    GROUP_DOESNT_EXIST = "🥀 такой группы нет.. напиши моему автору!"
    EDIT_MISSING_PARAMS = "чего-то не хватает. /edit group day"
    EDIT_WRONG_DAY = "день введён неправильно. можно 0-6"
    CANT_PARSE_CHATANDMSG_IDS = "не могу спарсить айдишники"
    NOTHING_FOUND = "по таким ключевым словам ничего не найдено... попробуй другие."
    RESULT_TOO_LARGE = "поиск по таким ключевым словам слишком широкий. Преподов получилось слишком много и они не помещаются в одно сообщение"
    FILE_IS_NOT_PDF = "нужен pdf!"
    IMPOSSIBLE_DAY_NOT_FOUND = "странно однако этого дня нет"
    INVALID_JSON = "failed to validate json"
    NO_PDF_AVAILABLE = "о нет pdf ещё не загрузили"

    @classmethod
    def no_such_group(cls, group: str):
        return f"группы {group} нет."

    @classmethod
    def cant_send_msg(cls, user_id: int):
        return f"{user_id} меня заблочил."

    @classmethod
    def error_happened(cls, err_msg: str):
        return f"произошла ошипка. {err_msg}"

    @classmethod
    def cant_answer(cls, err_msg: str):
        return f"ошипка: {err_msg}. не могу ответить"
    
    @classmethod
    def json_load_failed(cls, e: Exception):
        return f"failed to load json. {e}"
    
    @classmethod
    def failed_to_write(cls, e: Exception):
        return f"ошибка во время записи: {e}"
    
    @classmethod
    def failed_to_read(cls, e: Exception):
        return f"ошибка чтения file_id. {e}"


class TextResponse(str):
    SEE_MENU = "🌾 посмотри в меню, там команды всякие. но пока можешь выбрать свою группу:"
    CHOOSE_DAY = "🌻 выбери день:"
    CHOOSE_GROUP = "🌾 надо выбрать группу:"
    CHOOSE_GROUP2 = "🌾 выбери группу из списка:"
    NO_SCHEDULE_FOR_DAY = "🍂 на этот день расписания нет"
    DAY_NOTHING = "🌻 НИЧЕГО!!! СВОБОДА!!!"
    CURR_CLASS_NONE = "🍂 кажется ничего не идёт..."
    NEXT_CLASS_NONE = "🌾 домой"
    SAME_GROUP_CHOSEN = "кажется ты уже выбрал эту группу..."
    USER_DELETED = "🌽 тебя больше (а может и не больше) нет в моей бд. (но в логах есть🙃)"
    CHOOSE_GROUP_POLITE = "🌽 к сожалению, я пока о тебе ничего не знаю. попробуй /setgr"
    YOU_ARE_NOT_ADMIN = "🥀 ты не админ..."
    NOTHING_SENT = "🏔 ничего не отправлено. сообщение пустое!"
    MESSAGE_SENT_SUCCESSFULLY = "🌽 сообщение отправлено!"
    MESSAGE_WASNT_SENT = "🏔 ничего не отправлено"
    WRITE_MESSAGE_FOR_ADMIN = "что мне передать админу?"
    ENTER_KEYWORDS = "введи через пробел какие-нибудь ключевые слова, по которым можно найти препода/ов, например фамилию или её часть (поиск по точным совпадениям):\n<i>симонов матан</i>\n<i>симонов ngs</i>\n<i>био</i>"

    ADMIN_SELECT_DEGREE = "выберите степень: 0 - bak, 1 - mag, 2 - asp"
    ADMIN_NUM_NOT_IN_RANGE = "эээ"
    ADMIN_REPLIED = "ответил"
    ATTACH_PDF = "прикрепите pdf"
    PDF_UPDATED = "расписание обновлено"
    MSG_IS_NOT_TEXT = "нужен текст..."
    THIS_IS_BACH_SCHEDULE = "это бакалаврское расписание"

    STATE_CLEARED = "окэй"
    NO_STATES = "нет состояний."
    SPECIAL_STICKER_FILE_ID = "CAACAgIAAxkBAAINPmXOezeSpDrrcpaYkrk4tO3YgoOsAAJDNAACSzfASfFXoCOxFpenNAQ"

    POLICY = "\n\nя храню только жизненно необходимую информацию, а именно: " + \
        "айди телеграма, имя в телеграме, номер группы, время обращения " + \
        "и все сообщения боту. Чтобы удалить себя из базы данных, пропишите /del ." + \
        "\nЧтобы получить расписание в pdf напишите /pdf или pdf ." + \
        "\nЧтобы отправить какое-либо сообщение админу напишите /send_admin *сообщение*" + \
        "\n\nрепа: <a href='github.com/lindy2076/tg_bot_spbau_schedule/tree/master'>гитхаб</a>"

    @classmethod
    def greet(cls, username: str) -> str:
        return "🌻 привет, {:s}!! 🤗🤗🤗".format(username)

    @classmethod
    def echo_and_dayselect(cls, username: str, msg: str) -> str:
        """
        Повторяет сообщение пользователя и предлагает выбрать день недели.
        """
        return "выбери день: ".format(username, msg)

    @classmethod
    def curr_class(cls, class_name: str, class_room: str ) -> str:
        """
        Пишет, что текущая пара под названием class_name идёт в class_room
        """
        return "🌾 сейчас идёт {:s} в {:s}".format(class_name, class_room)

    @classmethod
    def future_class(cls, class_name: str, class_room: str, class_time: str) -> str:
        """
        Пишет, что следующая пара под названием class_name будет в class_room в class_time 
        """
        return "🌽 сейчас будет {:s} в {:s} в {:s}".format(class_name, class_time, class_room)

    @classmethod
    def new_group(cls, new_group: str) -> str:
        return "🌾 теперь {:s} - ваша группа".format(new_group)

    @classmethod
    def info_and_policy(cls, group: str) -> str:
        return "🌻 я выдаю для тебя расписание группы номер {:s}".format(group) + TextResponse.POLICY

    @classmethod
    def curr_time(cls, day: str, time: str) -> str:
        return "\n\nсейчас у меня {:s}, {:s}".format(day.lower(), time)

    @classmethod
    def echo_user_msg_for_admin(cls, msg_obj) -> str:
        """Пишет имя отправителя и сообщение. Обрезается команда"""
        return f"{msg_obj.from_user.full_name} передаёт:\n{msg_obj.text}\n{msg_obj.from_user.id}_{msg_obj.message_id}"

    @classmethod
    def echo_msg_from_admin(cls, msg: str) -> str:
        return f"🥀 админ передаёт: {msg}"

    @classmethod
    def sent_successfully_to(cls, count: int) -> str:
        """пишет, что отправилось + количество"""
        return f"вроде отправилось. Всего {count}"
    
    @classmethod
    def group_day_and_day_json(cls, group: str, day: str, day_json: str):
        """выдает день, группу и словарь расписания дня"""
        return f"{group} {day} <pre><code class='language-json'>{day_json}</code></pre>\nОтправьте новый словарь. Или пишите /cancel для отмены"

    @classmethod
    def curr_week_odd_even(cls, week_is_odd: bool):
        """пишет неделя четная или нет"""
        return f"\n🍂 сейчас {('чётная', 'нечётная')[week_is_odd]} неделя"

    @classmethod
    def check_msg_before_sending(cls, msg_obj) -> str:
        """Пишет содержание сообщения и спрашивает отправить админу или нет"""
        return f"🍁 следующее сообщение будет передано админу:\n\n{msg_obj.text}\n\nотправлять?"

    @classmethod
    def prepend_emoji(cls, msg: str, emoji: str) -> str:
        return f"{emoji} {msg}"

    @classmethod
    def no_one_works_today(cls, daytitle_accusative: str) -> str:
        return f"🍂 {daytitle_accusative} никто не работает"
    
    @classmethod
    def schedule_json_changed(cls, dict: dict) -> str:
        return f"ok. <pre><code class='language-json'>{str(dict)}</code></pre>"


class LogMessage(str):
    @classmethod
    def sent_msg2admin(cls, message: object) -> str:
        return f"send_admin ({message.from_user.id}), {message.from_user.full_name}"

    @classmethod
    def err_send_all(cls, err: Exception) -> str:
        return f"error during send_all. {err}"

    @classmethod
    def same_msg_didnt_edit(cls, e: Exception) -> str:
        return f"same text, didn't edit. {e}"

    @classmethod
    def schedule_updated(cls, group: str) -> str:
        return f"расписание {group} обновлено"
