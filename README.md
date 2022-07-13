# PB 搶單程式

### 使用方法
1. 確定環境中有 python3
2. pip3 安裝依賴
```
pip3 install --upgrade pip
pip3 install selenium
```
3. 到 [下載點](https://chromedriver.chromium.org/downloads) 下載執行環境安裝的 chrome 版本
4. 解壓縮後改名為 `chromedriver` 放至根目錄
5. 編輯 main.py 於 36 行設定帳號、商品、數量等資訊，62 行設定觸發時間。
6. 執行 `python3 main.py`

### extra
1. 使用前確認 電腦裡 selenium 版本，版本號 4 以上執行 `python3 main4.py`  
其餘照舊  
```
pip3 show selenium  // 確認版本號指令
```
2. 如果登入過久會被系統自動登出，導致加進購物車失敗，  
所以請於開搶前 5 分鐘再執行，太早執行怕會被自動登出。
