import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from urllib.request import urlopen


url = 'http://www.playdb.co.kr/playdb/playdbDetail.asp?sReqPlayno=160403'

response = requests.get(url)
soup = bs(response.text, "html.parser")
presses = soup.select(
    '.detail_contents .detail_contentsbox table img')  # 배우 얼굴 페이지
for press in presses:
    print("- Soup 객체: ", press)


# html = urlopen(url)
# bsObj = bs(html)
# imageLocation = bsObj.find("a", {"id": "logo"}).find("img")["src"]
# urlretrieve(imageLocation, "logos.jpg")
