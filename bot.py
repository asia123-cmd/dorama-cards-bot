
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from cards import get_random_card
from database import (
    init_db,
    add_card,
    get_collection,
    get_top_players,
    get_user_total_cards,
    get_user_unique_cards,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="🎴 Получить карточку")
    builder.button(text="📚 Моя коллекция")
    builder.button(text="🎁 Бонус")
    builder.button(text="🏆 Топ игроков")
    builder.button(text="⚙️ Профиль")

    builder.adjust(1, 1, 2, 1)

    return builder.as_markup(
        resize_keyboard=True
    )


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🌸 Добро пожаловать в Dorama Cards!\n\n"
        "Здесь ты можешь собирать карточки персонажей "
        "из любимых дорам.\n\n"
        "🎴 Нажми «Получить карточку», чтобы начать!",
        reply_markup=main_keyboard(),
    )


@dp.message(F.text == "🎴 Получить карточку")
async def get_card_handler(message: Message):
    card = get_random_card()

    is_new = await add_card(
        user_id=message.from_user.id,
        card_id=card["id"],
    )

    if is_new:
        status = "✨ Новая карточка!"
    else:
        status = "🔁 Дубликат!"

    await message.answer(
        f"{status}\n\n"
        f"🎴 Карточка #{card['id']}\n"
        f"👤 {card['character']}\n"
        f"🎬 {card['drama']}\n"
        f"⭐ Редкость: {card['rarity']}"
    )


@dp.message(F.text == "📚 Моя коллекция")
async def collection_handler(message: Message):
    collection = await get_collection(message.from_user.id)

    if not collection:
        await message.answer(
            "📚 Твоя коллекция пока пуста.\n"
            "Нажми «🎴 Получить карточку»!"
        )
        return

    text = "📚 Твоя коллекция:\n\n"

    for card_id, count in collection:
        text += f"🎴 #{card_id} × {count}\n"

    total = await get_user_total_cards(message.from_user.id)
    unique = await get_user_unique_cards(message.from_user.id)

    text += (
        f"\n✨ Уникальных карт: {unique}\n"
        f"🎴 Всего карт: {total}"
    )

    await message.answer(text)


@dp.message(F.text == "🎁 Бонус")
async def bonus_handler(message: Message):
    await message.answer(
        "🎁 Бонусная система пока находится в разработке!\n\n"
        "Скоро здесь можно будет получать дополнительные карты."
    )


@dp.message(F.text == "🏆 Топ игроков")
async def top_handler(message: Message):
    top = await get_top_players()

    if not top:
        await message.answer("🏆 Пока игроков нет.")
        return

    text = "🏆 Топ игроков:\n\n"

    for position, (user_id, total) in enumerate(top, start=1):
        text += f"{position}. ID {user_id} — 🎴 {total} карт\n"

    await message.answer(text)


@dp.message(F.text == "⚙️ Профиль")
async def profile_handler(message: Message):
    total = await get_user_total_cards(message.from_user.id)
    unique = await get_user_unique_cards(message.from_user.id)

    await message.answer(
        "⚙️ Твой профиль\n\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"🎴 Всего карт: {total}\n"
        f"✨ Уникальных: {unique}"
    )


async def main():
    await init_db()

    logging.info("Dorama Cards bot is starting...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
