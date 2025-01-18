class Participant:
    ''' Класс, описывающий состояние участника викторины '''
    def __init__(self, name: str, id: int, score:int=0):
        self.name = name
        self.id = id
        self.inroom = False
        self.score = score
        self.game_score = 0
        self.room = None
        self.answer = None
        self.answered = False

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_answered(self) -> bool:
        return self.answered

    def set_answered(self) -> None:
        self.answered = True

    def clear_answered(self) -> None:
        self.answered = False

    def set_room(self, room) -> None:
        self.room = room

    def get_room(self) -> str:
        return self.room

    def set_registered(self, registered) -> None:
        self.registered = registered

    def get_registered(self) -> bool:
        return self.registered

    def get_answer(self) -> int | str:
        return self.answer

    def set_answer(self, answer) -> None:
        self.answer = answer

    def clear_answer(self) -> None:
        self.answer = None

    def increment_score(self) -> None:
        self.score += 1

    def clear_score(self) -> None:
        self.score = 0

    def get_score(self) -> int:
        return self.score

    def increment_game_score(self) -> None:
        self.game_score += 1

    def clear_game_score(self) -> None:
        self.game_score = 0

    def get_game_score(self) -> int:
        return self.game_score