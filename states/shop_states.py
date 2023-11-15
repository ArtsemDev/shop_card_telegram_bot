from aiogram.fsm.state import StatesGroup, State


__all__ = ["ShopAddStatesGroup"]


class ShopAddStatesGroup(StatesGroup):
    shop = State()
    barcode_type = State()
