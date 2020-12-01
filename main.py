#!/usr/bin/env python3
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from coupons import generate_udemy
from pdf import PDF
from browser import login,reg_course
from creds import Creds
from init import utils

#generating the udemy coupon links
coupons = generate_udemy()

#Starting Selinum browser:Chrome
service = Service(os.path.join(os.getcwd(),'chromedriver'))
service.start()
browser = webdriver.Remote(service.service_url)
browser.maximize_window()
time.sleep(3) 

if login(browser, Creds):
   reg_data = reg_course(browser, coupons) 
else:
    print('Theres an error with the login\n Fix the issue and try again later')
    browser.quit()
    sys.exit("Login Error")

#creating pdf
pdf = PDF()
pdf.create_pdf(reg_data)

utils.clrscr()
for i, j in reg_data.items():
  print(i, " : ",j.split('|')[0])
print('\nCheck the report generated for more details (saved in Documents>Udemy Report)')
