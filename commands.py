
import model
from create_bot import bot
from aiogram import types
from random import random

async def start(message: types.Message):
    model.setCount(int(model.getUserCount()))
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}!\n'
                                                 f'Это игра про конфеты! Введи /help, если тебе '
                                                 f'что-нибудь непонятно или нужно объяснить правила!\n'
                                                 f'/run - чтобы немедленно начать!')
async def run(message: types.Message):
    model.setCount(int(model.getUserCount()))
    await bot.send_message(message.from_user.id, f'Всего конфет {model.getCount()}')
    model.setFirstTurn()
    first_turn = model.getFirstTurn()
    if first_turn:
        await bot.send_message(message.from_user.id, f'Первый ход за {message.from_user.username}!\n')
        await playerTake(message)
    else:
        await bot.send_message(message.from_user.id, 'Первый ход за ботом!\n')
        await enemyTurn(message)

async def help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Хватай конфеты! Побеждает игрок, '
                                                 'который заберёт последние конфеты, '
                                                 'брать за ход можно от 1 до 28 конфет\n'
                                                #  '/set_count - изменить кол-во начальных конфет\n'
                                                 '/run - начать игру')


# async def set_count(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Сколько конфет оставить на столе? ')
#     count = message.text.split()
#     if len(count) == 2:
#         model.setUserCount(int(count[1]))
#     await bot.send_message(message.from_user.id, f'Стартовое количество конфет изменено '
#                                                  f'на {model.getUserCount()}')

async def playerTake(message: types.Message):
    await bot.send_message(message.from_user.id, f'{message.from_user.username}, '
                                                 f'бери конфеты, но не более 28 шт')

async def playerTurn(message: types.Message):
    take = None
    if message.text.isdigit():
        if not 0 < int(message.text) < 29:
            await bot.send_message(message.from_user.id, f'Эй! Можно взять от 1 до 28 конфет!')
        else:
            take = int(message.text)
            model.setTake(int(message.text))
            model.setCount(model.getCount() - take)
            await bot.send_message(message.from_user.id, f'{message.from_user.username}, '
                                                         f'взял {take} конфет, осталось'
                                                         f'{model.getCount()}')
            if model.checkWin():
                await bot.send_message(message.from_user.id, f'Победа {message.from_user.username}!')
                return
            await enemyTurn(message)
    else:
        await bot.send_message(message.from_user.id, f'{message.from_user.username}, '
                                                         f'Введите число')


async def enemyTurn(message: types.Message):
    count = model.getCount()
    take = count%29 if count%29 != 0 else random.randint(1,28)
    model.setTake(take)
    model.setCount(count - take)
    await bot.send_message(message.from_user.id, f'Бот взял {model.getTake()} конфет, '
                                                 f'осталось {model.getCount()}')
    if model.checkWin():
        await bot.send_message(message.from_user.id, 'Бот победил! Подсказать, как победить? '
                                                     'Введи команду /How_Win, чтобы узнать!')
        return
    await playerTake(message)

async def howWin(message: types.Message):
    await bot.send_message(message.from_user.id, 'Всё просто! Главное начать ходить первым. '
                                                 'Смотри, всегда дели оставшиеся конфеты на '
                                                 'максимум, который позволено взять и + 1 конфета. '
                                                 'Бери остаток от этого деления и победа твоя! '
                                                 '(например 150/29 --> 5, 60/29 --> 2)')