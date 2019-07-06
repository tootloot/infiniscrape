import requests
import urllib
import time
from bs4 import BeautifulSoup

def processmodactions(soup):
    rawmodactions = soup.find("table", {"class": "modlog"}).contents[1:]
    modactions = []
    for line in rawmodactions:
        linedict = {}
        timestamp = line.contents[2].find("span").attrs.get("title")
        description = line.contents[4].text
        linedict["timestamp"] = timestamp
        linedict["description"] = description
        modactions.append(linedict)
    return modactions

def listoflinks(soup):
    result = []
    otherlinks = soup.find("p", {"class": "unimportant"})
    for link in list(filter(lambda x: x.name == 'a', otherlinks.contents)):
        test = url + link.attrs.get('href')
        result.append(test)
    return result


url = 'https://8ch.net/log.php?board=pol'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
pagelist = processmodactions(soup)
otherpages = listoflinks(soup)
for page in otherpages:
    url = page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pagelist += processmodactions(soup)
print("mod actions: " + str(len(pagelist)) + ", first timestamp: " + pagelist[0].get("timestamp") + "last timestamp: " + pagelist[-1].get("timestamp"))


