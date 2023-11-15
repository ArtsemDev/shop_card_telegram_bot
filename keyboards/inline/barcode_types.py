from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.utils.database import BarcodeType, session

__all__ = [
    "barcode_type_ikb"
]


def barcode_type_ikb() -> InlineKeyboardMarkup:
    with session() as s:
        barcode_types = s.query(BarcodeType).all()
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=barcode_type.name.upper(),
                    callback_data=barcode_type.name
                )
            ]
            for barcode_type in barcode_types
        ]
    )
