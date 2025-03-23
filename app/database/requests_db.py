from datetime import datetime
from sqlalchemy.orm import Mapped
from app.database.models import async_session, User, Task
from sqlalchemy import select, update, delete, ScalarResult


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, user_sort_preferences="sort_first_old_ones"))
            await session.commit()


async def get_tasks(tg_id: int) -> ScalarResult[Task]:
    async with async_session() as session:
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        tasks: ScalarResult[Task] = await session.scalars(select(Task).where(Task.user == user.id))
        return tasks


async def set_task(tg_id: int, task: str) -> None:
    async with async_session() as session:
        current_date = datetime.now().strftime("%d.%m.%Y / %H:%M")
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Task(text=task, user=user.id, status=False, created_at=current_date))
        await session.commit()


async def get_task_by_id(task_id: int) -> Task | None:
    async with async_session() as session:
        task: Task | None = await session.scalar(select(Task).where(Task.id == task_id))
        return task


async def update_task_status(task_id: int, new_status: bool) -> None:
    async with async_session() as session:
        task: Task | None = await session.scalar(select(Task).where(Task.id == task_id))
        if task:
            await session.execute(update(Task).where(Task.id == task_id).values(status=new_status))
            await session.commit()


async def edit_task_text(task_id: int, new_text: str) -> None:
    async with async_session() as session:
        task: Task | None = await session.scalar(select(Task).where(Task.id == task_id))
        if task:
            await session.execute(update(Task).where(Task.id == task_id).values(text=new_text))
            await session.commit()


async def delete_task(task_id: int) -> None:
    async with async_session() as session:
        task: Task | None = await session.scalar(select(Task).where(Task.id == task_id))
        if task:
            await session.execute(delete(Task).where(Task.id == task_id))
            await session.commit()


async def delete_all_completed_tasks() -> None:
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.status == True))
        await session.commit()


async def get_sort_preferences(tg_id: int) -> Mapped[str] | str:
    async with async_session() as session:
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.user_sort_preferences


async def update_sort_preferences(tg_id: int) -> None:
    async with async_session() as session:
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        sort_mode: str = "sort_first_old_ones" if "new" in user.user_sort_preferences else "sort_first_new_ones"
        await session.execute(update(User).where(User.tg_id == tg_id).values(user_sort_preferences=sort_mode))
        await session.commit()
