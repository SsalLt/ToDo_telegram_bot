from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import logger
import app.keyboards as kb
import app.database.requests_db as rq

router = Router()


class TaskState(StatesGroup):
    add_task_text = State()
    edit_task_text = State()


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
    await state.set_state(TaskState.add_task_text)
    await message.answer(text="Введите текст новой задачи:", reply_markup=kb.back_to_main)
    logger.debug('add_task command')


@router.message(TaskState.add_task_text, F.text)
async def process_add_task_text(message: Message, state: FSMContext):
    logger.debug('task_text_process command')
    await message.answer(text="⏳ Добавляю задачу...")
    await rq.set_task(tg_id=message.from_user.id, task=message.text)
    await message.reply(text=f"✅ Задача добавлена!", reply_markup=kb.main)
    await state.clear()


async def process_tasks_list(ctx: Message | CallbackQuery) -> None:
    user_sort_preference = await rq.get_sort_preferences(tg_id=ctx.from_user.id)
    sort_mode = True if "old" in user_sort_preference else False
    tasks = await kb.tasks(tg_id=ctx.from_user.id, sort_mode=sort_mode)
    if isinstance(ctx, Message):
        if tasks is None:
            await ctx.answer(text="📋 *Список задач пуст.*\n"
                                  "Для добавления задачи воспользуйтесь командой /add или соответствующей кнопкой.",
                             parse_mode="Markdown")
            return
        await ctx.answer(
            text="📋 *Список задач:*",
            reply_markup=tasks,
            parse_mode="Markdown"
        )
    elif isinstance(ctx, CallbackQuery):
        await ctx.answer()
        if tasks is None:
            await ctx.message.edit_text(
                text="📋 *Список задач пуст.*\n"
                     "Для добавления задачи воспользуйтесь командой /add или соответствующей кнопкой.",
                parse_mode="Markdown")
            return
        await ctx.message.edit_text(
            text="📋 *Список задач:*",
            reply_markup=tasks,
            parse_mode="Markdown"
        )


@router.message(F.text == "📋 Список задач")
@router.message(Command('my_tasks'))
async def list_tasks(message: Message):
    await process_tasks_list(ctx=message)


@router.callback_query(F.data.startswith("task_"))
async def view_the_task(callback: CallbackQuery):
    task_id: int = int(callback.data.split("_")[1])
    task = await rq.get_task_by_id(task_id=task_id)

    if task is None:
        await callback.message.answer(text="Ошибка! Задача не найдена.")
        return
    task_menu = await kb.create_task_menu_kb(task_id=task_id, is_completed=task.status)
    await callback.answer()
    await callback.message.edit_text(
        text=f"{"📌" if not task.status else "✅"} | *{task.text}* |\n"
             f"📅 Создано: _{task.created_at}_\n"
             f"📊 Статус: _{'Выполнено' if task.status else 'Не выполнено'}_",
        reply_markup=task_menu,
        parse_mode="Markdown"
    )


@router.callback_query(F.data == 'back_to_list')
async def back_to_list(callback: CallbackQuery):
    await process_tasks_list(ctx=callback)


@router.callback_query(F.data.startswith("complete_"))
async def complete_task(callback: CallbackQuery):
    task_id: int = int(callback.data.split("_")[1])
    task = await rq.get_task_by_id(task_id=task_id)
    await rq.update_task_status(task_id=task_id, new_status=not task.status)
    await process_tasks_list(ctx=callback)


@router.callback_query(F.data.startswith("edit_"))
async def edit_task(callback: CallbackQuery, state: FSMContext):
    task_id: int = int(callback.data.split("_")[1])
    await state.update_data(task_id=task_id)
    await state.set_state(TaskState.edit_task_text)
    await callback.answer()
    await callback.message.answer(text="Введите новый текст для задачи:", reply_markup=kb.back_to_main)


@router.message(TaskState.edit_task_text, F.text)
async def process_edit_task_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    task_id = state_data.get("task_id")
    await rq.edit_task_text(task_id=task_id, new_text=message.text)
    await message.reply(text="✍ Текст задачи обновлён!", reply_markup=kb.main)
    await state.clear()


@router.callback_query(F.data.startswith("delete_"))
async def delete_task(callback: CallbackQuery):
    task_id: int = int(callback.data.split("_")[1])
    task = await rq.get_task_by_id(task_id=task_id)
    if task is None:
        await callback.message.edit_text(text="Ошибка! Задача не найдена.")
        return
    await callback.answer()
    await callback.message.edit_text(
        text=f"Действительно удалить задачу | *{task.text}* | ?",
        reply_markup=await kb.confirm_delete_kd(task_id=task_id),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith("confirm_delete_task_"))
async def confirm_delete(callback: CallbackQuery):
    task_id: int = int(callback.data.split("_")[3])
    await rq.delete_task(task_id=task_id)
    await process_tasks_list(ctx=callback)


@router.callback_query(F.data.startswith("cancel_delete_task_"))
async def cancel_delete(callback: CallbackQuery):
    task_id: int = int(callback.data.split("_")[3])
    task = await rq.get_task_by_id(task_id=task_id)
    task_menu = await kb.create_task_menu_kb(task_id=task_id, is_completed=task.status)
    await callback.answer()
    await callback.message.edit_text(
        text=f"{"📌" if not task.status else "✅"} | *{task.text}* |\n"
             f"📅 Создано: _{task.created_at}_\n"
             f"📊 Статус: _{'Выполнено' if task.status else 'Не выполнено'}_",
        reply_markup=task_menu,
        parse_mode="Markdown"
    )


@router.message(F.text == "🚮 Удалить выполненные задачи")
@router.message(Command('delete'))
async def delete_completed_tasks(message: Message):
    await message.answer("Вы уверены, что хотите удалить все выполненные задачи?",
                         reply_markup=kb.confirm_delete_completed_tasks_kb)


@router.callback_query(F.data == "confirm_delete_completed_tasks")
async def confirm_delete_completed_tasks(callback: CallbackQuery):
    await rq.delete_all_completed_tasks()
    await callback.answer()
    await callback.message.edit_text(text="♻ Выполненные задачи удалены!")


@router.callback_query(F.data == "cancel_delete_completed_tasks")
async def cancel_delete_completed_tasks(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="⛔ Удаление выполненных задач отменено.")


@router.callback_query(F.data == "switch_sort_mode")
async def switch_sort_mode(callback: CallbackQuery):
    await rq.update_sort_preferences(tg_id=callback.from_user.id)
    await process_tasks_list(ctx=callback)
