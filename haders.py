from aiogram import F, Dispatcher, Bot, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
import asyncio

from avito_parce import one_avito_parse, prefix



rt_avito = Router()

#prefix = "fRmzq"
secret_id = ["1086225549", "5271211921",]
search = "отдам+бесплатно"

@rt_avito.message(Command('start'))
async def avito_start(message: types.Message):
    global secret_id
    if str(message.from_user.id) not in secret_id: # type: ignore
        await message.answer(f"{message.from_user.first_name} у вас нет прав пользоваться ботом!!! 🤔 \n ваш id {message.from_user.id}") # type: ignore
    else:
        await message.answer(f"Привет {message.from_user.first_name} собираем информацию для стартового листа!!!\n ваш id {message.from_user.id}") # type: ignore
        while True:
            avito_dict = one_avito_parse(search)
            if not avito_dict:
                #print ("пока ничего")
                pass
         
            else:
                bot = message.bot
                for i in avito_dict:
                    for user_id in secret_id:
                        await bot.send_message(user_id,f"{i}\n{avito_dict[i]}") # type: ignore
                        await asyncio.sleep(1)
                
            await asyncio.sleep(900)
            
            
@rt_avito.message(Command("change_prefix"))
async def prefix_question (message: types.Message):
    await message.answer("напиши префикс который надо добавить")
    @rt_avito.message(F.text)
    async def prefix_changer(message: types.Message):
        global prefix
        prefix = message.text
        await message.answer(f"префикс заменен на {prefix}")
    
@rt_avito.message(Command("add"))
async def about_funk(message: types.Message):
    await message.answer("Добавить пользователя 🤔 \nвведите id пользователя")
    @rt_avito.message(F.text)
    async def add_user(message: types.Message):
        global secret_id
        id = ''
        for simbol in str(message.text):
            if simbol in '1234567890':
                id += simbol
        secret_id.append(id)
        print (secret_id)
        await message.answer(f"id {id} добавлен в список")

@rt_avito.message(Command("menu"))
async def menu_func (message: types.Message):
    await message.answer("здесь пока ничего")