from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.requests_db as rq

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Добавить задачу")],
    [KeyboardButton(text="📋 Список задач")]
],
    resize_keyboard=True)

remove = ReplyKeyboardRemove()


async def tasks(tg_id: int) -> InlineKeyboardMarkup:
    tasks = await rq.get_tasks(tg_id=tg_id)
    keyboard = InlineKeyboardBuilder()
    for task in tasks:
        keyboard.add(InlineKeyboardButton(text=task.text, callback_data=f'task_{task.id}'))
    return keyboard.adjust(1).as_markup()
