class Question:
    def __init__(self, id: int, question: str, answer: int | str, answers: list):
        self.id = id
        self.question = question
        self.answer = answer
        self.answers = answers

    ''' Получить ID вопроса '''
    def get_id(self) -> int:
        return self.id
    ''' Получить вопрос '''
    def get_question(self) -> str:
        return self.question
    ''' Получить правильный ответ '''
    def get_answer(self) -> int | str:
        return self.answer
    ''' Получить набор всех ответов '''
    def get_answers(self) -> list:
        return self.answers
