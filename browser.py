#!/usr/bin/env python3

import time
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import os


def browser(driver, name, url):
    driver.get(url)
    time.sleep(5)

    try:
        x_path = "//button[@class='udlite-btn udlite-btn-large udlite-btn-primary udlite-heading-md styles--btn--express-checkout--28jN4']"
        status_check = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH , x_path)))
    except:
        return 'ERROR |'+ url

    #In case the course was already registered
    if status_check.text == 'Go to course':
        return 'Course already Registered'

    #In case the course isnt free or the coupon has expired
    elif status_check.text == 'Buy now':
        return 'The course is not free'
        
    ### The below scrip is to be used only if the course is free and not registered already
    elif status_check.text == 'Enroll now':
        try:
            xpath_enroll = "//button[@class='udlite-btn udlite-btn-large udlite-btn-primary udlite-heading-md styles--btn--express-checkout--28jN4'][.='Enroll now']"
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH , xpath_enroll))).click()
            ##The below statement is intended for people from India but you may change it for your country
            try:
                xpath_state = f"//*[@value][.='{Creds.state}']"
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH , xpath_state))).click()
            except:
                pass
            xpath_confirm = '//*[@id="udemy"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button'
            enroll_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH , xpath_confirm)))
            time.sleep(3)
            enroll_btn.click()
            #driver.find_element_by_xpath("//button[@class='ellipsis btn btn-lg btn-primary btn-block'][.='Enroll now']").click()
            #driver.find_element_by_xpath('//button[normalize-space()="Enroll now"]').click()
            start_course = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Start course')))
            time.sleep(1)
            url = start_course.get_attribute('href')
            driver.save_screenshot(f"temp/{name}.png")
            return 'Success |' + url
        except:
            return 'Failed |'+ url

def login(driver, Creds):
    login_page = 'https://www.udemy.com/join/login-popup/'
    try:
        driver.get(login_page)
        driver.find_element_by_xpath('//*[@id="email--1"]').send_keys(Creds.username)
        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(Creds.password)
        driver.find_element_by_xpath('//*[@id="submit-id-submit"]').click()
        time.sleep(3)
        if driver.current_url == login_page:
            return False
        return True
    except: 
        return False

def reg_course(driver, coupons):
    if not os.path.isdir('temp'):
        os.mkdir('temp')
    outcome = {}

    for course in coupons.keys():
        url = coupons[course]
        outcome[course] = browser(driver, course, url)
    driver.quit()

    return outcome



