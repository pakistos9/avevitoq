from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

search_buttons = ReplyKeyboardMarkup(
   keyboard =[
       [KeyboardButton (text = "поиск железа"),
        KeyboardButton (text = "задать поиск")]
   ],
   resize_keyboard=True, input_field_placeholder= "выбирите вариант"
)
del_kbd = ReplyKeyboardRemove() # Этот класс удаляет клавиатуру 
#await message.answer("Привет ты нажал команду menu!", reply_markup=reply.del_kbd)
                                # его подставляют в тоже место где и вызывают клавиатуру


iron_buttons = ReplyKeyboardMarkup(
   keyboard =[
       [KeyboardButton (text = "стиральные машины"),
        KeyboardButton (text = "холодильники")],
       [KeyboardButton (text = "газовые плиты")],
   ],
   resize_keyboard=True, input_field_placeholder= "выбирите вариант"
)

stop_button = ReplyKeyboardMarkup(
   keyboard=[
      [KeyboardButton(text="остановить заданный поиск")]
   ], resize_keyboard=True, input_field_placeholder="нажми"
)