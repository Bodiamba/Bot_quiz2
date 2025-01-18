class TgBot:
    token: str

    def __init__(self, token: str):
        self.token = token

class DatabaseConfig:
    database:str # Путь к таблице БД

    def __init__(self, database: str):
        self.database = database

class GoogleTable:
    service_account_file: str # Путь к JSON-файлу с учётными данными сервисного аккаунта
    spreadsheet_id: str # ID google таблицы

    def __init__(self, service_account_file: str, spreadsheet_id: str):
        self.service_account_file = service_account_file
        self.spreadsheet_id = spreadsheet_id

class Btns:
    btn_reg: str # кнопка регистрации
    btn_start_quiz: str # кнопка старта викторины
    btn_show_score: str # кнопка отображения счёта
    btn_show_participants: str # кнопка отображения участников

    def __init__(self, btn_reg: str, btn_start_quiz: str, btn_show_score: str, btn_show_participants: str):
        self.btn_reg = btn_reg
        self.btn_start_quiz = btn_start_quiz
        self.btn_show_score = btn_show_score
        self.btn_show_participants = btn_show_participants

class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    gt: GoogleTable
    btns: Btns
    helpmsg: str

    def __init__(self, tg_bot: TgBot, db: DatabaseConfig, gt: GoogleTable, btns: Btns, helpmsg: str):
        self.tg_bot = tg_bot
        self.db = db
        self.gt = gt
        self.btns = btns
        self.helpmsg = helpmsg
