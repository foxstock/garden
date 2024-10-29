# fox_CMTSL 開發記錄:

每日借券賣出下載改為使用 chromedriver 以規避交易所的封鎖

## fix logs:
* 2024-10-29 櫃買中心網頁改版造成爬蟲失敗 分析後修正

## used links:
"證交所首頁":"https://www.twse.com.tw/zh/index.html",
"證交所融券借券賣出餘額":"https://www.twse.com.tw/zh/trading/margin/twt93u.html",
"上櫃融券借券賣出餘額":"https://www.tpex.org.tw/zh-tw/mainboard/trading/margin-trading/sbl.html"

## action分析:


## 輸出CSV檔格式範例:
20241028223012.csv
年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype
2024/10/28,0050,80000,0,0,25176000,3633594,0

