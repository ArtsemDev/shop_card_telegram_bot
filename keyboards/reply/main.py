from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


__all__ = ["main_rkb"]

main_rkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [
            KeyboardButton(
                text="МОИ КАРТОЧКИ 💳"
            )
        ]
    ]
)
