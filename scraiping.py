import urllib.request
from bs4 import BeautifulSoup 

url = "https://profile.yahoo.co.jp/fundamental/4902"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
items = soup.select('div.profile > div > div > table > tr > td > table > tr > td')
print(items[5].text)
'''
for item in items:
    print(item)
    print("=======================================")
'''
