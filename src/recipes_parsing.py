from bs4 import BeautifulSoup
import requests
import re
import database


URL = "https://www.povarenok.ru/recipes/"
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
}


def parse():
    for num in range(1, 200):
        if num == 1:
            url = URL
        else:
            url = URL + f"~{num}/"
        req = requests.get(url, headers=HEADERS)
        src = req.text

        data = []
        soup = BeautifulSoup(src, "lxml")
        names = soup.find_all("h2")
        for i in names:
            rec = dict()
            tmp = i.find("a")
            if tmp == None:
                break
            rec["name"] = tmp.text
            rec["link"] = tmp.get("href")
            data.append(rec)

        ingr = soup.find_all("div", class_=re.compile("ingr_fast"))
        for k, i in enumerate(ingr):
            ingrs = ""
            tmp = i.find_all("span")
            ingreds = []
            for j in tmp:
                ingreds.append(j.text)
            ingreds.sort()
            data[k]["ingrs"] = ",".join(ingreds)
        

        for recipe in data:
            database.add_line(recipe["name"], recipe["ingrs"], recipe["link"])
            print(recipe)
