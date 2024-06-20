# PYWIN32模組須降級(for Python3.7x) : pip install --upgrade pywin32==224
# 查詢網站參考 :
# TWSE : https://www.twse.com.tw/zh/trading/margin/twt93u.html
# TPEX : https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl.php?l=zh-tw

import time,json,os,pathlib,subprocess
from traceback import extract_tb
from sys import exc_info,exit,argv
from datetime import datetime
from time import gmtime, strftime
from MyModules.WindowMgr import *
import myModule as my

def validate_date(date_str):
    try:
        # 嘗試將字串按照指定格式轉換為日期
        datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        # 如果轉換失敗，捕捉到 ValueError，則輸入格式不正確
        print("輸入日期錯誤，請重試")
        exit(0)

def compare_last_download(txt1,txt2):
    if my.utf8len(txt1)!=my.utf8len(txt2): # 若長度不同,視為有變
        return False
    else:
        for i,v in enumerate(txt1): # 長度相同,逐字比對內容
            if v!=txt2[i]:
                return False
        return True # 逐字比對內容無異,視為無變

def wait_until_task_close(task_name):
    while True:
        task_str = str(subprocess.check_output(['tasklist'])).upper()
        if task_str.find(task_name.upper())!=-1:
            #task仍在執行中
            print(task_name,'is still running.')
            os.system("taskkill /f /im "+task_name)
            time.sleep(1)
        else:
            #task已close
            print(task_name,' closed!')
            return True

def create_dir_if_not_exist(dir_loc):
    pathlib.Path(dir_loc).mkdir(parents=True, exist_ok=True)

def checkDateStr(arg,todaystr,todayHMS):
    argD=arg[0:8]
    argHMS=arg[8:]
    if argD!=todaystr:
        return True
    elif argD==todaystr and todayHMS[0:2]!=argHMS[0:2]:
        return True
    else:
        return False

def remove_old_tmp_file(today):
    print('移除今日之前的JSON暫存檔')
    folder_path_tw = SOURCE_JSON_TW_DIR
    folder_path_to = SOURCE_JSON_TO_DIR
    for filename in os.listdir(folder_path_tw):
        if filename.endswith('.json') and not filename.startswith(today) and not filename.startswith('temp'):
            # 構建檔案的完整路徑
            file_path = os.path.join(folder_path_tw, filename)
            # 刪除檔案
            os.remove(file_path)
            print(f'已刪除檔案：{folder_path_tw} {filename}')
    for filename in os.listdir(folder_path_to):
        if filename.endswith('.json') and not filename.startswith(today) and not filename.startswith('temp'):
            # 構建檔案的完整路徑
            file_path = os.path.join(folder_path_to, filename)
            # 刪除檔案
            os.remove(file_path)
            print(f'已刪除檔案：{folder_path_to} {filename}')

def download_process(today_str,toHHMMSS_str):
    #執行下載動作
    dataProcessCount=0
    tmp = (today_str[:4]+'/'+today_str[4:6]+'/'+today_str[6:8])+' '+(toHHMMSS_str[:2]+':'+toHHMMSS_str[2:4]+':'+toHHMMSS_str[4:6])
    print(tmp)
    now_ts= str(int(my.datetime_str_to_timestamp(tmp)))
    # 處理上市
    url = "https://www.twse.com.tw/rwd/zh/marginTrading/TWT93U?date="+today_str+"&response=json&_="+now_ts
    source=my.get_web_content(url,15)
    if(my.utf8len(source)<5000):
        #表示今天數據還沒更新
        print("TWSE 今天數據還沒更新，請稍後重試...")
    else:
        try:
            old_txt,new_txt='',''
            with open(SOURCE_JSON_TW_DIR+"temp.json","w") as f:
                f.write(source.replace('\\','\\\\'))
            with open(SOURCE_JSON_TW_DIR+"temp.json","r") as f:
                new_txt=f.read()
            if os.path.exists(SOURCE_JSON_TW_DIR+today_str+".json"):
                with open(SOURCE_JSON_TW_DIR+today_str+".json","r") as f:
                    old_txt=f.read()
            print('TW_OLD:',my.utf8len(old_txt),'TW_NEW:',my.utf8len(new_txt))
            if not compare_last_download(old_txt,new_txt):
                with open(SOURCE_JSON_TW_DIR+today_str+".json","w") as f:
                    f.write(source.replace('\\','\\\\'))
                print("TWSE 今天新數據已下載完成!")
                dataProcessCount+=1
            else:
                print("TWSE 今天無新數據!")
        except:
            pass
    # 處理上櫃
    url="https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl_result.php?l=zh-tw&d="+my.AD_to_CY(today_str)
    source1=my.get_web_content(url,10)
    if(my.utf8len(source1)<5000):
        #表示今天數據還沒更新
        print("TPEX 今天數據還沒更新，請稍後重試...")
    else:
        try:
            old_txt,new_txt='',''
            with open(SOURCE_JSON_TO_DIR+"temp.json","w") as f:
                f.write(source1.replace('\\','\\\\'))
            with open(SOURCE_JSON_TO_DIR+"temp.json","r") as f:
                new_txt=f.read()
            if os.path.exists(SOURCE_JSON_TO_DIR+today_str+".json"):
                with open(SOURCE_JSON_TO_DIR+today_str+".json","r") as f:
                    old_txt=f.read()
            print('TO_OLD:',my.utf8len(old_txt),'TO_NEW:',my.utf8len(new_txt))
            if not compare_last_download(old_txt,new_txt):
                with open(SOURCE_JSON_TO_DIR+today_str+".json","w") as f:
                    f.write(source1.replace('\\','\\\\'))
                print("TPEX 今天新數據已下載完成!")
                dataProcessCount+=1
            else:
                print("TPEX 今天無新數據!")
        except:
            pass
    if dataProcessCount>0: #表示上市或上櫃有更新
        # 檢查 source 與 source1 的內容是否大於 5000 若都小於5000則不寫入文檔
        print(f"TW:{my.utf8len(source)} TO:{my.utf8len(source1)}")
        if my.utf8len(source)<5000 and my.utf8len(source1)<5000:
            return 0
        #寫入上市data到csv
        with open(FINAL_CSV_DIR+today_str+toHHMMSS_str+".csv", "w") as csv_file:
            csv_file.writelines('年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype\n')
            json_array = json.loads(source)
            for i in json_array['data']:
                if(i[0]!=''):
                    csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,0\n" % (my.fix_datetime_format(today),i[0],my.num_comma_clear(i[9]),my.num_comma_clear(i[10]),my.num_comma_clear(i[11]),my.num_comma_clear(i[12]),my.num_comma_clear(i[13])))
        #寫入上櫃data到csv
        with open(FINAL_CSV_DIR+today_str+toHHMMSS_str+".csv", "a") as csv_file:
            json_array = json.loads(source1)
            for i in json_array['aaData']:
                if(i[0]!=''):
                    csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,1\n" % (my.fix_datetime_format(today),i[0],my.num_comma_clear(i[9]),my.num_comma_clear(i[10]),my.num_comma_clear(i[11]),my.num_comma_clear(i[12]),my.num_comma_clear(i[13])))
        print(today_str+toHHMMSS_str+".csv 儲存完畢!")
    else:
        print('數據無異動，無需更新!')
    ### 清理 0KB檔案
    # 遍歷資料夾中的所有檔案
    for filename in os.listdir(FINAL_CSV_DIR):
        file_path = os.path.join(FINAL_CSV_DIR, filename)
        # 確保是檔案而不是資料夾
        if os.path.isfile(file_path):
        # 獲取檔案大小
            size = os.path.getsize(file_path)
            # 如果檔案小於1KB，則刪除
            if size < 2048:
                os.remove(file_path)
                print(f'已刪除0KB檔案：{filename}')

