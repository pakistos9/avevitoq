import requests, lxml, asyncio
from bs4 import BeautifulSoup as bs
import asyncio, logging
from aiogram import F, Dispatcher, Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand

#from avito import get_info_avito, new_avito_seils, one_avito_parse
avito_super_dict = {}
secret_id = []
def one_avito_parse(search):
    global avito_super_dict
    url = f"https://www.avito.ru/orel?q={search}&s=104"
    text_dict = {}

    responce = requests.get(url)
    soup = bs(responce.text, "lxml")
    cards = soup.find_all("div", class_="""iva-item-content-OWwoq""")
    for card in cards:
        text = str(card.text)
        link = "https://www.avito.ru" + str(card.find ("a").get("href"))
        text_dict.setdefault(text,link)

    new_avito_dict = {}

    if not avito_super_dict:
        avito_super_dict = text_dict.copy()
        return text_dict
    
    else:
        for el in text_dict:
            if el not in avito_super_dict:
                new_avito_dict.setdefault(el, text_dict[el])
        avito_super_dict.update(new_avito_dict)
        return new_avito_dict
        


#Avevitio_Bot
#asyncio.sleep(10) # асинхронная функция сна
token = "5588564340:AAFXOO86bIWG5pILzAs0PEqr4sN_PcXrX4I"
menu_comands = [BotCommand (command= "start", description= "начать поиск"),
                BotCommand(command="about", description= "как работает бот"),
                BotCommand(command= "menu", description= "вызов меню"),]

bot = Bot(token=token)
search = "отдам+бесплатно"
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

#async def avito_search(search):
    #await new_avito_dict = new_avito_seils(search)

@dp.message(Command('start'))
async def avito_start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name} собираем информацию для стартового листа!!!\n ваш id {message.from_user.id}")
    while True:
        avito_dict = one_avito_parse(search)
        if not avito_dict:
            print ("пока ничего")
            
        else:
            for i in avito_dict:
                await message.answer(f"{i}\n{avito_dict[i]}")
                await asyncio.sleep(1)
        await asyncio.sleep(900)

#@dp.message(Command("go"))
#async def avito_go(message: types.Message):
#    await message.answer("пробую найти")
#    while True:
#        new_avito_dict = new_avito_seils(search)

#        if not new_avito_dict:
#            #await message.answer("пока ничего")
#            await asyncio.sleep(900)
#        else:
#            for i in new_avito_dict:
#                await message.answer(f"{i} \n{new_avito_dict[i]}")
#                await asyncio.sleep(2)
#            await asyncio.sleep(900)
    
@dp.message(Command("about"))
async def about_funk(message: types.Message):
    await message.answer("бот загружает данные с сайта авито и сохраняет их, в последующем он каждые 15 минут проверяет обновления и присылаит их пользователю 🤗")

@dp.message(Command("menu"))
async def menu_func (message: types.Message):
    await message.answer("здесь пока ничего")


async def main():
    await bot.set_my_commands(commands=menu_comands,
        scope = types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
