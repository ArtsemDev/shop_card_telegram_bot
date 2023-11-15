from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters import IsAdmin
from states import ShopAddStatesGroup
from keyboards.inline import barcode_type_ikb
from core.utils.database import Shop, session

__all__ = ["router"]


router = Router()


@router.message(IsAdmin(), F.text == "/add_shop")
async def add_shop(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    await state.set_state(ShopAddStatesGroup.shop)
    await message.answer(
        text="Введите название магазина"
    )


@router.message(ShopAddStatesGroup.shop)
async def get_shop(message: Message, state: FSMContext):
    await message.delete()
    with session() as s:
        shop = s.get(Shop, message.text.upper())
        if shop is None:
            await state.update_data(shop=message.text.upper())
            await state.set_state(ShopAddStatesGroup.barcode_type)
            await message.answer(
                text="Выберите протокол",
                reply_markup=barcode_type_ikb()
            )
        else:
            await message.answer(
                text="Данный магазин уже существует!"
            )


@router.callback_query(ShopAddStatesGroup.barcode_type)
async def get_barcode_type(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await state.clear()
    with session() as s:
        shop = Shop(
            name=state_data.get("shop"),
            barcode_type=callback.data
        )
        s.add(shop)
        s.commit()
    await callback.message.edit_text(
        text="МАГАЗИН ЗАПИСАН"
    )
