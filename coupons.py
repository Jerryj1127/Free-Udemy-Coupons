from requests import get
from bs4 import BeautifulSoup
from datetime import date
import os
def scrap_udemy_coupon(url):
    site_data = get(url)
    soup = BeautifulSoup(site_data.text, 'html.parser')
    hrefs = [anchor['href'] for anchor in soup.findAll(href=True)]
    return [link for link in hrefs if 'www.udemy.com' in link][0]

def generate_udemy():
    data = get('https://www.freshercooker.in/')
    coupons = {}
    #with open('site.txt') as f:
    #    data = f.read()
    soup = BeautifulSoup(data.text, 'html.parser')
    x = soup.find_all("div", class_="td-module-meta-info")
    for i,elem in enumerate(x):
        print('*'*50,'\n','*'*50,'\n',' '*15,f'RETRIVING COUPON: {i+1}/{len(x)}','\n','*'*50,'\n','*'*50)
        title = elem.find(href=True)['title']
        href = elem.find(href=True)['href']
        coupon_url = scrap_udemy_coupon(href).strip()
        date_ = elem.find(class_= 'entry-date updated td-module-date')['datetime'][:10]
        os.system('clear')
        if date_ == str(date.today()):
            coupons[title] = coupon_url
    return coupons
    
        


