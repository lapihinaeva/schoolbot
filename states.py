from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    waiting_for_grade = State()

class Registration_change(StatesGroup):
    waiting_for_grade_change = State()