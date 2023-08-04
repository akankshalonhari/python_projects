import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

urlset = []

def build_site_map(starting_url : str, max_depth: int) :
    response = requests.get(starting_url)
    html_text = response.text
    soup = BeautifulSoup(html_text, 'html.parser')
    
    tempdict = {
        "page_url" : starting_url,
        "links" : [],
        "images" : []
    }

    urlend = ".com"
    suburl = starting_url[starting_url.index(urlend) + len(urlend):]

    scrappedlinks = []
    for link in soup.find_all('a'):
        templink = link.get('href')
        if templink[0] == "/" and suburl in templink and len(templink)>1:
            scrappedlinks.append(templink)
            urlset.append(templink)
    #print(scrappedlinks)
    
    scrappedimgs = []
    for imgs in soup.find_all('link'):
        tempimg = imgs.get('href')
        if "/img/" in tempimg:
            scrappedimgs.append(tempimg)

    for imgs in soup.find_all('img'):
        tempimg = imgs.get('src')
        if "/img/" in tempimg:
            scrappedimgs.append(tempimg)
    #print(scrappedimgs)
    
    tempdict["links"] = scrappedlinks
    tempdict["images"] = scrappedimgs
    return tempdict

def checkmatch(substring: str, tempstr: str):
    if len(substring) == 1 and len(tempstr) == 1 and substring == "/":
        return True
    else:
        if len(substring) <= len(tempstr) and substring in tempstr:
            return True
        else:
            return False
    return False

if __name__ == '__main__':
    resultjson = []
    starting_url = "https://hckrnews.com"
    max_depth = 3
    resultjson.append(build_site_map(starting_url + "/", max_depth))
    
    count = len(urlset)
    for url in urlset:
        max_depth -= 1
        if max_depth > 0 :
            resultjson.append(build_site_map(starting_url + url, max_depth))
        count -= 1
        if count == 0:
            break
    pprint(resultjson)