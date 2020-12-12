import requests
from bs4 import BeautifulSoup

input_term = input("Enter a term to search:")
source = requests.get(
    "https://www.google.com/search?q={0}&source=lnms&tbm=nws".format(input_term)).text)
soup = BeautifulSoup(source, 'html.parser')

# here div#ires contains an ol which contains the results.
heading_results = soup.find("div", {"id": "ires"}).find("ol").find_all('h3', {'class': 'r'})
# Loop over each item to obtain the title and link (anchor tag text and link)
print(heading_results)