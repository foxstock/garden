# coding=UTF-8
"""
程式名稱: foxDTD.py
程式功能: 抓取每日上市＆上櫃當沖資訊
Editor: Dennis Yang
修改日期: 2019/04/22
"""
import sys,time,json,pathlib,os,shutil
from time import gmtime, strftime
from datetime import datetime, timedelta
from MyModule.log_writer import log_writer
from MyModule.get_latest_3days import get_latest_3days
from MyModule.get_web_content import get_web_content
from MyModule.write_file import write_file
from MyModule.day_trade_data_to_csv import day_trade_data_to_csv
from MyModule.ftp_upload import ftp_upload

is_twseDL=0
is_tpexDL=0
is_merge=0
is_upload=0
#ftpInfo={'host':'localhost','username':'user','password':'passwd','filename':''}
base_dir = os.path.dirname(os.path.realpath(__file__))+"\\"
#先刪除舊的下載檔案
if os.path.exists(base_dir+"DOWNLOAD\\"): shutil.rmtree(base_dir+"DOWNLOAD\\")

today_str=strftime("%Y%m%d", time.localtime())
toHHMM_str=strftime("%H%M", time.localtime())

dateStr=today_str
if len(sys.argv)>1: dateStr=sys.argv[1]

#work_day_str=get_web_content('http://www.web3d.url.tw/workDate/')
#讀取本地文件 workday2021.txt
workday_txt_url= base_dir + "\\workday2021.txt"
with open(workday_txt_url,'r') as f:
    work_day_str=f.read()
last3days=get_latest_3days(dateStr,work_day_str)
print(last3days)

