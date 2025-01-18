from .fsm import QuizFSM, FSM, StateFilter

quiz_fsm = QuizFSM(FSM, StateFilter(FSM.waiting_for_confirmation))