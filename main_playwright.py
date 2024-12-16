#!/usr/bin/python3

from playwright.sync_api import sync_playwright
from datetime import datetime
import logging
import time
import asyncio
import os
from typing import Optional

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PBandaiCrawlerPlaywright:
    @staticmethod
    def ensure_browser():
        """確保瀏覽器已安裝"""
        try:
            # 嘗試安裝 Chromium
            result = os.system("python -m playwright install chromium")
            if result == 0:
                logger.info("Chromium 已安裝或安裝成功")
                return True
            else:
                logger.error("Chromium 安裝失敗")
                return False
        except Exception as e:
            logger.error(f"安裝瀏覽器時發生錯誤: {str(e)}")
            return False

    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        # 確保瀏覽器已安裝
        if not self.ensure_browser():
            raise RuntimeError("無法確保瀏覽器安裝")
