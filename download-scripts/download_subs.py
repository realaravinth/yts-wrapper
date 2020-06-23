from bs4 import BeautifulSoup
import sys
import requests

def yify_subs(url):
    response = requests.get(url)
    if response.ok:
        return response
    else:
        yify_subs(url)

list_url = "https://www.yifysubtitles.com/movie-imdb/" + str(sys.argv[1])
response = yify_subs(list_url)
soup = BeautifulSoup(response.content, 'html.parser')
heading = soup.h4
if heading['class'][0] == 'modal-title':
    print(1)
else:
    while True:
        try:
            heading = heading.next_element
            if heading == 'English':
                target = heading.next_element.a
                break
        except:
                break
    subs_page = "https://www.yifysubtitles.com" + target.get('href')
    response = yify_subs(subs_page)
    soup = BeautifulSoup(response.content, 'html.parser')
    for i in soup.find_all('a'):
        try:
            if i.attrs['class'][0] == 'btn-icon':
                subs_link = i.get('href')
                break
        except:
            continue
    print(subs_link) 
