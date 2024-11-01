import time,re,os,pathlib,time,configparser,requests
from sys import exit,argv,executable
from datetime import datetime
from time import gmtime,strftime
#from WindowMgr import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

def get_latest_3days(dateStr,work_day_str):
	work_day_arr=work_day_str.split("\n")#np.loadtxt(work_day_str,dtype=str,unpack=True, ndmin = 1)
	print('日期: '+dateStr)
	tmpnum=0
	today_inT2=0
	for i in work_day_arr:
		if i==dateStr:
			today_inT2=1
			break
		else:
			tmpnum=tmpnum+1
	t2 = []
	if today_inT2==0:
		return (t2)
	t2.append(str(work_day_arr[tmpnum-2]))
	t2.append(str(work_day_arr[tmpnum-1]))
	t2.append(str(work_day_arr[tmpnum]))
	return (t2)

def get_web_content(url):
	while 1:
		try:
			#headers=get_fake_userAgent()
			r=requests.get(url)
			r.encode='utf-8'
			if(r.status_code==200):
				break
			else:
				time.sleep(5)
		except:
			time.sleep(5)
	return r.text

def create_dir_if_not_exist(dir_loc):
    pathlib.Path(dir_loc).mkdir(parents=True, exist_ok=True)

def remove_comma(num_str):
    return str(num_str).replace(",","")

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        print("Input Date Error...Please Try Again!")
        exit(0)

def ac_to_cc(date_str):
    return str(int(date_str[0:4])-1911)+'/'+date_str[4:6]+'/'+date_str[6:8]

def add_slash_to_date_str(date_str):
    return f"{date_str[0:4]}/{date_str[4:6]}/{date_str[6:8]}"

today_str=input("上市櫃當沖 : 輸入要下載的日期:").strip()
if today_str=="":
	today_str=strftime("%Y%m%d",time.localtime())
	toHHMMSS_str=strftime("%H%M%S",time.localtime())
else:
	toHHMMSS_str="233000"
work_day_str=get_web_content('http://www.web3d.url.tw/workDate/')
last3days=get_latest_3days(today_str,work_day_str)
#print(last3days)
if last3days:
    print(f"最近三個交易日:{last3days}")
else:
    print(f"{today_str} 不是交易日!")
    exit()

# 上市當沖: "https://www.twse.com.tw/rwd/zh/dayTrading/TWTB4U?date={today_str}&selectType=All&response=html",
# 上櫃當沖: "https://www.tpex.org.tw/www/zh-tw/intraday/stat?type=Daily&date={yy}%2F{mm}%2F{dd}&id=&response=html"


########################################
########################################

url="https://www.google.com"
service = Service("C:\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(2)
for tmp_day in last3days:
    try:
        yy=tmp_day[0:4]
        mm=str(int(tmp_day[4:6]))
        dd=str(int(tmp_day[6:8]))
        # 抓取近三天的上市當沖DATA
        driver.get(f"https://www.twse.com.tw/rwd/zh/dayTrading/TWTB4U?date={tmp_day}&selectType=All&response=html")
        time.sleep(3)
        source=driver.page_source
        with open(f"TW_{tmp_day}.txt","w+") as f:
            f.write(source)
        print(f"TW_{tmp_day}.txt 已儲存.")
        time.sleep(7)
    except:
        pass
driver.get(url)
for tmp_day in last3days:
    try:
        yy=tmp_day[0:4]
        mm=str(int(tmp_day[4:6]))
        dd=str(int(tmp_day[6:8]))
        # 抓取近三天的上櫃當沖DATA
        driver.get(f"https://www.tpex.org.tw/www/zh-tw/intraday/stat?type=Daily&date={yy}%2F{mm}%2F{dd}&id=&response=html")
        time.sleep(3)
        source=driver.page_source
        with open(f"TO_{tmp_day}.txt","w+") as f:
            f.write(source)
        print(f"TO_{tmp_day}.txt 已儲存.")
        time.sleep(7)
    except:
        pass

driver.close()