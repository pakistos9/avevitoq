import requests, lxml, asyncio,shelve,os,re
import fake_useragent, time
from bs4 import BeautifulSoup as bs

session = requests.Session()

search = "отдам+бесплатно"

def one_avito_parse(search):
    user = fake_useragent.UserAgent().random
    #headers = {
    #    "User-Agent": user,
    #    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    #}
    
    headers = {
        'User-Agent': user,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': "https://www.avito.ru/orel?q={search}&s=104"}
    
    url = f"https://www.avito.ru/orel?q={search}&s=104"

    text_dict = {}
    response = requests.Session().get(url, headers=headers)
    print(f"бесплатные обЪявления статус код сбора карточек попытка {response.status_code}")
    soup = bs(response.text, "lxml")
    cards = soup.find_all("div", class_=re.compile(r"iva-item-content-\w+"))
    for card in cards:
        pre_text = card.find("div", class_=re.compile(r"iva-item-bottomBlock-\w+")) 
        text = pre_text.find("div", class_=re.compile(r"iva-item-ivaItemRedesign-\w+")).text
        link = "https://www.avito.ru" + card.find("a").get("href", "")
        
        if "репетитор" in text.lower():
            continue
        
        # Сохраняем и текст, и ссылку
        text_dict[text] = link
    if not text_dict:
        return {"ошибка": "Нет новых объявлений или неверный префикс!"}
    
    # Работаем с shelve
    with shelve.open("avito", writeback=True) as file:
        if "data" not in file:
            file["data"] = {}
        old_data = file["data"]
        new_avito_dict = {}
        
        # Сравниваем и текст, и ссылку
        for text, link in text_dict.items():
            # Если объявления нет в старых данных ИЛИ текст изменился
            if text not in old_data and link not in old_data.values():
                new_avito_dict[text] = link
        
        # Обновляем базу
        file["data"].update(new_avito_dict)
    
    return new_avito_dict

#=================================================================================================
#=================================================================================================

def name_avito_parse(search):
    user = fake_useragent.UserAgent().random
    
    headers = {
        'User-Agent': user,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',}
        #'Referer': "https://www.avito.ru/orel?q={search}&s=104"}
    
    #headers = {
    #    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
    #    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    #}
    
    url = f"https://www.avito.ru/orel?q={search}&s=104"
    # ищем количество страниц
    text_dict = {}
               
    response = requests.Session().get(url, headers=headers)
    print(f"статус код заданного поиска {response.status_code}")
    soup = bs(response.text, "lxml")
    cards = soup.find_all("div", class_=re.compile(r"iva-item-content-\w+"))
    for card in cards:
        pre_text = card.find("div", class_=re.compile(r"iva-item-bottomBlock-\w+")) 
        text = pre_text.find("div", class_=re.compile(r"iva-item-ivaItemRedesign-\w+")).text
        link = "https://www.avito.ru" + card.find("a").get("href", "")
        
        if "репетитор" in text.lower():
            continue
        
        # Сохраняем и текст, и ссылку
        text_dict[text] = link
    # Работаем с shelve
    with shelve.open("some_avito", writeback=True) as file:
        if "data" not in file:
            file["data"] = {}
        old_data = file["data"]
        new_avito_dict = {}
        # Сравниваем и текст, и ссылку
        for text, link in text_dict.items():
            # Если объявления нет в старых данных ИЛИ текст изменился
            if text not in old_data and link not in old_data.values():
                new_avito_dict[text] = link
        # Обновляем базу
        file["data"].update(new_avito_dict)
    
    return new_avito_dict


print (one_avito_parse(search))