from aiogram import F, Dispatcher, Bot, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
import asyncio, os
from aiogram.types import BufferedInputFile

from avito_parce import one_avito_parse, name_avito_parse
from buttons import search_buttons, del_kbd, iron_buttons, stop_button
from iron import Parse_iron
from EXIF_func import meta_get


rt_avito = Router()
go = False
#prefix = "fRmzq"
secret_id = ["1086225549", "5271211921",]
search = "отдам+бесплатно"
search_object = ""

@rt_avito.message(Command('start'))
async def avito_start(message: types.Message):
    global search
    global secret_id
    if str(message.from_user.id) not in secret_id: # type: ignore
        await message.answer(f"{message.from_user.first_name} у вас нет прав пользоваться ботом!!! 🤔 \n ваш id {message.from_user.id}") # type: ignore
    else:
        await message.answer(f"Привет {message.from_user.first_name} собираем информацию для стартового листа!!!\n ваш id {message.from_user.id}") # type: ignore
        while True:
            avito_dict = one_avito_parse(search=search)
            if not avito_dict:
                #print ("пока ничего")
                pass
         
            else:
                #bot = message.bot #для того что бы отправить сообщение ользовотелю принудительно
                for i in avito_dict:
                    for user_id in secret_id:
                        await message.bot.send_message(user_id,f"*️⃣отдам бесплатно*️⃣ \n{i}\n{avito_dict[i]}") # type: ignore # отправить сообщение на юзер ай ди
                        await asyncio.sleep(1)
                
            await asyncio.sleep(900)
            
            

    
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
    await message.answer("держи", reply_markup=search_buttons)
    
 #===================================================================   
@rt_avito.message(F.text == "поиск железа")
async def search_iron (message: types.Message):
    await message.answer("выберете поиск...",reply_markup=iron_buttons)
    
    @rt_avito.message(F.text == "стиральные машины")
    async def search_washing_machin(message: types.Message):
        global secret_id
        await message.answer("ищу...", reply_markup=del_kbd)
        while True:
            washing_machine = Parse_iron().get_washing_machine()
            for i in washing_machine:
                for u_id in secret_id:
                    await message.bot.send_message(u_id, f"🔵стиралки🔵 \n{i}\n{washing_machine[i]}") # type: ignore
                    await asyncio.sleep(1)
            await asyncio.sleep(1000)
                
    
    @rt_avito.message(F.text == "холодильники")
    async def search_fridge(message: types.Message):
        global secret_id
        await message.answer("ищу...", reply_markup=del_kbd)
        while True:
            fridges = Parse_iron().get_fridge()
            for i in fridges:
                for u_id in secret_id:
                    await message.bot.send_message(u_id,f"🔶холодильники🔶 \n{i}\n{fridges[i]}") # type: ignore
                    await asyncio.sleep(1)
            await asyncio.sleep(1000)
    
    @rt_avito.message(F.text == "газовые плиты")
    async def search_gas(message: types.Message):
        global secret_id
        await message.answer("ищу...", reply_markup=del_kbd)
        while True:
            gas = Parse_iron().get_gaz()
            for i in gas:
                for u_id in secret_id:
                    await message.bot.send_message(u_id,f"🔷газовые плиты🔷 \n{i}\n{fridges[i]}") # type: ignore
                    await asyncio.sleep(1)
            await asyncio.sleep(1000)

@rt_avito.message(F.text == "задать поиск")
async def search_other (message: types.Message):
    global go
    if go == False:
        await message.answer("введите что хотите найти: ", reply_markup=del_kbd)
    else: await message.answer("останови поиск", reply_markup=stop_button)
    
    @rt_avito.message(F.text)
    async def search_add(message: types.Message):
        global go
        go = True
        global secret_id
        search_object = str(message.text).lower()
        search_object = search_object.split()
        search_object = "+".join(search_object)
        print (search_object)
        while go:
            search_dict = name_avito_parse(search=search_object)
            for k, v in search_dict.items():
                for u_id in secret_id:
                    await message.bot.send_message(u_id,f"🔻 заданный поиск 🔻 \n{k}\n{v}") # type: ignore
                    await asyncio.sleep(1)
            await asyncio.sleep(1000)
                
@rt_avito.message(F.text == "остановить заданный поиск")
async def stop_search(message: types.Message):
    global go
    go = False
    await message.answer("🔅поиск остановлен!🔅")



ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 
    'image/tiff', 'image/webp'
}

    
@rt_avito.message(F.document & F.document.mime_type.in_(ALLOWED_MIME_TYPES)) 
async def seeq_file_exif (message: types.Message):
    file_id = message.document.file_id # type: ignore
    file = await message.bot.get_file(file_id) # type: ignore
    file_path = f"photo.jpg"
    await message.bot.download_file(file.file_path, destination=file_path) # type: ignore
    meta_data = meta_get()
    for k, v in meta_data.items():
        await message.answer(f" ▫️метаданные▫️ \n{k} {v}")
        await asyncio.sleep(1)
    
   
#@rt_avito.message(F.photo)
#async def seeq_photo_exif(message: types.Message):
    
#    photo = message.photo[-1] # type: ignore
    
 #   file_info = await message.bot.get_file(photo.file_id) # type: ignore
 #   file_path = f"photo.jpg"
 #   await message.bot.download_file( # type: ignore
#            file_path=file_info.file_path, # type: ignore
#            destination=file_path
#        )
        
    