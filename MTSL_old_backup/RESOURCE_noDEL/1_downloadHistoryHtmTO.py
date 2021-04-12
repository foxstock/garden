import requests
import urllib.request  
import time
import myModule as mod



text_file = open("workDate.txt", "r")
lines = text_file.read().split('\n')
text_file.close()
#print(lines)
def AD_to_CY(arg):
	return str(int(arg[0:4])-1911)+'/'+arg[4:6]+'/'+arg[6:8]

for i in lines:
	if int(i)<20120317:
		url="https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl_10103/margin_sbl_result.php?l=zh-tw&d="
	elif (int(i)>20120317 and int(i)<20121002):
		url="https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl_10110/margin_sbl_result.php?l=zh-tw&d="
	else:
		url="https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl_result.php?l=zh-tw&d="
	url=url+AD_to_CY(i)
	try:
		urllib.request.urlretrieve(url,"SOURCE_JSON_TO\\"+i+".json")
		print('download ok : '+i)
	except:
		print('download error : '+i)
		mod.log('download error : '+i)
	finally:
		time.sleep(5)