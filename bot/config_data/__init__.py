from .config import Config, TgBot, DatabaseConfig, GoogleTable, Btns

# Инициализация конфигурации
config = Config(
    tg_bot=TgBot(token='7743216405:AAEXiZEm9KYtwAfT8pWibEgjBacb1tKz_Gs'),
    db=DatabaseConfig(database='database/userscores.db'),
    gt=GoogleTable(service_account_file='googlesheets/pivotal-gearing-446718-h6-ba524314f613.json',
                   spreadsheet_id='1UvqCYe2zFyLCqHboE647RapiKOMrAwamaUJMmd2WVBg'),
    btns=Btns(btn_reg='Зарегистрироваться',
              btn_start_quiz='Начать викторину',
              btn_show_score='Показать счёт',
              btn_show_participants='Показать участников'),
    helpmsg='''1. Чтобы стать участником викторины, нажми "Зарегистрироваться". \n
2. Викторина начинается с теми участниками, которые успели зарегистрироваться. \n
3. Время, отведённое для ответа на каждый вопрос: 30 секунд. \n
4. Чтобы посмотреть общий счёт (все игры) - нажми "Показать счёт"'''
)
