import requests, lxml, asyncio,shelve,os,re
import fake_useragent,time,asyncio
from bs4 import BeautifulSoup as bs



    
class Parse_iron:
    def __init__(self):
        self.user = fake_useragent.UserAgent().random
        #self.headers = {"User-Agent":"user",
        #                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",}
        
        #self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
        #"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",}
        self.url_gaz = f"https://www.avito.ru/orel/bytovaya_tehnika?cd=1&geoCoords=52.970371%2C36.063837&q=газовая+плита&radius=50&s=104&searchRadius=50"
        self.url_washing_machine = f"https://www.avito.ru/orel/dlya_doma_i_dachi?geoCoords=52.970371%2C36.063837&q=стиральная+машина&radius=50&s=104&searchRadius=50"
        self.url_fridge = f"https://www.avito.ru/orel/dlya_doma_i_dachi?geoCoords=52.970371%2C36.063837&q=холодильник&radius=50&s=104&searchRadius=50"
        
    def get_gaz (self):
        headers = {
        'User-Agent': self.user,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',}
        #'Referer': "'https://www.avito.ru/" }
        gaz_dict = {}
        responce_gaze = requests.Session().get(self.url_gaz,headers=headers)
        print(f"gas_status {responce_gaze.status_code}")
        soup = bs(responce_gaze.text, "lxml") 
        cards = soup.find_all("div", class_=re.compile(r"iva-item-content-\w+"))
        for card in cards:
            if not card:
                print("ошибка нет карточки")
            pre_text = card.find("div", class_=re.compile(r"iva-item-bottomBlock-\w+"))

            text = pre_text.find("div", class_=re.compile(r"iva-item-ivaItemRedesign-\w+")).text
            print(text)
            link = "https://www.avito.ru" + card.find("a").get("href", "")
            pre_price = card.find("span", class_="price-root-tm5ut").text
            pre_price = pre_price.strip("₽")
            print(pre_price)
            price = ""
            for el in pre_price:
                if el in "1234567890":
                    price += el
            if price.isdigit():
                if int(price) > 700:
                    continue
            if "репетитор" in text.lower():
                continue
            #print(price)   
            # Сохраняем и текст, и ссылку
            gaz_dict[text] = link
            
        with shelve.open ("iron", writeback=True) as file:
            if "gas" not in file:
                file["gas"] = {}
            old_gas = file["gas"]
            new_gas_dict = {}
            for text, link in gaz_dict.items():
                if text not in old_gas:
                    new_gas_dict[text] = link #if text not in old_gas else None
            
            file["gas"].update(new_gas_dict)
              
        return new_gas_dict
    
 #===================================================================================================
 #===================================================================================================   
    def get_washing_machine (self):
        headers = {
        'User-Agent': self.user,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',}
        #'Referer': self.url_washing_machine }
        washing_dict = {}   
        responce_washing_machine = requests.Session().get(self.url_washing_machine,headers=headers)
        print(f"статус стиральных машин {responce_washing_machine.status_code}")
        soup = bs(responce_washing_machine.text,"lxml")
            #print (str(soup))
        cards = soup.find_all("div", class_=re.compile(r"iva-item-content-\w+"))
        for card in cards:
               # print(card.text)
            pre_text = card.find("div", class_=re.compile(r"iva-item-bottomBlock-\w+"))
                #print(pre_text)
            text = pre_text.find("div", class_=re.compile(r"iva-item-ivaItemRedesign-\w+")).text
            link = "https://www.avito.ru" + card.find("a").get("href", "")
            pre_price = card.find("span", class_="price-root-tm5ut").text
            pre_price = pre_price.strip("₽")
            #print(pre_price)
            price = ""
            for el in pre_price:
                if el in "1234567890":
                    price += el
            if price.isdigit():
                if int(price) > 1000:
                    continue
            if "репетитор" in text.lower():
                continue
            washing_dict[text] = link
                
        with shelve.open ("washmachine", writeback=True) as file:
                if "washing" not in file:
                    file["washing"]={}
                old_washing = file["washing"]
                new_washing_dict = {}
                for text, link in washing_dict.items():
                    if text not in old_washing:
                        new_washing_dict[text] = link
                file["washing"].update(new_washing_dict)
        return new_washing_dict

#===========================================================================================================
#===========================================================================================================

    def get_fridge(self):
        headers = {
        'User-Agent': self.user,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',}
        #'Referer': self.url_fridge }
        fridges_dict = {} 
    
        responce_fridges = requests.Session().get(self.url_fridge,headers=headers)
        print (f"холодильник статус код {responce_fridges.status_code}")
        soup = bs(responce_fridges.text,"lxml")
            
        cards = soup.find_all("div", class_=re.compile(r"iva-item-content-\w+"))
        for card in cards:
           
            pre_text = card.find("div", class_=re.compile(r"iva-item-bottomBlock-\w+"))
            #print(pre_text)
            text = pre_text.find("div", class_=re.compile(r"iva-item-ivaItemRedesign-\w+")).text
            print(text)
            link = "https://www.avito.ru" + card.find("a").get("href", "")
            pre_price = card.find("span", class_="price-root-tm5ut").text
            pre_price = pre_price.strip("₽")
            #print(pre_price)
            price = ""
            for el in pre_price:
                if el in "1234567890":
                   price += el
            if price.isdigit():
                if int(price) > 1000:
                    continue
            if "репетитор" in text.lower():
                continue
            fridges_dict[text] = link
        with shelve.open ("fridges", writeback=True) as file:
                if "fridge" not in file:
                    file["fridge"]={}
                old_fridges = file["fridge"]
                new_fridges_dict = {}
                for text, link in fridges_dict.items():
                    if text not in old_fridges:
                        new_fridges_dict[text] = link
                file["fridge"].update(new_fridges_dict)
        return new_fridges_dict
        
#print(Parse_iron().get_washing_machine())

#print (Parse_iron().get_fridge())

#print (Parse_iron().get_gaz())