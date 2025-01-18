import database
import asyncio
from datetime import datetime
from aiogram import Bot
import gui
import googlesheets
from .question import Question
from .participant import Participant


def sort_dict(data: dict) -> str:
    """Сортировка словаря по убыванию и конвертация в строку."""
    sorted_items = sorted(data.items(), key=lambda item: item[1], reverse=True)
    result = ", ".join(f"{key}: {value}" for key, value in sorted_items)
    return result

class Quiz:
    # Типы сообщений
    MSG_TYPE_QUESTION = 0
    MSG_TYPE_RESULTS = 1
    MSG_TYPE_LAST_REGISTERED = 2

    def __init__(self, bot: Bot, db: database.DB):
        self.bot = bot
        self.db = db
        self.participants = {} # id участника: объект участника
        self.inactive_participants = {} # id участника: объект участника
        self.questions = {} # id вопроса: объект вопроса
        self.current_question_index = 0
        self.quiz_started = False
        self.time = 0
        self.delay = 1
        self.question: Question = None
        self.task_instance = asyncio.create_task(self.task_handler())
        self.results = {}
        self.results_str = None
        self.last_connected_participant: Participant = None
        self.connect_and_check_table()

    # ---- ВЗАИМОДЕЙСТВИЕ С БД ---- #
    def connect_and_check_table(self):
        self.inactive_participants = self.db.load_users_to_dict()

    # ---- ЛОГИКА ИГРЫ ---- #
    # Обработка викторины
    async def task_handler(self):
        while True:
            await self.task()
            await asyncio.sleep(self.delay)

    async def task(self) -> None:
        """Основная задача для обработки викторины. """
        if self.quiz_started:
            self.time += self.delay
            if self.time % 30 == 0:
                await self.next_question()

            pa: list[int | str] = []
            for participant in self.participants:
                participant: Participant = self.participants.get(participant)
                # Соберём ответы участников, чтобы проверить, все ли ответили
                pa.append(participant.get_answer())
                # Если был правильный ответ, повысим счёт и перейдём к следующему
                if str(participant.get_answer()) == str(self.question.get_answer()):
                    participant.increment_score()
                    participant.increment_game_score()
                    await self.next_question()
                elif None not in pa:
                    await self.next_question()
    
    # Вызовы
    async def quiz_start(self) -> int:
        """Запуск викторины и очистка статусов предыдущей. """
        if not self.questions or self.quiz_started:
            return
        self.question = self.questions.get(0)
        self.quiz_started = True
        self.current_question_index = 0
        self.time = 0
        self.set_noanswered_all()
        self.clear_game_score_all()
        await self.send_info_all(self.MSG_TYPE_QUESTION, None)
    
    async def next_question(self) -> None:
        """Переключение вопроса на следующий и обновление статусов. """
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.question = self.questions.get(self.current_question_index)
            self.set_noanswered_all()
            self.time = 0
            await self.send_info_all(self.MSG_TYPE_QUESTION, None)
        else:
            self.quiz_started = False
            await self.send_results_all()

    def set_noanswered_all(self) -> None:
        """Убирает ответы у всех участников (меняет на None). """
        for participant in self.participants:
            participant: Participant = self.participants.get(participant)
            participant.clear_answered()

    def set_participant_answer(self, participant_id, answer_with_id: str) -> int:
        """Обработка полученного из aiogram ответа. """
        # Вопросы приходят только участникам
        # retval: 0 - успешно, 1 - нажали на предыдущий вопрос, 2 - уже отвечали
        participant: Participant = self.participants.get(participant_id)
        if not participant.get_answered():
            answer_id = answer_with_id.split("_")[0]
            answer_text = answer_with_id.split("_")[1]
            if str(answer_id) == str(self.question.get_id()):
                participant.set_answer(answer_text)
                participant.set_answered()
                return 0
            else:
                return 1
        else:
            return 2

    def clear_game_score_all(self):
        """Очистка счёта последней игры. """
        for participant in self.participants:
            participant: Participant = self.participants.get(participant)
            participant.clear_game_score()

    async def send_results_all(self):
        """Отправка результатов игры всем участникам. """
        list_for_gglsheets = []
        for participant in self.participants:
            participant: Participant = self.participants.get(participant)
            self.results[participant.get_name()] = participant.get_game_score()
            self.db.update_user_score(participant.get_id(), participant.get_score())
            list_for_gglsheets.append([participant.get_name(), participant.get_game_score(), str(datetime.now())])
        
        self.results_str = sort_dict(self.results)
        await self.send_info_all(self.MSG_TYPE_RESULTS, None)
        await googlesheets.googlesheet.set_data_to_google_sheets(list_for_gglsheets)
        


    # ----- МЕНЕДЖМЕНТ ВОПРОСОВ И УЧАСТНИКОВ ----- #
    def add_question(self, question: Question):
        """Добавить вопрос (Question) в список вопросов. """
        self.questions[question.get_id()] = question

    async def add_participant(self, participant: Participant) -> bool:
        """Добавить участника игры. """
        # retvals: 0 - пользователь найден в базе данных, 1 - пользователь зарегистрирован,
        # 2 - пользователь уже зарегистрирован или идёт игра
        if participant.id not in self.participants.keys() and not self.quiz_started:
            if participant.get_id() in self.inactive_participants.keys():
                self.participants[participant.get_id()] = participant
                return 0
            else:
                self.participants[participant.get_id()] = participant
                self.last_connected_participant = participant
                await self.send_info_all(self.MSG_TYPE_LAST_REGISTERED, self.last_connected_participant)
                self.db.add_user(participant.get_id(), participant.get_name(), 0)
                return 1
        else:
            return 2
        
    def get_participants_dict(self) -> dict:
        """Получить словарь со всеми участниками. """
        return self.participants
    
    def get_participants_str(self) -> str:
        """Получить строку со всеми участниками. """
        participants = self.get_participants_dict()
        ptlist: list[str] = []
        for participant in participants:
            participant: Participant = participants.get(participant)
            ptlist.append(participant.name)
        return ", ".join(ptlist)
    
    def del_participant(self, participant: Participant) -> bool:
        if participant.get_id() in self.participants.keys() and not self.quiz_started:
            del self.participants[participant.get_id()]
            self.db.delete_user(participant.get_id())
            return 0
        elif self.quiz_started:
            return 1
        else:
            return 2
    
    # ----- ОТПРАВКА ИНФОРМАЦИИ УЧАСТНИКАМ ----- #
    async def send_info(self, participant: Participant, type: int):
        """Отправляет вопрос с инлайн-кнопками, список игроков или результаты участнику. """
        if type == self.MSG_TYPE_QUESTION:
            keyboard = await gui.gui.show_inl_keyboard(self.question.get_id(), self.question.answers)
            await self.bot.send_message(participant.get_id(), self.question.question, reply_markup=keyboard)
        elif type == self.MSG_TYPE_RESULTS:
            await self.bot.send_message(participant.get_id(), self.results_str)
        elif type == self.MSG_TYPE_LAST_REGISTERED:
            await self.bot.send_message(participant.get_id(), f'{self.last_connected_participant.get_name()} зарегистрировался.')

    async def send_info_all(self, type: int, except_participant: Participant):
        """Отправляет информацию всем участникам с исключением или без него. """
        for participant in self.participants:
            participant: Participant = self.participants.get(participant)
            # Исключение при отправке сообщения
            if participant is not except_participant:
                participant.clear_answer()
                await self.send_info(participant, type)