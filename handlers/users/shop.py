from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError

from core.utils.shortcuts import create_barcode
from keyboards.inline import ShopInlineKeyboardMarkup, ShopCallbackData
from states import CardAddStatesGroup, CardEditStatesGroup
from core.utils.database import UserCard, session
from settings import bot


__all__ = ["router"]

router = Router()


@router.message(F.text == "МОИ КАРТОЧКИ 💳")
async def shops(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    await message.answer(
        text="Выберите магазин!",
        reply_markup=ShopInlineKeyboardMarkup.list(user_id=message.from_user.id)
    )


@router.callback_query(ShopCallbackData.filter(F.action == "back"))
async def back_to_shop_list(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        text="Выберите магазин!",
        reply_markup=ShopInlineKeyboardMarkup.list(user_id=callback.from_user.id)
    )


@router.callback_query(ShopCallbackData.filter(F.action == "edit"))
async def edit_card(callback: CallbackQuery, callback_data: ShopCallbackData, state: FSMContext):
    await state.clear()
    await state.set_state(CardEditStatesGroup.barcode)
    await state.update_data(shop=callback_data.shop)
    await callback.message.delete()
    await callback.message.answer(
        text="Введите новый номер карты!",
        reply_markup=ShopInlineKeyboardMarkup.back(shop=callback_data.shop)
    )


@router.message(CardEditStatesGroup.barcode)
async def get_new_card_number(message: Message, state: FSMContext):
    await message.delete()
    barcode = message.text.replace(" ", "")
    if barcode.isdigit():
        state_data = await state.get_data()
        await state.clear()
        with session() as s:
            s.execute(
                update(UserCard)
                .values(barcode=message.text)
                .filter_by(
                    shop=state_data.get("shop"),
                    user_id=message.from_user.id
                )
            )
            s.commit()
            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except TelegramBadRequest:
                pass
            barcode_image = create_barcode(
                barcode=barcode,
                shop=state_data.get("shop")
            )
            await message.answer_photo(
                photo=BufferedInputFile(
                    file=barcode_image.read(),
                    filename=f"{message.text}.png"
                ),
                caption=f"<b>{state_data.get('shop')}</b>",
                reply_markup=ShopInlineKeyboardMarkup.edit(
                    callback_data=ShopCallbackData(
                        shop=state_data.get("shop"),
                        action="get"
                    )
                )
            )
    else:
        await message.answer(
            text="Допустимы только числа"
        )


@router.callback_query(ShopCallbackData.filter(F.action == "delete"))
async def delete_card(callback: CallbackQuery, callback_data: ShopCallbackData):
    with session() as s:
        s.execute(
            delete(UserCard)
            .filter_by(
                user_id=callback.from_user.id,
                shop=callback_data.shop
            )
        )
        s.commit()
    await callback.message.delete()
    await callback.message.answer(
        text="Карта удалена, можете добавить новую!",
        reply_markup=ShopInlineKeyboardMarkup.add(callback_data=callback_data)
    )


@router.callback_query(ShopCallbackData.filter(F.action == "get"))
async def get_shop_card(callback: CallbackQuery, callback_data: ShopCallbackData):
    with (session() as s):
        user_card = s.scalar(
            select(UserCard).filter_by(
                user_id=callback.from_user.id,
                shop=callback_data.shop
            )
        )
        try:
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id - 1
            )
        except TelegramBadRequest:
            pass
        if user_card is not None:
            barcode_image = create_barcode(barcode=user_card.barcode, shop=user_card.shop)
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=BufferedInputFile(
                    file=barcode_image.read(),
                    filename=f"{user_card.barcode}.png"
                ),
                caption=f"<b>{user_card.shop}</b>",
                reply_markup=ShopInlineKeyboardMarkup.edit(
                    callback_data=callback_data
                )
            )
        else:
            await callback.message.edit_text(
                text="У вас еще нет карты данного магазина!",
                reply_markup=ShopInlineKeyboardMarkup.add(
                    callback_data=callback_data
                )
            )


@router.callback_query(ShopCallbackData.filter(F.action == "add"))
async def add_card(callback: CallbackQuery, callback_data: ShopCallbackData, state: FSMContext):
    await state.clear()
    await state.set_state(CardAddStatesGroup.barcode)
    await state.update_data(shop=callback_data.shop)
    await callback.message.edit_text(
        text=f"Введите номер карты магазина {callback_data.shop}"
    )


@router.message(CardAddStatesGroup.barcode)
async def get_barcode(message: Message, state: FSMContext):
    await message.delete()
    barcode = message.text.replace(" ", "")
    if barcode.isdigit():
        state_data = await state.get_data()
        await state.clear()
        with session() as s:
            user_card = UserCard(
                user_id=message.from_user.id,
                shop=state_data.get("shop"),
                barcode=message.text.replace(" ", "")
            )
            s.add(user_card)
            try:
                s.commit()
            except IntegrityError:
                await message.answer(
                    text="Неизвестная ошибка, обратитесь к разработчику!"
                )
            else:
                barcode_image = create_barcode(
                    barcode=barcode,
                    shop=state_data.get("shop")
                )
                await message.answer_photo(
                    photo=BufferedInputFile(
                        file=barcode_image.read(),
                        filename=f"{message.text}.png"
                    ),
                    caption=f"<b>{user_card.shop}</b>",
                    reply_markup=ShopInlineKeyboardMarkup.edit(
                        callback_data=ShopCallbackData(
                            shop=state_data.get("shop"),
                            action="get"
                        )
                    )
                )
    else:
        await message.answer(
            text="Допустимы только числа"
        )
