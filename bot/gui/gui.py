from aiogram.types import KeyboardButton as KB, ReplyKeyboardMarkup as RKM, \
                          InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

class Gui:
    btn_reg: str
    btn_start_quiz: str
    btn_show_score: str
    btn_show_participants: str
    
    def __init__(self, btn_reg: str, btn_start_quiz: str, btn_show_score: str, btn_show_participants: str):
        self.btn_reg = btn_reg
        self.btn_start_quiz = btn_start_quiz
        self.btn_show_score = btn_show_score
        self.btn_show_participants = btn_show_participants

    async def show_keyboard(self) -> RKM:
        btn1 = KB(text=self.btn_reg)
        btn2 = KB(text=self.btn_start_quiz)
        btn3 = KB(text=self.btn_show_score)
        btn4 = KB(text=self.btn_show_participants)
        keyboard = RKM(keyboard=[[btn1, btn2], [btn3, btn4]], resize_keyboard=True)
        return keyboard
    
    async def show_inl_keyboard(self, question_id: int, answers: list) -> IKM:
        buttons = []
        for answer in answers:
          buttons.append([IKB(text=str(answer), callback_data=f"answer_{question_id}_{answer}")])
        keyboard = IKM(inline_keyboard=buttons)
        return keyboard