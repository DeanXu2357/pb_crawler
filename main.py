#!/usr/bin/python3

from re import sub
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
from threading import Timer
import os
import time

def execute(driver, productUrl, quantity):
    print(datetime.now())
    print(productUrl)
    print(quantity)
    # redirect to product
    driver.get(productUrl)

    # select quantity
    countSelect = Select(driver.find_element_by_xpath("/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/ul/li/div/select"))
    countSelect.select_by_value(quantity)

    # add to cart
    submitBtn = driver.find_element_by_xpath("/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/div/button")
    submitBtn.click()

    time.sleep(2)

    driver.get_screenshot_as_file("capture.png")


option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('window-size=1920x1080')
option.add_argument("--incognito")

# Configs
chrome_driver = "./chromedriver"
account = ""
pwd = ""
productUrl = "https://p-bandai.com/tw/item/N2631684001001"
quantity = "2"

# open product page
driver = webdriver.Chrome(chrome_options=option, executable_path=chrome_driver)
driver.get(productUrl)

# login flow
loginBtn = driver.find_element_by_xpath("/html/body/header/div[1]/div[4]/a")
loginBtn.click()

accountElem = driver.find_element_by_xpath("/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[1]/div[2]/label/input")
accountElem.send_keys(account)
pwdElem = driver.find_element_by_xpath("/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[2]/div[2]/label/input")
pwdElem.send_keys(pwd)

submitLoginBtn = driver.find_element_by_xpath("/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[2]/button/a")
submitLoginBtn.click()

now = datetime.now()
nt = now.timestamp()

targetTime = datetime.strptime('2022-07-13', "%Y-%m-%d").replace(hour=11, minute=13)
tt = targetTime.timestamp()

t = Timer(tt-nt, execute, [driver, productUrl, quantity])
t.start()
