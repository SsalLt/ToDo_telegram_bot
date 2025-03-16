from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN, logger
from app.handlers import router


async def start_polling():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info('Bot started.')
        asyncio.run(start_polling())
    except KeyboardInterrupt:
        logger.info('Bot stopped.')
        exit(1)
