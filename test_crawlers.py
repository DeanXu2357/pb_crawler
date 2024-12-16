import unittest
from datetime import datetime
import logging
import asyncio
from main_new import PBandaiCrawler as SeleniumCrawler
from main_playwright import PBandaiCrawlerPlaywright as PlaywrightCrawler

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCrawlers(unittest.TestCase):
    def setUp(self):
        # 測試配置
        self.test_url = "https://p-bandai.com/tw"
        self.product_url = "https://p-bandai.com/tw/item/N2631684001001"
        self.test_account = ""  # 測試帳號
        self.test_password = ""  # 測試密碼

    def test_selenium_basic(self):
        """測試 Selenium 版本基本功能"""
        crawler = SeleniumCrawler("./chromedriver", headless=False)
        try:
            # 測試首頁載入
            crawler.driver.get(self.test_url)
            self.assertTrue(crawler.driver.current_url == self.test_url)
            
            # 測試是否能找到登入按鈕
            login_btn = crawler.driver.find_element("css selector", "a.header__member")
            self.assertIsNotNone(login_btn)
            
            # 截圖
            crawler.driver.save_screenshot("selenium_basic_test.png")
            
        finally:
            crawler.close()

    def test_selenium_login(self):
        """測試 Selenium 版本登入功能"""
        if not self.test_account or not self.test_password:
            logger.warning("未設置測試帳號密碼，跳過登入測試")
            return
            
        crawler = SeleniumCrawler("./chromedriver", headless=False)
        try:
            result = crawler.login(self.test_account, self.test_password)
            self.assertTrue(result)
            crawler.driver.save_screenshot("selenium_login_test.png")
        finally:
            crawler.close()

    def test_selenium_product(self):
        """測試 Selenium 版本商品頁面"""
        crawler = SeleniumCrawler("./chromedriver", headless=False)
        try:
            crawler.driver.get(self.product_url)
            # 檢查商品頁面元素
            quantity_select = crawler.driver.find_element("name", "quantity")
            submit_btn = crawler.driver.find_element("css selector", "button[type='submit']")
            
            self.assertIsNotNone(quantity_select)
            self.assertIsNotNone(submit_btn)
            
            crawler.driver.save_screenshot("selenium_product_test.png")
        finally:
            crawler.close()

    async def async_test_playwright_basic(self):
        """測試 Playwright 版本基本功能"""
        async with PlaywrightCrawler(headless=False) as crawler:
            # 測試首頁載入
            await crawler.page.goto(self.test_url)
            self.assertTrue(crawler.page.url == self.test_url)
            
            # 測試是否能找到登入按鈕
            login_btn = await crawler.page.wait_for_selector("a.header__member")
            self.assertIsNotNone(login_btn)
            
            # 截圖
            await crawler.page.screenshot(path="playwright_basic_test.png")

    async def async_test_playwright_login(self):
        """測試 Playwright 版本登入功能"""
        if not self.test_account or not self.test_password:
            logger.warning("未設置測試帳號密碼，跳過登入測試")
            return
            
        async with PlaywrightCrawler(headless=False) as crawler:
            result = await crawler.login(self.test_account, self.test_password)
            self.assertTrue(result)
            await crawler.page.screenshot(path="playwright_login_test.png")

    async def async_test_playwright_product(self):
        """測試 Playwright 版本商品頁面"""
        async with PlaywrightCrawler(headless=False) as crawler:
            await crawler.page.goto(self.product_url)
            
            # 檢查商品頁面元素
            quantity_select = await crawler.page.wait_for_selector("select[name='quantity']")
            submit_btn = await crawler.page.wait_for_selector("button[type='submit']")
            
            self.assertIsNotNone(quantity_select)
            self.assertIsNotNone(submit_btn)
            
            await crawler.page.screenshot(path="playwright_product_test.png")

    def test_playwright_basic(self):
        asyncio.run(self.async_test_playwright_basic())

    def test_playwright_login(self):
        asyncio.run(self.async_test_playwright_login())

    def test_playwright_product(self):
        asyncio.run(self.async_test_playwright_product())

if __name__ == '__main__':
    unittest.main()
