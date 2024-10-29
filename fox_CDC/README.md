# fox_CDC 開發記錄:

每日當沖下載改為使用 chromedriver 以規避交易所的封鎖

## fix logs:
* 2024-10-29 櫃買中心網頁改版造成爬蟲失敗 分析後修正

## used links:
"證交所首頁":"https://www.twse.com.tw/zh/index.html",
"證交所每日當日沖銷交易標的":"https://www.twse.com.tw/zh/trading/day-trading.html",
"上櫃現股當沖":"https://www.tpex.org.tw/zh-tw/mainboard/trading/day-trading/statistics/day.html"

## action分析:

https://www.twse.com.tw/zh/index.html

首頁>交易資訊>當日沖銷交易標的>每日當日沖銷交易標的
https://www.twse.com.tw/zh/trading/day-trading.html

select[name=yy]value=2024 select[name=mm]value=1~12 select[name=dd]value=1~31
select[name=selectType] value=All
button.Search click!
ajax loading
div.per-page select value=-1
loading All
div.class="rwd-table dragscroll F2 R4_" 

## 輸出CSV檔格式範例:
20241028223012.csv
資料日期,證券代號,當日沖銷交易成交股數,當日沖銷交易買進成交金額,當日沖銷交易賣出成交金額
20240614,0050,435000,77688600,77781650