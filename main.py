import requests, lxml, asyncio,shelve
from bs4 import BeautifulSoup as bs
import asyncio, logging, os
from aiogram import F, Dispatcher, Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand

from haders import rt_avito

#secret_id = ["1086225549", "5271211921",]
#search = "отдам+бесплатно"
#=========================================================================

#Avevitio_Bot
#asyncio.sleep(10) # асинхронная функция сна
token = "5588564340:AAFXOO86bIWG5pILzAs0PEqr4sN_PcXrX4I"
bot = Bot(token=token)

menu_comands = [BotCommand (command= "start", description= "начать поиск"),
                BotCommand(command="add", description= "добавить человека"),
                BotCommand(command= "menu", description= "вызов меню"),
                ]

#bot = Bot(token=token)

dp = Dispatcher()
dp.include_routers(rt_avito,)
logging.basicConfig(level=logging.INFO)

#async def avito_search(search):
    #await new_avito_dict = new_avito_seils(search)


            
async def main():
    await bot.set_my_commands(commands=menu_comands,
        scope = types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())