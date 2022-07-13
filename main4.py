#!/usr/bin/python3

from re import sub
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from threading import Timer
import os
import time

# Configs
account = "" # 帳號
pwd = "" # 密碼
productUrl = "https://p-bandai.com/tw/item/N2631684001001" # 商品連結 
quantity = "2" # 商品數量 (需注意商品敘述內單筆訂單上限)
targetDate = "2022-07-13" # 日期 yyyy-mm-dd
targetHour = 16 # 時 hh (24小時制)
targetMinute = 59 # 分 mm 

def execute(driver, productUrl, quantity):
    print(datetime.now())
    print(productUrl)
    print(quantity)
    # redirect to product
    driver.get(productUrl)

    # select quantity
    countSelect = Select(driver.find_element("xpath","/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/ul/li/div/select"))
    countSelect.select_by_value(quantity)

    # add to cart
    submitBtn = driver.find_element("xpath","/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/div/button")
    submitBtn.click()

    time.sleep(2)

    driver.get_screenshot_as_file("capture.png")


option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('window-size=1920x1080')
option.add_argument("--incognito")



# open product page
driver = webdriver.Chrome(options=option,service=Service(ChromeDriverManager().install()))
driver.get(productUrl)

# login flow
loginBtn = driver.find_element("xpath","/html/body/header/div[1]/div[4]/a")
loginBtn.click()

accountElem = driver.find_element("xpath","/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[1]/div[2]/label/input")
accountElem.send_keys(account)
pwdElem = driver.find_element("xpath","/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[2]/div[2]/label/input")
pwdElem.send_keys(pwd)

submitLoginBtn = driver.find_element("xpath","/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[2]/button/a")
submitLoginBtn.click()

now = datetime.now()
nt = now.timestamp()

targetTime = datetime.strptime(targetDate, "%Y-%m-%d").replace(hour=targetHour, minute=targetMinute)
tt = targetTime.timestamp()

t = Timer(tt-nt, execute, [driver, productUrl, quantity])
t.start()
