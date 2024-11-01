# 輸出格式 : 資料日期,證券代號,當日沖銷交易成交股數,當日沖銷交易買進成交金額,當日沖銷交易賣出成交金額
# 輸出範例 : 20241025,0050,680000,133166650,133231400
# 備註 : Big5 文件格式
# 選中第 n 個表格的css語法: table:nth-of-type(1) 取得body底下第一個表格
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

def remove_td(arg):
    tmp = re.sub("<td[^>]*>","",str(arg))
    return tmp.replace("</td>","").replace(",","")


today_str=input("上市櫃當沖 : 輸入要下載的日期:").strip()
if today_str=="":
	today_str=strftime("%Y%m%d",time.localtime())
	toHHMMSS_str=strftime("%H%M%S",time.localtime())
else:
	toHHMMSS_str="233000"
work_day_str=get_web_content('http://www.web3d.url.tw/workDate/')
date_ls=get_latest_3days(today_str,work_day_str)
#print(last3days)
if date_ls:
    print(f"最近三個交易日:{date_ls}")
else:
    print(f"{today_str} 不是交易日!")
    exit()

final_ls=[]

date_ls=sorted(date_ls)
#print(date_ls)

for i in date_ls:
    tmp_date=i
    with open(f"TW_{tmp_date}.txt","r") as f:
        source = f.read() 
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())
    result = soup.select('table:nth-of-type(1) tbody tr td') #取得 加權data
    #print(result) 取 result[0],result[2],result[4]
    final_ls.append([tmp_date,'100',remove_td(result[0]),remove_td(result[2]),remove_td(result[4])])
    #print("加權:",final_ls)
    result = soup.select('table:nth-of-type(2) tbody tr') #取得 個股data
    for j in result:
        re_ls=re.findall("<td>(.*?)</td>",(str(j).replace("\n","")))
        #print(re_ls)
        if len(re_ls)==6:
            final_ls.append([tmp_date,remove_td(re_ls[0]),remove_td(re_ls[3]),remove_td(re_ls[4]),remove_td(re_ls[5])])
# print(final_ls)

for i in date_ls:
    tmp_date=i
    with open(f"TO_{tmp_date}.txt","r") as f:
        source = f.read() 
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())
    result = soup.select('table:nth-of-type(1) tbody tr td') #取得 上櫃data
    #print(result) 取 result[0],result[2],result[4]
    final_ls.append([tmp_date,'400',remove_td(result[0]),remove_td(result[2]),remove_td(result[4])])
    #print("上櫃:",final_ls)
    result = soup.select('table:nth-of-type(2) tbody tr') #取得 個股data
    for j in result:
        re_ls=re.findall("<td[^>]*>(.*?)</td>",(str(j).replace("\n","")))
        #print(re_ls)
        if len(re_ls)==6:
            final_ls.append([tmp_date,remove_td(re_ls[0]),remove_td(re_ls[3]),remove_td(re_ls[4]),remove_td(re_ls[5])])
# print(final_ls)

with open(f"{today_str}{toHHMMSS_str}.csv","w+") as f:
    f.writelines(f"資料日期,證券代號,當日沖銷交易成交股數,當日沖銷交易買進成交金額,當日沖銷交易賣出成交金額\n")
    for ln in final_ls:
        if len(ln)>=5:
            f.writelines(f"{ln[0]},{ln[1]},{ln[2]},{ln[3]},{ln[4]}\n")
print(f"{today_str}{toHHMMSS_str}.csv SAVED!")
input()