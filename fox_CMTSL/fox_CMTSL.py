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
    global config,today_str,toHHMMSS_str,FINAL_CSV_DIR,url_dict
    try:
        service = Service(config['SETTING.chromedriver_loc'])
        # 初始化 Chrome 選項
        options = Options()
        # 添加參數，使 Chrome 瀏覽器最大化
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-gps")
        driver = webdriver.Chrome(service=service, options=options)
        try:
            if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(5)
            driver.get(url_dict["證交所首頁"])
        except:
            if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(10)
            driver.get(url_dict["證交所融券借券賣出餘額"])
        if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(10)
        driver.get(url_dict["證交所融券借券賣出餘額"])

        time.sleep(3)
        # 使用 By 類別來定位名稱為 'yy' 的 select 元素
        select_element = Select(driver.find_element(By.NAME, 'yy'))
        select_element.select_by_value(yy)

        time.sleep(1)

        # 使用 By 類別來定位名稱為 'mm' 的 select 元素
        select_element = Select(driver.find_element(By.NAME, 'mm'))
        select_element.select_by_value(mm)

        time.sleep(1)

        # 使用 By 類別來定位名稱為 'dd' 的 select 元素
        select_element = Select(driver.find_element(By.NAME, 'dd'))
        select_element.select_by_value(dd)

        time.sleep(1)

        btn_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/div[2]/button')
        btn_element.click()

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

        select_element = Select(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/div[2]/hgroup/div/div[1]/select'))  
        # 選擇 value 為 'All' 的選項
        select_element.select_by_value('-1')

        time.sleep(5)

        # 定位到 class 名稱為 'rwd-table dragscroll F2 R4_' 的 DIV 元素
        table_element = driver.find_element(By.TAG_NAME, 'html')

        # 取得該 DIV 元素的內容 HTML 原始碼
        inner_html = table_element.get_attribute('innerHTML')

        soup = BeautifulSoup(inner_html, 'html.parser')
        target_table = soup.select_one('div.main-content div.rwd-table table tbody')
        final_ls=[]
        cells=[]
        for row in target_table.find_all('tr'):
            cells.append( row )
        for i in range(0,len(cells)-1):
            ls=re.findall(r"<td[^>]*>(.*?)</td>",str(cells[i]))
            final_ls.append([today_str,ls[0],remove_comma(ls[9]),remove_comma(ls[10]),remove_comma(ls[11]),remove_comma(ls[12]),remove_comma(ls[13]),'0'])
        # 上市ok
        driver.get(url_dict["上櫃融券借券賣出餘額"])
        input_date = driver.find_element(By.NAME,'input_date')
        #input_date.clear()
        for _ in range(10):
            input_date.send_keys(Keys.BACKSPACE)
        input_date.send_keys(ac_to_cc(today_str))
        input_date.send_keys(Keys.TAB)
        time.sleep(5)

        # 定位到 html 元素
        div_element = driver.find_element(By.TAG_NAME, 'html')

        # 取得該 DIV 元素的內容 HTML 原始碼
        inner_html = div_element.get_attribute('innerHTML')
        if len(inner_html)<70000: 
            print("上櫃融券借券賣出餘額無數據或尚未更新...")
            driver.quit()
            #exit(0)
            return True
        tmp_url=f"https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl_result.php?l=zh-tw&d={ac_to_cc(today_str)}&s=0,asc,0&o=htm"

        driver.get(tmp_url)
        time.sleep(5)
        div_element = driver.find_element(By.TAG_NAME, 'html')
        inner_html = div_element.get_attribute('innerHTML')
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
        print('執行期間發生不可預期之錯誤，強制終止程式...10秒後採集程式會重新執行。')
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
        "上櫃融券借券賣出餘額":"https://www.tpex.org.tw/web/stock/margin_trading/margin_sbl/margin_sbl.php?l=zh-tw"
    }
    while 1:
        result=scrapy()
        #print(f"result:{result}")
        if result:
            exit(0)
        else:
            time.sleep(10)