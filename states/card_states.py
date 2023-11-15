from aiogram.fsm.state import StatesGroup, State


__all__ = [
    "CardEditStatesGroup",
    "CardAddStatesGroup"
]


class CardAddStatesGroup(StatesGroup):
    barcode = State()


class CardEditStatesGroup(StatesGroup):
    barcode = State()
