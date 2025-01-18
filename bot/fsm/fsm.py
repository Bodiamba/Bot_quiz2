from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter

class FSM(StatesGroup):
    waiting_for_confirmation = State()

class QuizFSM():
    fsm: FSM
    waiting_for_confirmation_filter: StateFilter
    def __init__(self, fsm: FSM, waiting_for_confirmation_filter: StateFilter):
        self.fsm = fsm
        self.waiting_for_confirmation_filter = waiting_for_confirmation_filter

