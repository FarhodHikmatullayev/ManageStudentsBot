from aiogram.dispatcher.filters.state import StatesGroup, State


class CreatePenaltyBallState(StatesGroup):
    student_id = State()
    rated_by_id = State()
    ball = State()


class GetPenaltyBallState(StatesGroup):
    period = State()
