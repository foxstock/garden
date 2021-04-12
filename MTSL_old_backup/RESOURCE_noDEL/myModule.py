""" 程式說明
程式名稱: myModule.py    建立時間:2019/08/29
說明:常用函式庫整合
"""
import re,requests,random,time,os,pathlib
from random import choice
from time import gmtime, strftime
from datetime import datetime, timedelta

#產生假的user_agent header
def get_fake_userAgent():
	user_agent = [
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
	"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
	"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
	"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
	"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
	"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
	"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
	"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	"MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
	"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
	"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
	"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
	"Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
	"UCWEB7.0.2.37/28/999",
	"NOKIA5700/ UCWEB7.0.2.37/28/999",
	"Openwave/ UCWEB7.0.2.37/28/999",
	"Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
	]
	return {'User-Agent':random.choice(user_agent)}

#get_twse_rest_day的子函數
def parse_date_from_cht(arg):
	arg=re.sub("(\d{1,2})([^\d]+)(\d{1,2})([^\d]+)",r'\1,\3',arg)
	tmp_arr=arg.split(",")
	if int(tmp_arr[0])<10: tmp_arr[0]='0'+str(tmp_arr[0])
	if int(tmp_arr[1])<10: tmp_arr[1]='0'+str(tmp_arr[1])
	return (tmp_arr[0]+tmp_arr[1])

#取得台灣證交所網站公告的休市日
def get_twse_rest_day():
	url="http://www.twse.com.tw/zh/holidaySchedule/holidaySchedule"
	headers = get_fake_userAgent()
	source = str(requests.get(url, headers=headers, timeout=10).text)
	#source=htmlTxt
	rest_day_arr=[]
	source=re.findall('<td align="center">(.*?)</td>', source)
	for i in range(0,len(source),1):
		if source[i].find('月')!=-1:
			#檢查字串內是否有<br/>
			if source[i].find('<br/>')==-1:
				#只有單一個日期 例如:1月2日
				rest_day_arr.append(parse_date_from_cht(source[i]))
			else:
				tmp_arr=source[i].split("<br/>")
				for j in tmp_arr:
					rest_day_arr.append(parse_date_from_cht(j))
	return rest_day_arr

#檢查dateStr是否為周一至周五
def check_work_day(dateStr):
	ckday = datetime.strptime(dateStr, '%Y%m%d').weekday()
	if ckday<5:
		return True # Mon - Fri
	else:
		return False # Sat - Sun

#檢查今天是否為交易日，是則傳回True，否則傳回False
def check_today_is_workday_and_not_twse_rest_day():
	oday_str=strftime("%Y%m%d", time.localtime())
	twse_rest_arr=get_twse_rest_day()
	if check_work_day(oday_str):
		if oday_str[4:8] in twse_rest_arr:
			return False
		else:
			return True
	else:
		return False

#取得網頁內容_以requests.get方式獲取，傳回目標url的html源碼
def get_web_content(url,sleep_time):
	while 1:
		try:
			headers=get_fake_userAgent()
			#print(headers)
			r=requests.get(url,headers=headers, timeout=15)
			r.encode='utf-8'
			if(r.status_code==200):
				break
			else:
				time.sleep(sleep_time)
		except:
			time.sleep(sleep_time)
	return r.text


#將日期時間及說明字串記錄到event.log
def log(arg):
	today_str=strftime("%Y%m%d", time.localtime())
	toHHMM_str=strftime("%H%M%S", time.localtime())
	#print("%s %s" %(today_str,toHHMM_str))
	base_dir = os.path.dirname(os.path.realpath(__file__))+"\\log\\"
	pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True) 
	file=open(base_dir+'event.log','a+')
	file.writelines("'%s %s', '%s'\r\n" %(today_str,toHHMM_str,arg))
	file.close

#返回變數s的sizes(bytes)
def utf8len(s):
	return len(s.encode('utf-8'))

#將西曆YYYYMMDD轉成國曆YYY/MM/DD
def AD_to_CY(arg):
	return str(int(arg[0:4])-1911)+'/'+arg[4:6]+'/'+arg[6:8]

#將國曆YYY/MM/DD轉成西曆YYYYMMDD
def CY_to_AD(arg):
	tmp_arr=arg.split("/")
	return str(int(tmp_arr[0])+1911)+''+tmp_arr[1]+''+tmp_arr[2]

#將YYYYMMDD轉成YYYY/MM/DD
def fix_datetime_format(arg):
	return str(arg[:4])+'/'+arg[4:6]+'/'+arg[6:8]

#將數字字串裡的千分符','用''取代，例如123,456轉成123456
def num_comma_clear(arg):
	return arg.replace(",","")


def get_proxy():
	url="https://www.sslproxies.org/"
	r=requests.get(url)
	print(r.text)
	#soup=BeautifulSoup(r.content,'html5lib')
	#return {str(htype):choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
