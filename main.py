import os
from random import randint
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()

users = {}
ATTEMPTS = 5

def get_random_number() -> int:
    return randint(1, 100)

def get_users(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "in_game": False,
            "secret_number": 0,
            "attempts": 0,
            "games": 0,
            "wins": 0
        }
    return users[message.from_user.id]

@dp.message(CommandStart())
async def star_bot(message: Message):
    get_users(message)
    await message.answer('Привет. Поиграем?')

@dp.message(Command(commands= "help"))
async def help_bot(message: Message):
    get_users(message)
    await message.answer("Ни чем помочь не могу. Разбирайся сам)")

@dp.message(Command(commands="stat"))
async def stat_user_bot(message: Message):
    await message.answer(f"Ты сыграл {users[message.from_user.id]["games"]} игр. \
                         \nИз них ты выиграл {users[message.from_user.id]["wins"]}.")

@dp.message(Command(commands="cancel"))
async def cancel_game_bot(message: Message):
    if users[message.from_user.id]["wins"]:
        users[message.from_user.id]["wins"] = False
        await message.answer("Вы вышли из игры. \
                             \nЕсли захотите сыграть снова - напишите об этом")
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )

@dp.message(F.text.lower().in_(["да"]))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]["in_game"]:
        users[message.from_user.id]["in_game"] = True
        users[message.from_user.id]["secret_number"] = get_random_number()
        users[message.from_user.id]["attempts"] = ATTEMPTS
        await message.reply("ИГРА НАЧАЛАСЬ! \
                            \nЯ загадал число от 1 до 100, попробуй угадать!")
    else:
        await message.answer("Мы же и так играем...")

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}'
                f'\n\nДавайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

if __name__ == '__main__':
    dp.run_polling(bot)