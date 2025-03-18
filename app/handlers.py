from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import logger
import app.keyboards as kb
import app.database.requests_db as rq

router = Router()


class AddTaskState(StatesGroup):
    task_text = State()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await rq.set_user(tg_id=message.from_user.id)
    await state.clear()
    await message.answer(
        text=f"Привет, {message.from_user.full_name}!\nЭто бот для управления задачами.",
        reply_markup=kb.main)


@router.message(F.text == "Назад ↩")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Вы вернулись в главное меню.", reply_markup=kb.main)
    logger.debug('back_to_main command')


@router.message(F.text == '➕ Добавить задачу')
@router.message(Command("add"))
async def add_task(message: Message, state: FSMContext):
    await state.set_state(AddTaskState.task_text)
    await message.answer(text="Введите текст новой задачи:", reply_markup=kb.back_to_main)
    logger.debug('add_task command')


@router.message(AddTaskState.task_text)
async def task_text_process(message: Message, state: FSMContext):
    logger.debug('task_text_process command')
    await state.update_data(task_text=message.text)
    state_data: dict = await state.get_data()
    await rq.set_task(tg_id=message.from_user.id, task=state_data.get("task_text"))
    await message.reply(text=f"✅ Задача добавлена!", reply_markup=kb.main)
    await state.clear()


@router.message(F.text == "📋 Список задач")
@router.message(Command('list_tasks'))
async def list_tasks(message: Message, state: FSMContext):
    user_tg_id = message.from_user.id
    tasks = await kb.tasks(tg_id=user_tg_id)
    if tasks is None:
        await message.answer(text="У вас ещё нет ни одной задачи!\n"
                                  "Для добавления задачи воспользуйтесь командой /add или соответствующей кнопкой.")
        return
    await message.answer(text="Список ваших задач:",
                         reply_markup=tasks)
