from aiogram.fsm.state import State, StatesGroup


class SearchProfessor(StatesGroup):
    search = State()


class EditForm(StatesGroup):
    group = State()
    day = State()
    edit = State()


class PdfUpdForm(StatesGroup):
    select_degree = State()
    wait_for_pdf = State()


class SendAdminForm(StatesGroup):
    wait_for_message = State()
    confirm = State()
