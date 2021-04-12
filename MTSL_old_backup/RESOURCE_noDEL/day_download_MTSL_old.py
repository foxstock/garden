import time,json
from time import gmtime, strftime
import lib.myModule as my

today_str=strftime("%Y%m%d", time.localtime())
toHHMMSS_str=strftime("%H%M%S", time.localtime())
today = today_str if my.check_today_is_workday_and_not_twse_rest_day() else False
print(("Current Date: %s" % today) if today!=False else "今天不是交易日")

if(today!=False):
	url="https://www.twse.com.tw/exchangeReport/TWT93U?response=json&date="+today
	source=my.get_web_content(url,5)
	if(my.utf8len(source)<5000):
		#表示今天數據還沒更新
		print("TWSE今天數據還沒更新，請稍後重試...")
	else:
		csv_file = open("FINAL_CSV\\"+today+toHHMMSS_str+".csv", "w")
		csv_file.writelines('年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype\n')
		json_array = json.loads(source)
		for i in json_array['data']:
			if(i[0]!=''):
				csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,0\n" % (my.fix_datetime_format(today),i[0],my.num_comma_clear(i[9]),my.num_comma_clear(i[10]),my.num_comma_clear(i[11]),my.num_comma_clear(i[12]),my.num_comma_clear(i[13])))
		csv_file.close()
		print("TWSE今天數據已下載完成!")
	url="https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl_result.php?l=zh-tw&d="+my.AD_to_CY(today)
	source1=my.get_web_content(url,5)
	if(my.utf8len(source)<5000):
		#表示今天數據還沒更新
		print("TPEX今天數據還沒更新，請稍後重試...")
	else:
		csv_file = open("FINAL_CSV\\"+today+toHHMMSS_str+".csv", "a")
		json_array = json.loads(source1)
		for i in json_array['aaData']:
			if(i[0]!=''):
				csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,1\n" % (my.fix_datetime_format(today),i[0],my.num_comma_clear(i[9]),my.num_comma_clear(i[10]),my.num_comma_clear(i[11]),my.num_comma_clear(i[12]),my.num_comma_clear(i[13])))
		csv_file.close()
		print("TPEX今天數據已下載完成!")