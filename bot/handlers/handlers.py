from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import fsm
import gui
import config_data
import game





class Handlers:
    def __init__(self, bot: Bot, fsm: fsm.QuizFSM):
        self.qr: game.Quiz = None
        self.bot = bot
        self.qrfsm = fsm

    def create_participant(self, message: Message) -> game.Participant:
        name = message.from_user.first_name
        id = message.from_user.id
        return game.Participant(name, id)

    def set_quiz_class(self, qr: game.Quiz) -> None:
        self.qr = qr

    async def get_registered(self, message: Message) -> bool | None:
        if message.from_user.id in self.qr.get_participants_dict().keys():
            return True
        else:
            await self.send_reply(message, 'Вы не зарегистрированы.')

    async def send_reply(self, message: Message, text: str) -> None:
        await message.bot.send_message(message.from_user.id, text)

    async def command_start_handler(self, message: Message) -> None:
        await message.bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}.', reply_markup=await gui.gui.show_keyboard())

    async def command_help_handler(self, message: Message) -> None:
        await self.send_reply(message, config_data.config.helpmsg)

    async def show_participants_handler(self, message: Message) -> None:
        if await self.get_registered(message):
            await self.send_reply(message, self.qr.get_participants_str())

    async def show_score_handler(self, message: Message) -> None:
        if await self.get_registered(message):
            participant: game.Participant = self.qr.get_participants_dict().get(message.from_user.id)
            await self.send_reply(message, str(participant.get_score()))

    async def register_handler(self, message: Message) -> None:
        res = await self.qr.add_participant(self.create_participant(message))
        if res == 0:
            await self.send_reply(message, 'Вы вернулись.')
        elif res == 1:
            await self.send_reply(message, 'Вы зарегистрировались.')
        elif res == 2:
            await self.send_reply(message, 'Вы уже зарегистрированы или регистрация в данный момент невозможна.')

    async def start_quiz_handler(self, message: Message) -> None:
        if await self.get_registered(message):
            await self.qr.quiz_start()

    async def process_callback_answer(self, callback_query: CallbackQuery):
        # Извлечение текста ответа из callback_data
        answer_with_id = callback_query.data.split('answer_')[1]
        await self.bot.answer_callback_query(callback_query.id) # Подтверждение нажатия
        res = self.qr.set_participant_answer(callback_query.from_user.id, answer_with_id)
        if res == 0:
            await self.bot.send_message(callback_query.from_user.id, f'Вы выбрали: {answer_with_id.split("_")[1]}')
        elif res == 1:
            await self.bot.send_message(callback_query.from_user.id, f'На вопрос: {answer_with_id.split("_")[0]} уже отвечали.')
        elif res == 2:
            await self.bot.send_message(callback_query.from_user.id, 'Вы уже отвечали.')

    async def register_handler(self, message: Message) -> None:
        res = await self.qr.add_participant(self.create_participant(message))
        if res == 0:
            await self.send_reply(message, 'Вы вернулись.')
        elif res == 1:
            await self.send_reply(message, 'Вы зарегистрировались.')
        elif res == 2:
            await self.send_reply(message, 'Вы уже зарегистрированы или регистрация в данный момент невозможна.')

    """ Обработчик для удаления аккаунта. Приём команды пользователя """
    async def delete_account_handler(self, message: Message, state: FSMContext):
        await state.set_state(self.qrfsm.fsm.waiting_for_confirmation) # Установка состояния
        await message.reply("Пожалуйста, подтвердите 'Y' или отмените удаление аккаунта - 'N'.")

    """ Обработчик для удаления аккаунта. Ожидание ответа пользователя """
    async def delete_account_confirmation_handler(self, message: Message, state: FSMContext):
        if message.text.upper() == 'Y':
            res = self.qr.del_participant(self.create_participant(message))
            if res == 0:
                await message.reply("Ваш аккаунт был успешно удален.")
            elif res == 1:
                await message.reply("Сейчас идёт игра, удаление невозможно.")
            elif res == 2:
                await message.reply("Вы не зарегистрированы.")
        elif message.text.upper() == 'N':
            await message.reply("Удаление аккаунта отменено.")
        else:
            await message.reply("Пожалуйста, ответьте 'Y' или 'N'.")
        # Сброс состояния
        await state.clear()



    def register_handlers(self, dp: Dispatcher) -> None:
        dp.message.register(self.command_start_handler, CommandStart())
        dp.message.register(self.command_help_handler, Command("help"))
        dp.message.register(self.delete_account_handler, Command("delacc"))
        dp.message.register(self.register_handler, lambda message: message.text == config_data.config.btns.btn_reg)
        dp.message.register(self.start_quiz_handler, lambda message: message.text == config_data.config.btns.btn_start_quiz)
        dp.message.register(self.show_score_handler, lambda message: message.text == config_data.config.btns.btn_show_score)
        dp.message.register(self.show_participants_handler, lambda message: message.text == config_data.config.btns.btn_show_participants)
        dp.message.register(self.delete_account_confirmation_handler, self.qrfsm.waiting_for_confirmation_filter)
        dp.callback_query.register(self.process_callback_answer, lambda c: c.data.startswith('answer_'))

