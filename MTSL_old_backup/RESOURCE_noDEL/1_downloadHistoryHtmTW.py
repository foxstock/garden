import requests
import urllib.request  
import time




text_file = open("workDate.txt", "r")
lines = text_file.read().split('\n')
text_file.close()

year_prefix='2019'
for i in lines:
	if(i[:4]==year_prefix):
		print(i)
		try:
			url="https://www.twse.com.tw/exchangeReport/TWT93U?response=json&date="+i
			urllib.request.urlretrieve(url,"SOURCE_JSON_TW\\"+i+".json")
		except:
			print('download error with '+i)
			with open('error.log','a') as f:
				f.writelines(i)
		finally:
			time.sleep(10)