# MTSL 借券賣出 log

## 2023/MM/DD
### TMP TITLE
-----

## 2023/03/21
### TWSE 修改了API網址的參數導致 03/20 晚間程式執行出錯
既然要修改，就順便把一些小問題也解決了，處理如下:
1. 保留現有架構:
    * SOURCE_JSON_TW
    * SOURCE_JSON_TO
    * FINAL_CSV
2. workdate 的部份改成抓取 http://www.web3d.url.tw/workDate/ 來作判斷，這樣後續維護會輕鬆一些。
3. 清理 MTSL 裡面一些無用的東西DirtyCode。
4. 將 MTSL 改寫另存一個可以通過輸入日期取得 日期.csv 的版本 (MTSL_input_date.py)
5. 或許可以在樹莓派寫個腳本每天抓取一份並放在web3d.idv.tw上面，畢竟還是自己能管理的站比較好維護!

-----