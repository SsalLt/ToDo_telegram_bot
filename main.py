from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN


async def start_polling():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_polling())
        print('Bot started...')
    except KeyboardInterrupt:
        print('Bot stopped...')
        exit(1)
