from bs4 import BeautifulSoup as bs

import json, sys

data = {}

# ------------------------ Scraping ------------------------

with open("data/exercisesNames.html", "r") as f:
    ul = f.read()

ul = bs(ul, "lxml")

lis = ul.find_all("li")

for li in lis:
    lessonName = li.find_all("div")[0].find_all("div")[1].text
    if lessonName != "Non inviato":
        data[lessonName] = {}
        uls = li.find_all("ul")#.div.find_all("div")[0].find_all("ul")[0].find_all("li")
        if len(uls) > 1:
            divs = uls[0].find_all("div", class_="col m6 offset-m1")
            for i in range(len(divs)):
                data[lessonName][f"E{i+1}"] = divs[i].text
            divs = uls[1].find_all("div", class_="col m6 offset-m1")
            for i in range(len(divs)):
                data[lessonName][f"H{i+1}"] = divs[i].text

with open("data/exercisesNames.json", "w") as f:
    f.write(json.dumps(data, indent=2))

print("INFO - Scraping successful")
