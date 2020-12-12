import requests
from bs4 import BeautifulSoup


url = "https://news.google.com"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify())