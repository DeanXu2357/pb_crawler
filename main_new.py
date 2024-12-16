#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PBandaiCrawler:
    def __init__(self, chrome_driver_path, headless=True):
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--window-size=1920x1080')
        self.options.add_argument('--incognito')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(
            executable_path=chrome_driver_path,
            options=self.options
        )
        self.wait = WebDriverWait(self.driver, 10)  # 10秒等待時間

    def login(self, account, password):
        try:
            logger.info("開始登入流程")
            
            # 等待登入按鈕出現並點擊
            login_btn = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.header__member"))
            )
            login_btn.click()
            
            # 等待並填寫帳號
            account_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "j_username"))
            )
            account_input.send_keys(account)
            
            # 填寫密碼
            password_input = self.driver.find_element(By.NAME, "j_password")
            password_input.send_keys(password)
            
            # 點擊登入
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_btn.click()
            
            # 等待登入完成
            time.sleep(2)
            
            logger.info("登入完成")
            return True
            
        except Exception as e:
            logger.error(f"登入失敗: {str(e)}")
            return False

    def add_to_cart(self, product_url, quantity):
        try:
            logger.info(f"開始將商品添加到購物車: {product_url}")
            
            # 前往商品頁面
            self.driver.get(product_url)
            
            # 等待數量選擇器出現
            quantity_select = self.wait.until(
                EC.presence_of_element_located((By.NAME, "quantity"))
            )
            Select(quantity_select).select_by_value(str(quantity))
            
            # 等待加入購物車按鈕可點擊
            add_to_cart_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            add_to_cart_btn.click()
            
            # 等待加入購物車完成
            time.sleep(2)
            
            # 截圖保存
            self.driver.save_screenshot(f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            logger.info("商品已成功添加到購物車")
            return True
            
        except Exception as e:
            logger.error(f"添加到購物車失敗: {str(e)}")
            return False

    def execute_at_time(self, target_time, product_url, quantity):
        """在指定時間執行購買"""
        while datetime.now() < target_time:
            time.sleep(0.1)  # 減少 CPU 使用率
            
        return self.add_to_cart(product_url, quantity)

    def close(self):
        self.driver.quit()

def main():
    # 配置
    CHROME_DRIVER = "./chromedriver"  # 根據你的 Chrome 版本選擇對應的驅動
    ACCOUNT = ""  # 你的帳號
    PASSWORD = ""  # 你的密碼
    PRODUCT_URL = "https://p-bandai.com/tw/item/N2631684001001"
    QUANTITY = "1"
    TARGET_TIME = datetime.strptime('2024-12-16 12:00:00', '%Y-%m-%d %H:%M:%S')

    try:
        # 初始化爬蟲
        crawler = PBandaiCrawler(CHROME_DRIVER)
        
        # 登入
        if not crawler.login(ACCOUNT, PASSWORD):
            logger.error("登入失敗，程式終止")
            return
        
        # 在指定時間執行購買
        success = crawler.execute_at_time(TARGET_TIME, PRODUCT_URL, QUANTITY)
        
        if success:
            logger.info("商品購買流程完成")
        else:
            logger.error("商品購買失敗")
            
    except Exception as e:
        logger.error(f"發生異常: {str(e)}")
        
    finally:
        crawler.close()

if __name__ == "__main__":
    main()
