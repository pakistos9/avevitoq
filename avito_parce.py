import requests, lxml, asyncio,shelve,os
from bs4 import BeautifulSoup as bs




prefix = "fRmzq"


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
