from .sqlitedb import DB
import config_data

db = DB(config_data.config.db.database) # Инициализация базы данных