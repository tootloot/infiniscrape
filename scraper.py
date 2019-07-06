import requests
import urllib
import time
from bs4 import BeautifulSoup

url = 'https://8ch.net/log.php?board=pol'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
soup.findAll('a')
