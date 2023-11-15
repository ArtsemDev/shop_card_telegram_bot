from typing import Literal, Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select

from core.utils.database import session, Shop, UserCard

__all__ = [
    "ShopCallbackData",
    "ShopInlineKeyboardMarkup"
]


class ShopCallbackData(CallbackData, prefix="shop"):
    shop: Optional[str] = None
    action: Literal["get", "add", "delete", "edit", "back"]


class ShopInlineKeyboardMarkup:

    @classmethod
    def list(cls, user_id: int) -> InlineKeyboardMarkup:
        with session() as s:
            shops = s.scalars(select(Shop).order_by(Shop.name.asc())).all()
            user_cards = s.scalars(select(UserCard.shop).filter_by(user_id=user_id)).all()
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=f"{shop.name.upper()} {'✔️' if shop.name in user_cards else '✖️'}",
                            callback_data=ShopCallbackData(
                                shop=shop.name,
                                action="get"
                            ).pack()
                        )
                    ]
                    for shop in shops
                ]
            )

    @classmethod
    def add(cls, callback_data: ShopCallbackData) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="ДОБАВИТЬ ➕",
                        callback_data=ShopCallbackData(
                            shop=callback_data.shop,
                            action="add"
                        ).pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ НАЗАД",
                        callback_data=ShopCallbackData(
                            action="back"
                        ).pack()
                    )
                ]
            ]
        )

    @classmethod
    def edit(cls, callback_data: CallbackData) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="ИЗМЕНИТЬ ✏️",
                        callback_data=ShopCallbackData(
                            shop=callback_data.shop,
                            action="edit"
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text="УДАЛИТЬ ❌",
                        callback_data=ShopCallbackData(
                            shop=callback_data.shop,
                            action="delete"
                        ).pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ НАЗАД",
                        callback_data=ShopCallbackData(
                            action="back"
                        ).pack()
                    )
                ]
            ]
        )

    @classmethod
    def back(cls, shop: str = None) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ НАЗАД",
                        callback_data=ShopCallbackData(
                            action="get" if shop is not None else "back",
                            shop=shop
                        ).pack()
                    )
                ]
            ]
        )
