import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.answer("Привет!\nПо играем?")

@dp.message(Command(commands="help"))
async def help_bot(message: Message):
    await message.answer("Я эхо-бот!\nБуду отправлять тебе тоже самое, что и ты мне отправляешь)))")

@dp.message()
async def send_echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)

if __name__ == "__main__":
    dp.run_polling(bot)
