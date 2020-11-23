login_page = 'https://www.udemy.com/join/login-popup/'
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import os
from creds import Creds
from coupons import generate_udemy, scrap_udemy_coupon
outcome = {}
coupons = generate_udemy()


def browser(name, url):
    driver.get(url)
    time.sleep(5)
    #In case the course was already registered
    try:
        status_check = driver.find_element_by_xpath("//button[@class='udlite-btn udlite-btn-large udlite-btn-primary udlite-heading-md styles--btn--express-checkout--28jN4']")
    except:
        return 'ERROR '+ url
    if status_check.text == 'Go to course':
        return 'Course already Registered'

    #In case the course isnt free or the coupon has expired
    elif status_check.text == 'Buy now':
        return 'The course is not free'
        
    ### The below scrip is to be used only if the course is free and not registered already
    elif status_check.text == 'Enroll now':
        try:
            driver.find_element_by_xpath("//button[@class='udlite-btn udlite-btn-large udlite-btn-primary udlite-heading-md styles--btn--express-checkout--28jN4'][.='Enroll now']").click()
            time.sleep(4)
            driver.find_element_by_xpath('//*[@id="udemy"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button').click()
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button')).click()
            #driver.find_element_by_xpath("//button[@class='ellipsis btn btn-lg btn-primary btn-block'][.='Enroll now']").click()
            #driver.find_element_by_xpath('//button[normalize-space()="Enroll now"]').click()
            time.sleep(5)
            driver.save_screenshot(f"temp/{name}.png")
            return 'Success'
        except:
            return 'Failed '

service = Service(os.path.join(os.getcwd(),'chromedriver'))
service.start()
driver = webdriver.Remote(service.service_url)
driver.get(login_page)
driver.maximize_window()
time.sleep(1) # Let the user actually see something!
driver.find_element_by_xpath('//*[@id="email--1"]').send_keys(Creds.username)
driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(Creds.password)
driver.find_element_by_xpath('//*[@id="submit-id-submit"]').click()
time.sleep(5)

for course in coupons.keys():
    url = coupons[course]
    outcome[course] = browser(course, url)

print('\n\n')

for i in outcome.items():
    print(i,'\n')