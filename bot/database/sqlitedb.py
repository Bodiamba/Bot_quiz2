import sqlite3
import game

class DB:
    database_name: str

    def __init__(self, database_name: str):
        self.database_name = database_name

        """Создаёт таблицу, если не создана. """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
        conn.close()

    def add_user(self, tg_id: int, username: str, score: int=0) -> bool:
        """Добавляет нового пользователя в таблицу users. """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (tg_id, username, score) VALUES (?, ?, ?)
                """,
                (tg_id, username, score),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def load_users_to_dict(self) -> dict:
        """Загружает данные всех пользователей из таблицы userscores в словарь. """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT tg_id, username, score FROM users
            """
        )
        participants = {}
        for row in cursor.fetchall():
            tg_id, username, score = row
            participants[int(tg_id)] = game.Participant(username, int(tg_id), int(score))
        conn.close()
        return participants

    def update_user_score(self, tg_id: int, score: int) -> bool:
        """Обновляет счет пользователя в базе данных. """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE users SET score = ? WHERE tg_id = ?
                """,
                (score, tg_id),
            )
            if cursor.rowcount == 0:
                # Пользователь не найден в базе данных
                conn.close()
                return False
            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False
        
    def delete_user(self, tg_id: int) -> bool:
        """ Удаляет пользователя из базы данных. """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM users WHERE tg_id = ?
                """,
                (tg_id,),
            )
            if cursor.rowcount == 0:
                # Пользователь не найден в базе данных
                conn.close()
                return False
            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False