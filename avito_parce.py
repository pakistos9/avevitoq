import requests, lxml, asyncio,shelve,os
from bs4 import BeautifulSoup as bs




prefix = "fRmzq"


def one_avito_parse(search):
    global prefix
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = f"https://www.avito.ru/orel?q={search}&s=104"
    
    # Парсим новые объявления
    response = requests.get(url, headers=headers)
    soup = bs(response.text, "lxml")
    cards = soup.find_all("div", class_=f"iva-item-content-{prefix}")
    
    text_dict = {}
    for card in cards:
        text = card.get_text(strip=True)  # Убираем лишние пробелы
        link = "https://www.avito.ru" + card.find("a").get("href", "")
        
        if "репетитор" in text.lower():
            continue
        
        # Сохраняем и текст, и ссылку
        text_dict[link] = text
    
    if not text_dict:
        return {"error": "Нет новых объявлений или неверный префикс!"}
    
    # Работаем с shelve
    with shelve.open("avito", writeback=True) as file:
        if "data" not in file:
            file["data"] = {}
        
        old_data = file["data"]
        new_avito_dict = {}
        
        # Сравниваем и текст, и ссылку
        for link, text in text_dict.items():
            # Если объявления нет в старых данных ИЛИ текст изменился
            if link not in old_data and text not in old_data.values():
                new_avito_dict[link] = text
        
        # Обновляем базу
        file["data"].update(new_avito_dict)
    
    return new_avito_dict