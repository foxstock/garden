import time,re,os,pathlib,time,configparser
from sys import exit,argv,executable
from datetime import datetime
from time import gmtime,strftime
from WindowMgr import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

def ini_to_dict(ini_loc):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(ini_loc,encoding='utf-8')
    sections=config.sections()
    tmp_dict={}
    for i in sections:
        options=config.options(i)
        for j in options:
            tmp_dict[i+'.'+j]=config[i][j]
    return tmp_dict

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

#返回變數s的sizes(bytes)
def utf8len(s,encode_type):
    return len(s.encode(encode_type))

def compare_two_txt_content(txt1,txt2):
    if utf8len(txt1,'Big5')!=utf8len(txt2,'Big5'): # 若長度不同,視為有變
        #print('長度不同,視為有變') #DEBUG
        return False
    else:
        for i,v in enumerate(txt1): # 長度相同,逐字比對內容
            #print(txt2[i]) #DEBUG
            if v!=txt2[i]: return False
    return True # 逐字比對內容無異,視為無變

def scrapy():
    global config,today_str,toHHMMSS_str,FINAL_CSV_DIR,url_dict,run_count,pause_second
    try:
        service = Service(config['SETTING.chromedriver_loc'])
        # 初始化 Chrome 選項
        options = Options()
        # 添加參數，使 Chrome 瀏覽器最大化
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-gps")
        driver = webdriver.Chrome(service=service, options=options)
        #try:
        #    if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(5)
        #    driver.get(url_dict["證交所首頁"])
        #except:
        #    if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(10)
        #    driver.get(url_dict["證交所融券借券賣出餘額"])
        #if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(10)
        driver.get(url_dict["證交所融券借券賣出餘額"])

        time.sleep(5)

        driver.get(f"https://www.twse.com.tw/rwd/zh/marginTrading/TWT93U?date={today_str}&response=html")

        time.sleep(5)
    
        # 定位到 html 元素
        div_element = driver.find_element(By.TAG_NAME, 'html')

        # 取得該 DIV 元素的內容 HTML 原始碼
        inner_html = div_element.get_attribute('innerHTML')

        if len(inner_html)<70000: 
            print("證交所融券借券賣出餘額無數據或尚未更新...")
            driver.quit()
            exit(0)
            return True

        soup = BeautifulSoup(inner_html, 'html.parser')
        target_table = soup.select_one('table tbody')
        final_ls=[]
        cells=[]
        for row in target_table.find_all('tr'):
            cells.append( row )
        for i in range(0,len(cells)-1):
            ls=re.findall(r"<td[^>]*>(.*?)</td>",str(cells[i]))
            final_ls.append([today_str,ls[0],remove_comma(ls[9]),remove_comma(ls[10]),remove_comma(ls[11]),remove_comma(ls[12]),remove_comma(ls[13]),'0'])
        # 上市ok
        driver.get(url_dict["上櫃融券借券賣出餘額"])
        time.sleep(5)

        button = driver.find_element(By.XPATH,"//*[contains(text(),'列印/匯出HTML')]")
        button.click() # 按下 列印/匯出HTML

        driver.switch_to.window(driver.window_handles[1])

        yy=today_str[0:4]
        mm=today_str[4:6]
        dd=today_str[6:8]

        tmp_url=f"https://www.tpex.org.tw/www/zh-tw/margin/sbl?date={yy}%2F{mm}%2F{dd}&id=&response=html"

        driver.get(tmp_url)
        time.sleep(5)
        div_element = driver.find_element(By.TAG_NAME, 'html')
        inner_html = div_element.get_attribute('innerHTML')
        
        if len(inner_html)<70000: 
            print("上櫃融券借券賣出餘額無數據或尚未更新...")
            driver.quit()
            #exit(0)
            return True

        soup = BeautifulSoup(inner_html, 'html.parser')
        target_table = soup.select_one('body table tbody')

        cells=[]
        for row in target_table.find_all('tr'):
            cells.append( row )
        for i in range(0,len(cells)):
            ls=re.findall(r"<td[^>]*>(.*?)</td>",str(cells[i]))
            #print(ls)
            final_ls.append([today_str,ls[0],remove_comma(ls[9]),remove_comma(ls[10]),remove_comma(ls[11]),remove_comma(ls[12]),remove_comma(ls[13]),'1'])

        driver.quit()
        with open(FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv','w+') as f:
            f.writelines('年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype\n')
            for ln in final_ls:
                f.writelines(f"{add_slash_to_date_str(ln[0])},{ln[1]},{ln[2]},{ln[3]},{ln[4]},{ln[5]},{ln[6]},{ln[7]}\n")
        print('借券賣出: '+today_str+toHHMMSS_str+'.csv 下載完成!')
        ### 清理 0KB檔案
        # 遍歷資料夾中的所有檔案
        #print("清理 0KB檔案") #DEBUG
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
        if config['SETTING.delete_same_content_at_same_day'] and os.path.isfile(FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv'):
            # 清除同日期相同內容的文字檔，如果 SETTING.delete_same_content_at_same_day 為 True 的話
            # 遍歷資料夾中的所有檔案
            #print("遍歷資料夾中的所有檔案") #DEBUG
            for filename in os.listdir(FINAL_CSV_DIR):
                file_path = os.path.join(FINAL_CSV_DIR, filename)
                #print(file_path)
                # 確保是檔案而不是資料夾
                if os.path.isfile(file_path):
                    tmp_date=str(file_path).split("\\")[-1][:8] # a=yyyymmdd
                    # 比對日期是否相同，若日期相同但檔名不同則比對文字檔內容，若文字檔內容相同則刪除先前已存在的文字檔，保留剛下載的文字檔，若不相同則不做刪除。
                    if tmp_date==today_str and file_path!=FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv':
                        #print(f"compare {file_path}") #DEBUG
                         # 比對兩個文字檔
                        txt1,txt2="",""
                        with open(FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv','r') as f:
                            txt1=f.read()
                            #print(f"read txt1 ") #DEBUG
                        with open(file_path,'r') as f:
                            txt2=f.read()
                            #print(f"read txt2 ") #DEBUG
                        if compare_two_txt_content(txt1,txt2):
                            # 若文字檔內容相同則刪除先前已存在的文字檔
                            os.remove(file_path)
                            print(f"文字檔內容相同已刪除:{file_path}")
        exit(0) #結束程式
        return True
    except Exception as e:
        if run_count==2:
            print(f'程式已執行2次，執行期間發生不可預期之錯誤，強制終止程式...。')
        else:    
            print(f'執行期間發生不可預期之錯誤，強制終止程式...{pause_second}秒後採集程式會重新執行。')
        driver.quit()
        return False


if __name__ == "__main__":
    exec_path_full=executable #獲取完整執行檔路徑
    exec_path_ls=exec_path_full.split("\\")
    exec_path=exec_path_full.replace(exec_path_ls[-1],"")
    print(f"執行檔所在路徑: {exec_path}")
    #先檢查是否有先前還沒結束的task
    #將當前視窗名設為"CMTSL-DAILY"
    w=WindowMgr()
    w.set_cmd_title("C-M-T-S-L-T-E-M-P")
    while 1:
        w.find_window_wildcard("CMTSL-DAILY")
        if w.is_exist==True:
            print("PREV-CMTSL-DAILY FOUND.KILL IT!")
            w.set_foreground()
            w.close_current_window()
            time.sleep(1)
        else:
            break
        time.sleep(1)
    #將DOS視窗名設為"MTSL-DAILY"
    w.find_window_wildcard("C-M-T-S-L-T-E-M-P")
    w.set_cmd_title("CMTSL-DAILY")        
    base_dir = exec_path
    config=ini_to_dict(f"{exec_path}\\setting.ini")
    #print(config)
    FINAL_CSV_DIR = base_dir + "FINAL\\"
    # CREATE FINAL CSV DIR IF NOT EXIST
    create_dir_if_not_exist(FINAL_CSV_DIR)
    if len(argv)>1:
        validate_date(argv[1])
        today_str=argv[1]
        toHHMMSS_str="233000"
    else:
        today_str=strftime("%Y%m%d",time.localtime())
        toHHMMSS_str=strftime("%H%M%S",time.localtime())
    yy=today_str[0:4]
    mm=str(int(today_str[4:6]))
    dd=str(int(today_str[6:8]))
    url_dict={
        "證交所首頁":"https://www.twse.com.tw/zh/index.html",
        "證交所融券借券賣出餘額":"https://www.twse.com.tw/zh/trading/margin/twt93u.html",
        "上櫃融券借券賣出餘額":"https://www.tpex.org.tw/zh-tw/mainboard/trading/margin-trading/sbl.html"
    }
    run_count=0
    pause_second=20
    while 1:
        run_count=run_count+1
        result=scrapy()
        #print(f"result:{result}")
        if result or run_count==2:
            exit(0)
        else:
            time.sleep(pause_second)