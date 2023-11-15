from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.database import session, User
from keyboards.reply import main_rkb

__all__ = ["router"]

router = Router()


@router.message(F.text == "/start")
async def start_message(message: Message, state: FSMContext):
    await state.clear()
    with session() as s:
        user = s.get(User, message.from_user.id)
        if user is None:
            user = User(id=message.from_user.id)
            s.add(user)
            s.commit()
            text = "Привет, я Бот для хранения и управления дисконтными картами магазинов!"
        else:
            text = "Привет, давно не виделись!"
        await message.answer(
            text=text,
            reply_markup=main_rkb
        )