if last3days != False:
    while is_upload==0:
        if is_twseDL!=1:
            url='http://www.twse.com.tw/exchangeReport/TWTB4U?response=json&date='+(last3days[2])+'&selectType=All&_='+str(round(time.time(),3)).replace(',','')
            tmp=get_web_content(url)
            #print(tt)
            ck = json.loads(tmp)
            if len(ck['creditList'])==0:
                print("TWSE上市當沖網頁檔尚未更新!")
            else:
                #今日上市網頁已更新 先存到電腦
                d_url=base_dir+"DOWNLOAD\\TWSE\\SOURCE\\"
                pathlib.Path(d_url).mkdir(parents=True, exist_ok=True)
                write_file(d_url+last3days[2]+'.json','w',tmp)
                print('████ TWSE: '+last3days[2]+'.json'+'  Downloaded! ████')
                d_url2=base_dir+"DOWNLOAD\\TWSE\\TMP\\"
                pathlib.Path(d_url2).mkdir(parents=True, exist_ok=True)
                d_url3=base_dir+"DOWNLOAD\\TWSE\\TMP_100\\"
                pathlib.Path(d_url3).mkdir(parents=True, exist_ok=True)
                day_trade_data_to_csv(last3days[2],d_url+last3days[2]+'.json',d_url2+last3days[2]+'.csv','TWSE')
                day_trade_data_to_csv(last3days[2],d_url+last3days[2]+'.json',d_url3+last3days[2]+'.csv','100')
                time.sleep(8)
                #接著下載前兩交易日網頁
                for ii in range(0,2):
                    url='http://www.twse.com.tw/exchangeReport/TWTB4U?response=json&date='+(last3days[ii])+'&selectType=All&_='+str(round(time.time(),3)).replace(',','')
                    tmp=get_web_content(url)
                    write_file(d_url+last3days[ii]+'.json','w',tmp)
                    print('████ TWSE: '+last3days[ii]+'.json'+' Downloaded! ████')
                    day_trade_data_to_csv(last3days[ii],d_url+last3days[ii]+'.json',d_url2+last3days[ii]+'.csv','TWSE')
                    day_trade_data_to_csv(last3days[ii],d_url+last3days[ii]+'.json',d_url3+last3days[ii]+'.csv','100')
                    time.sleep(8)

                e_dir=base_dir+"DOWNLOAD\\TWSE\\RESULT\\"
                pathlib.Path(e_dir).mkdir(parents=True, exist_ok=True)
                write_file(e_dir+dateStr+'.csv', 'w','')
                for i in last3days:
                    with open(d_url2+i+'.csv') as f:
                        file = open(e_dir+dateStr+'.csv', 'a+')
                        lines = f.readlines()
                        for j in lines:
                            if j!="":
                                file.write(j)
                for i in last3days:
                    with open(d_url3+i+'.csv') as f:
                        file = open(e_dir+dateStr+'.csv', 'a+')
                        lines = f.readlines()
                        for j in lines:
                            if j!="":
                                file.write(j)
                print("%s上市日當沖網頁下載完成!" %(last3days[2]))
                is_twseDL=1
        else:
            print('今日上市當沖已下載完成!')
        if is_tpexDL!=1:
            tmpDateStr=str(int(last3days[2][0:4])-1911)+"/"+last3days[2][4:6]+"/"+last3days[2][6:8]
            url = 'http://www.tpex.org.tw/web/stock/trading/intraday_stat/intraday_trading_stat_result.php?l=zh-tw&d='+tmpDateStr
            tmp=get_web_content(url)
            ck = json.loads(tmp)
            if len(ck['stat_0'])==0:
                print("TPEX上櫃當沖網頁檔尚未更新!")
            else:
                #今日上櫃網頁已更新 先存到電腦
                d_url=base_dir+"DOWNLOAD\\TPEX\\SOURCE\\"
                pathlib.Path(d_url).mkdir(parents=True, exist_ok=True)
                write_file(d_url+last3days[2]+'.json','w',tmp)
                print('████ TPEX: '+last3days[2]+'.json'+'  Downloaded! ████')
                d_url2=base_dir+"DOWNLOAD\\TPEX\\TMP\\"
                pathlib.Path(d_url2).mkdir(parents=True, exist_ok=True)
                d_url3=base_dir+"DOWNLOAD\\TPEX\\TMP_400\\"
                pathlib.Path(d_url3).mkdir(parents=True, exist_ok=True)
                day_trade_data_to_csv(last3days[2],d_url+last3days[2]+'.json',d_url2+last3days[2]+'.csv','TPEX')
                day_trade_data_to_csv(last3days[2],d_url+last3days[2]+'.json',d_url3+last3days[2]+'.csv','400')
                #接著下載前兩交易日網頁
                for ii in range(0,2):
                    tmpDateStr=str(int(last3days[ii][0:4])-1911)+"/"+last3days[ii][4:6]+"/"+last3days[ii][6:8]
                    url = 'http://www.tpex.org.tw/web/stock/trading/intraday_stat/intraday_trading_stat_result.php?l=zh-tw&d='+tmpDateStr
                    tmp=get_web_content(url)
                    write_file(d_url+last3days[ii]+'.json','w',tmp)
                    print('████ TPEX: '+last3days[ii]+'.json'+' Downloaded! ████')
                    day_trade_data_to_csv(last3days[ii],d_url+last3days[ii]+'.json',d_url2+last3days[ii]+'.csv','TPEX')
                    day_trade_data_to_csv(last3days[ii],d_url+last3days[ii]+'.json',d_url3+last3days[ii]+'.csv','400')
                    time.sleep(8)
                print("%s上櫃日當沖網頁下載完成!" %(last3days[2]))
                e_dir=base_dir+"DOWNLOAD\\TPEX\\RESULT\\"
                pathlib.Path(e_dir).mkdir(parents=True, exist_ok=True)
                write_file(e_dir+dateStr+'.csv', 'w','')
                for i in last3days:
                    with open(d_url2+i+'.csv') as f:
                        file = open(e_dir+dateStr+'.csv', 'a+')
                        lines = f.readlines()
                        for j in lines:
                            if j!="":
                                file.write(j)
                for i in last3days:
                    with open(d_url3+i+'.csv') as f:
                        file = open(e_dir+dateStr+'.csv', 'a+')
                        lines = f.readlines()
                        for j in lines:
                            if j!="":
                                file.write(j)
                is_tpexDL=1
        else:
            print('今日上櫃當沖已下載完成!')

        if is_twseDL and is_tpexDL:
            if is_merge==0:
                #doMerge
                fileExt=".csv"
                s_dir=base_dir+"DOWNLOAD\\TWSE\\RESULT\\"
                source_file=last3days[2]+fileExt
                e_dir=base_dir+"FINAL\\"
                final_file=dateStr+toHHMM_str+fileExt
                pathlib.Path(e_dir).mkdir(parents=True, exist_ok=True)
                write_file(e_dir+final_file, 'w',"資料日期,證券代號,當日沖銷交易成交股數,當日沖銷交易買進成交金額,當日沖銷交易賣出成交金額%\n")

                if os.path.exists(s_dir+source_file):
                    with open(s_dir+source_file) as f:
                        file = open(e_dir+final_file, 'a+')
                        lines = f.readlines()
                        for j in lines:
                            if j!="":
                                file.write(j)
                s_dir=base_dir+"DOWNLOAD\\TPEX\\RESULT\\"
                if os.path.exists(s_dir+source_file):
                    with open(s_dir+source_file) as f:
                        file = open(e_dir+final_file, 'a+')
                        lines = f.readlines()
                        for j in lines:
                            if j!="":
                                file.write(j)
                print("%s上市上櫃日當沖資料合併完成!" %(last3days[2]))
                is_merge=1
            else:
                print("%s上市上櫃日當沖資料已合併!" %(last3days[2]))
        time.sleep(3)
        #doFtp
        if is_merge==1:
            exit(0)
            pass
            #tmp='{"host":"'+ftpInfo['host']+'","username":"'+ftpInfo['username']+'","password":"'+ftpInfo['password']+'","filename":"'+dateStr+toHHMM_str+'.csv"}'
            #write_file(base_dir+'ftp_info.json','w',tmp)
            #is_upload=1
        else:
            print("%s上市上櫃日當沖資料尚未合併!\n三分鐘後會自動重啟下載~請稍候\n===================\n" %(last3days[2]))
            time.sleep(180)