from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='➕ Добавить задачу')]
],
    resize_keyboard=True)

remove = ReplyKeyboardRemove()
