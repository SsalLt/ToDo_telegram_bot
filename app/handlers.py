from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import logger

router = Router()


class AddTaskState(StatesGroup):
    task_name = State()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}!\nThis is a ToDo List bot.")


@router.message(F.text == '➕Добавить задачу')
@router.message(Command("add"))
async def add_task(message: Message, state: FSMContext):
    await state.set_state(AddTaskState.task_name)
    await message.answer("Введите текст новой задачи:")


@router.message(AddTaskState.task_name)
async def task_name_process(message: Message, state: FSMContext):
    await state.update_data(message.text)
    state_data: dict = await state.get_data()
    # await add_task_to_bd(task=state_data.get("task_name"))
    await message.reply(f"Задача добавлена.")
    await state.clear()
