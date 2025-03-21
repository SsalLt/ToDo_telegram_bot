from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Mapped

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


async def confirm_delete_keyboard(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"confirm_delete_{task_id}"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"cancel_delete_{task_id}")
        ]
    ])


async def create_task_menu_kb(task_id: int, is_completed: bool | Mapped[bool]) -> InlineKeyboardMarkup:
    status_text = '🏅 Пометить как "Выполнено"' if not is_completed else '🚫 Пометить как "Не выполнено"'
    task_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=status_text, callback_data=f'complete_{task_id}')],
        [InlineKeyboardButton(text='✏ Изменить текст', callback_data=f'edit_{task_id}'),
         InlineKeyboardButton(text='🗑 Удалить задачу', callback_data=f'delete_{task_id}')],
        [InlineKeyboardButton(text='Назад ↩', callback_data='back_to_list')]
    ])
    return task_menu


async def tasks(tg_id: int) -> InlineKeyboardMarkup | None:
    tasks = await rq.get_tasks(tg_id=tg_id)
    keyboard = InlineKeyboardBuilder()
    tasks_lst: list = []
    for task in tasks:
        task_status = task.status
        text = f'{task.text[:20]}...' if len(task.text) > 20 else task.text
        text = f"📌 {text}" if not task_status else f"✅ {text}"
        keyboard.add(InlineKeyboardButton(text=text, callback_data=f'task_{task.id}'))
        tasks_lst.append(f'task_{task.id}')
    if not tasks_lst:
        return None
    return keyboard.adjust(1).as_markup()
