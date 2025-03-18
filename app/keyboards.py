from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.requests_db as rq
from config import logger

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Добавить задачу")],
    [KeyboardButton(text="📋 Список задач")]
],
    resize_keyboard=True)

remove = ReplyKeyboardRemove()

back_to_main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад ↩")]],
    resize_keyboard=True
)


async def tasks(tg_id: int) -> InlineKeyboardMarkup | None:
    tasks = await rq.get_tasks(tg_id=tg_id)
    keyboard = InlineKeyboardBuilder()
    tasks_lst: list = []
    for task in tasks:
        keyboard.add(InlineKeyboardButton(text=task.text, callback_data=f'task_{task.id}'))
        tasks_lst.append(f'task_{task.id}')
    logger.debug(tasks_lst)
    if not tasks_lst:
        return None
    return keyboard.adjust(1).as_markup()