if __name__ == "__main__":
    try:
        #先檢查是否有先前還沒結束的task
        #將當前視窗名設為"MTSL-DAILY"
        w=WindowMgr()
        w.set_cmd_title("M-T-S-L-T-E-M-P")
        while 1:
            w.find_window_wildcard("MTSL-DAILY")
            if w.is_exist==True:
                print("MTSL-DAILY FOUND.KILL IT!")
                w.set_foreground()
                w.close_current_window()
                time.sleep(1)
            else:
                break
            time.sleep(1)
        #將DOS視窗名設為"MTSL-DAILY"
        w.find_window_wildcard("M-T-S-L-T-E-M-P")
        w.set_cmd_title("MTSL-DAILY")
        #變數設定
        base_dir = os.getcwd()
        SOURCE_JSON_TW_DIR=base_dir+"\\SOURCE_JSON_TW\\"
        SOURCE_JSON_TO_DIR=base_dir+"\\SOURCE_JSON_TO\\"
        FINAL_CSV_DIR=base_dir+"\\FINAL_CSV\\"
        #先確定相關資料夾存在，若不存在則新增
        create_dir_if_not_exist(SOURCE_JSON_TW_DIR)
        create_dir_if_not_exist(SOURCE_JSON_TO_DIR)
        create_dir_if_not_exist(FINAL_CSV_DIR)
        #變數設定
        if len(argv)>1:
            validate_date(argv[1])
            today_str=argv[1]
            toHHMMSS_str="233000"
        else:
            today_str=strftime("%Y%m%d", time.localtime())
            toHHMMSS_str=strftime("%H%M%S", time.localtime())
        # 讀取 http://www.web3d.url.tw/workDate/
        work_day_str=my.get_web_content("http://www.web3d.url.tw/workDate/",5)
        today = today_str if my.check_today_is_workday_from_textfile(today_str,work_day_str) else False
        if today!=False:
            print("Current Date: %s" % today)
            remove_old_tmp_file(today_str)
            download_process(today_str,toHHMMSS_str)
        else:
            pass
            #print("今天不是交易日")
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = exc_info() #取得Call Stack
        lastCallStack = extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        with open('runtime_error.log','a+',encoding='utf-8') as f:
            f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\t'+errMsg+'\n')
        print(errMsg)
        ### 清理 0KB檔案
        # 遍歷資料夾中的所有檔案
        for filename in os.listdir(FINAL_CSV_DIR):
            file_path = os.path.join(FINAL_CSV_DIR, filename)
            # 確保是檔案而不是資料夾
            if os.path.isfile(file_path):
            # 獲取檔案大小
                size = os.path.getsize(file_path)
                # 如果檔案小於1KB，則刪除
                if size < 2048:
                    os.remove(file_path)
                    print(f'已刪除0KB檔案：{filename}')
        exit(0)