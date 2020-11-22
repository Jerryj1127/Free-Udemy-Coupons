from requests import get
from bs4 import BeautifulSoup
from datetime import date
import os
def get_udemy_coupon(url):
    site_data = get(url)
    soup = BeautifulSoup(site_data.text, 'html.parser')
    hrefs = [anchor['href'] for anchor in soup.findAll(href=True)]
    return [link for link in hrefs if 'www.udemy.com' in link][0]

def generate_udemy(url):
    data = get(url)
    global coupons
    coupons = {}
    #with open('site.txt') as f:
    #    data = f.read()
    soup = BeautifulSoup(data.text, 'html.parser')
    x = soup.find_all("div", class_="td-module-meta-info")
    for i,elem in enumerate(x):
        os.system('clear')
        print('*'*50,'\n','*'*50,'\n',' '*15,f'RETRIVING COUPON: {i+1}/{len(x)}','\n','*'*50,'\n','*'*50)
        title = elem.find(href=True)['title']
        href = elem.find(href=True)['href']
        coupon_url = get_udemy_coupon(href).strip()
        date_ = elem.find(class_= 'entry-date updated td-module-date')['datetime'][:10]
        if date_ == str(date.today()):
            coupons[title] = coupon_url
    
        

generate_udemy('https://www.freshercooker.in/')


print(coupons)

