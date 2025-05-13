import requests, lxml, asyncio,shelve
from bs4 import BeautifulSoup as bs
import asyncio, logging, os
from aiogram import F, Dispatcher, Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand



prefix = "fRmzq"
secret_id = ["1086225549", "5271211921",]
#=========================================================================
def one_avito_parse(search):
    global prefix
    url = f"https://www.avito.ru/orel?q={search}&s=104"
    text_dict = {}
    new_avito_dict = {} #новый словарь из новых объявлений

    responce = requests.get(url)
    soup = bs(responce.text, "lxml")
    cards = soup.find_all("div", class_=f"""iva-item-content-{prefix}""")
    for card in cards:
        text = str(card.text)
        link = "https://www.avito.ru" + str(card.find ("a").get("href"))
        text_dict.setdefault(text,link)
        
    if not text_dict:
        return{"словарь пуст":"добавте новый префикс!!!"}
    
    if os.path.isfile("avito"): # если авито фаил есть
        
        shelve_file = shelve.open("avito")
        avito_dict_file = shelve_file["data"]
        
        for el in text_dict:
            if el not in avito_dict_file.keys():
                new_avito_dict.setdefault(el,text_dict[el])
        new_dict = avito_dict_file.copy()
        shelve_file.close()
        new_dict.update(new_avito_dict)
        file = shelve.open("avito")
        file["data"]=new_dict
        file.close()
        return new_avito_dict
    else: # если фаила нет
        file = shelve.open("avito")
        file["data"] = text_dict
        file.close()
        return text_dict
    

        


#Avevitio_Bot
#asyncio.sleep(10) # асинхронная функция сна
token = "5588564340:AAFXOO86bIWG5pILzAs0PEqr4sN_PcXrX4I"
menu_comands = [BotCommand (command= "start", description= "начать поиск"),
                BotCommand(command="about", description= "как работает бот"),
                BotCommand(command= "menu", description= "вызов меню"),
                BotCommand(command="change_prefix", description="изменить префикс"),]

bot = Bot(token=token)
search = "отдам+бесплатно"
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

#async def avito_search(search):
    #await new_avito_dict = new_avito_seils(search)

@dp.message(Command('start'))
async def avito_start(message: types.Message):
    global secret_id
    if str(message.from_user.id) not in secret_id:
        await message.answer(f"{message.from_user.first_name} у вас нет прав пользоваться ботом!!! 🤔")
    else:
        await message.answer(f"Привет {message.from_user.first_name} собираем информацию для стартового листа!!!\n ваш id {message.from_user.id}")
        while True:
            avito_dict = one_avito_parse(search)
            if not avito_dict:
                #print ("пока ничего")
                pass
         
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
@dp.message(Command("change_prefix"))
async def prefix_question (message: types.Message):
    await message.answer("напиши префикс который надо добавить")
    @dp.message()
    async def prefix_changer(message: types.Message):
        global prefix
        prefix = message.text
        await message.answer(f"префикс заменен на {prefix}")
    
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
