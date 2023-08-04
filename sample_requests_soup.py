import requests
from bs4 import BeautifulSoup

def say_hello():
    print('Hello, World')

for i in range(3):
    say_hello()

request_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
response_htmltext = requests.get(request_url).text
soup_htmldata = BeautifulSoup(response_htmltext, 'html.parser')
#print(soup_htmldata.get_text())
print(soup_htmldata.title)
bannertext = soup_htmldata.find(id='banner_ad').text
print(bannertext)

for link in soup_htmldata.find_all('a'):
    print(link.get('href'))
