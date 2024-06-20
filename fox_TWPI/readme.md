# 程式說明:

TWPI指的是國發會-景氣指標查詢系統網站提供的數據，
網址為: https://index.ndc.gov.tw/n/zh_tw
這邊透過python爬取網站提供的xls文件，處理成所需的資料轉成csv文字檔。

# 待辦事項:

寫一個抓取下次更新時間並加入行事曆的功能。

# debug note

使用xlrd读取excel文件时， 出现异常：
xlrd.compdoc.CompDocError: Workbook corruption: seen[2] == 4 ...略
可以參考這個解決方案
https://blog.csdn.net/sderaa/article/details/113059134
