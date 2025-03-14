from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio
import os


async def start_polling():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_polling())
        print('Bot started...')
    except KeyboardInterrupt:
        print('Bot stopped...')
        exit(1)
