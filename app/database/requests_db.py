from app.database.models import async_session, User, Task
from sqlalchemy import select, update, delete, ScalarResult


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_tasks(tg_id: int) -> ScalarResult[Task]:
    async with async_session() as session:
        user: User | None = await session.scalar(select(User).where(User.tg_id == tg_id))
        tasks: ScalarResult[Task] = await session.scalars(select(Task).where(Task.user_id == user.id))
        return tasks
