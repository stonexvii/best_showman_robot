from aiogram.fsm.state import State, StatesGroup


class UserDialog(StatesGroup):
    wait_for_answer = State()
    count_out_of_range = State()
