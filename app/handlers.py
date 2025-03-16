from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router, Bot

from config import logger

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}!\nThis is a ToDo List bot.")
