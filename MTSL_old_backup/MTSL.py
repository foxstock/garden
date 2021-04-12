import time,json,os,pathlib
from time import gmtime, strftime
import lib.myModule as my

base_dir = os.path.dirname(os.path.abspath(__file__))

SOURCE_JSON_TW_DIR=base_dir+"\\SOURCE_JSON_TW\\"
SOURCE_JSON_TO_DIR=base_dir+"\\SOURCE_JSON_TO\\"
FINAL_CSV_DIR=base_dir+"\\FINAL_CSV\\"
#先確定相關資料夾存在，若不存在則新增
pathlib.Path(SOURCE_JSON_TW_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(SOURCE_JSON_TO_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(FINAL_CSV_DIR).mkdir(parents=True, exist_ok=True)

today_str=strftime("%Y%m%d", time.localtime())
toHHMMSS_str=strftime("%H%M%S", time.localtime())

#2019-12-06新增 把源從原本從twse網站休市日網頁改為本地端文字檔
workday_txt_url= base_dir + "\\workday2020.txt"
with open(workday_txt_url,'r') as f:
	work_day_str=f.read()
f.close()

today = today_str if my.check_today_is_workday_from_textfile(today_str,work_day_str) else False
#today = today_str if my.check_today_is_workday_and_not_twse_rest_day(today_str) else False
print(("Current Date: %s" % today) if today!=False else "今天不是交易日")

#讀取datestr判斷內容是否等於當前日期，是的話表示今日已經處理過了
DATESTR_TXT_PATH=base_dir+"\\lib\\dateStr.txt"
with open(DATESTR_TXT_PATH,'r') as f:
	datestr=f.read()
f.close()

def checkDateStr(arg,todaystr,todayHMS):
	argD=arg[0:8]
	argHMS=arg[8:]
	if argD!=todaystr:
		return True
	elif argD==todaystr and todayHMS[0:2]!=argHMS[0:2]:
		return True
	else:
		return False

if checkDateStr(datestr,today_str,toHHMMSS_str):
	#執行下載動作
	dataProcessCount=0
	if(today!=False):
		url="https://www.twse.com.tw/exchangeReport/TWT93U?response=json&date="+today
		source=my.get_web_content(url,5)
		if(my.utf8len(source)<5000):
			#表示今天數據還沒更新
			print("TWSE今天數據還沒更新，請稍後重試...")
		else:
			try:
				with open(SOURCE_JSON_TW_DIR+today+".json","w") as f:
					f.write(source)
				f.close()
				csv_file = open(FINAL_CSV_DIR+today+toHHMMSS_str+".csv", "w")
				csv_file.writelines('年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype\n')
				json_array = json.loads(source)
				for i in json_array['data']:
					if(i[0]!=''):
						csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,0\n" % (my.fix_datetime_format(today),i[0],my.num_comma_clear(i[9]),my.num_comma_clear(i[10]),my.num_comma_clear(i[11]),my.num_comma_clear(i[12]),my.num_comma_clear(i[13])))
				csv_file.close()
				print("TWSE今天數據已下載完成!")
				dataProcessCount=dataProcessCount+1
			except:
				pass
		url="https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl_result.php?l=zh-tw&d="+my.AD_to_CY(today)
		source1=my.get_web_content(url,5)
		if(my.utf8len(source)<5000):
			#表示今天數據還沒更新
			print("TPEX今天數據還沒更新，請稍後重試...")
		else:
			try:
				with open(SOURCE_JSON_TO_DIR+today+".json","w") as f:
					f.write(source1)
				f.close()
				csv_file = open(FINAL_CSV_DIR+today+toHHMMSS_str+".csv", "a")
				json_array = json.loads(source1)
				for i in json_array['aaData']:
					if(i[0]!=''):
						csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,1\n" % (my.fix_datetime_format(today),i[0],my.num_comma_clear(i[9]),my.num_comma_clear(i[10]),my.num_comma_clear(i[11]),my.num_comma_clear(i[12]),my.num_comma_clear(i[13])))
				csv_file.close()
				print("TPEX今天數據已下載完成!")
				dataProcessCount=dataProcessCount+1
			except:
				pass
		if dataProcessCount==2:
			#表示TWSE跟TPEX數據都有下載完成，這時要把dataStr.txt內容改成今天的日期
			with open(DATESTR_TXT_PATH,'w') as f:
				f.writelines(today_str+toHHMMSS_str)
			f.close()
else:
	print('今天數據已經下載轉檔完成!')
#os.system('pause')