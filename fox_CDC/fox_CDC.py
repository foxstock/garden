import time,re,os,pathlib,time,configparser,requests
from sys import exit,argv
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

#返回變數s的sizes(bytes)
def utf8len(s,encode_type):
    return len(s.encode(encode_type))

def compare_two_txt_content(txt1,txt2):
    #if utf8len(txt1,encode_type)!=utf8len(txt2,encode_type): # 若長度不同,視為有變
    #    return False
    #else:
    for i,v in enumerate(txt1): # 長度相同,逐字比對內容
        if v!=txt2[i]: return False
    return True # 逐字比對內容無異,視為無變

if __name__ == "__main__":
    try:
        #先檢查是否有先前還沒結束的task
        #將當前視窗名設為"CDC-DAILY"
        w=WindowMgr()
        w.set_cmd_title("C-D-C-T-E-M-P")
        while 1:
            w.find_window_wildcard("CDC-DAILY")
            if w.is_exist==True:
                print("PREV-CDC-DAILY FOUND.KILL IT!")
                w.set_foreground()
                w.close_current_window()
                time.sleep(1)
            else:
                break
            time.sleep(1)
        #將DOS視窗名設為"MTSL-DAILY"
        w.find_window_wildcard("C-D-C-T-E-M-P")
        w.set_cmd_title("CDC-DAILY") 
        base_dir = os.getcwd()
        config=ini_to_dict(f"{base_dir}\\setting.ini")
        #print(config)
        FINAL_CSV_DIR = base_dir + "\\FINAL\\"
        # CREATE FINAL CSV DIR IF NOT EXIST
        create_dir_if_not_exist(FINAL_CSV_DIR)
        if len(argv)>1:
            validate_date(argv[1])
            today_str=argv[1]
            toHHMMSS_str="233000"
        else:
            today_str=strftime("%Y%m%d",time.localtime())
            toHHMMSS_str=strftime("%H%M%S",time.localtime())

        work_day_str=get_web_content('http://www.web3d.url.tw/workDate/')
        last3days=get_latest_3days(today_str,work_day_str)
        #print(last3days)
        if last3days:
            print(f"最近三個交易日:{last3days}")
        else:
            print(f"{today_str} 不是交易日!")
            exit()

        url_dict={
        "證交所首頁":"https://www.twse.com.tw/zh/index.html",
        "證交所每日當日沖銷交易標的":"https://www.twse.com.tw/zh/trading/day-trading.html",
        "上櫃現股當沖":"https://www.tpex.org.tw/web/stock/trading/intraday_stat/intraday_trading_stat.php?l=zh-tw"
        }

        service = Service(config['SETTING.chromedriver_loc'])
        # 初始化 Chrome 選項
        options = Options()
        # 添加參數，使 Chrome 瀏覽器最大化
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        try:
            if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(3)
            driver.get(url_dict["證交所首頁"])
        except:
            driver.get(url_dict["證交所每日當日沖銷交易標的"])
        final_ls=[]
    
        for tmp_day in last3days:
            try:
                # 抓取近三天的上市當沖DATA
                yy=tmp_day[0:4]
                mm=str(int(tmp_day[4:6]))
                dd=str(int(tmp_day[6:8]))
                driver.get(url_dict["證交所每日當日沖銷交易標的"])

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

                # 使用 By 類別來定位名稱為 'selectType' 的 select 元素
                select_element = Select(driver.find_element(By.NAME, 'selectType'))  
                # 選擇 value 為 'All' 的選項
                select_element.select_by_value('All')

                time.sleep(1)

                # 使用 XPath 來定位按鈕
                button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/div[1]/div[3]/button')   
                # 對按鈕進行點擊
                button.click()

                time.sleep(5)

                select_element = Select(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/div[2]/div[2]/div[2]/hgroup/div/div[1]/select'))
                select_element.select_by_value('-1')

                time.sleep(5)

                # 定位到 class 名稱為 'rwd-table dragscroll F2 R4_' 的 DIV 元素
                div_element = driver.find_element(By.ID, 'reports')

                # 取得該 DIV 元素的內容 HTML 原始碼
                inner_html = div_element.get_attribute('innerHTML')



                if len(inner_html)<55000:
                    # 今日無數據或尚未更新
                    print("證交所每日當日沖銷無數據或尚未更新...")
                    driver.quit()
                    time.sleep(2)
                    exit(0)
                else:
                    soup = BeautifulSoup(inner_html, 'html.parser')

                    target_table = soup.select_one('div#tables div:nth-child(2) div.main-content div.rwd-table table')

                    cells=[]
                    for row in target_table.find_all('tr'):
                        cells.append( row )

                    for i in range(1,len(cells)):
                        ls=re.findall(r"<td>(.*?)</td>",str(cells[i]))
                        final_ls.append([(tmp_day),ls[0],remove_comma(ls[3]),remove_comma(ls[4]),remove_comma(ls[5])])

                    target_table = soup.select_one('div#tables div:nth-child(1) div.main-content div.rwd-table table')
                    cells=[]
                    for row in target_table.find_all('tr'):
                        cells.append( row )
                    ls=re.findall(r"<td>(.*?)</td>",str(cells[1]))
                    final_ls.append([(tmp_day),'100',remove_comma(ls[0]),remove_comma(ls[2]),remove_comma(ls[4])])
                    #print(final_ls)
            except:
                #print("上市當沖網頁載入過程出錯，程式終止請重試!")
                driver.quit()
                time.sleep(2)
                exit(0)
        time.sleep(5)
        for tmp_day in last3days:
            try:
                yy=tmp_day[0:4]
                mm=str(int(tmp_day[4:6]))
                dd=str(int(tmp_day[6:8]))

                driver.get(url_dict["上櫃現股當沖"])
                time.sleep(5)
                input_date = driver.find_element(By.NAME,'input_date')
                #input_date.clear()
                for _ in range(10):
                    input_date.send_keys(Keys.BACKSPACE)
                input_date.send_keys(ac_to_cc(tmp_day))
                input_date.send_keys(Keys.TAB)
                time.sleep(5)
                div_element = driver.find_element(By.CLASS_NAME, 'rpt-content')
                # 取得該 DIV 元素的內容 HTML 原始碼
                inner_html = div_element.get_attribute('innerHTML')
                #with open("400.txt","w",encoding="utf-8") as f:
                #    f.write(inner_html)
                #print(len(inner_html))
                if len(inner_html)<20000:
                    # 今日無數據或尚未更新
                    print("上櫃當日沖銷無數據或尚未更新...")
                    driver.quit()
                    time.sleep(2)
                    exit(0)
                else:
                    tmp_url="https://www.tpex.org.tw/web/stock/trading/intraday_stat/intraday_trading_stat_result.php?l=zh-tw&d="+ac_to_cc(tmp_day)+"&s=0,asc,0&o=htm"
                    driver.get(tmp_url)
                    time.sleep(5)
                    div_element = driver.find_element(By.TAG_NAME, 'html')
                    inner_html = div_element.get_attribute('innerHTML')
                    soup = BeautifulSoup(inner_html, 'html.parser')
                    target_table = soup.select_one('table#intraday_trading_stat_result tbody')

                    cells=[]
                    for row in target_table.find_all('tr'):
                        cells.append( row )
                    for i in range(0,len(cells)):
                        ls=re.findall(r"<td[^>]*>(.*?)</td>",str(cells[i]))
                        #print(ls)
                        final_ls.append([tmp_day,ls[0],remove_comma(ls[3]),remove_comma(ls[4]),remove_comma(ls[5])])
                    target_tr = soup.select_one('body table tbody')
                    ls=re.findall(r"<td[^>]*>(.*?)</td>",str(target_tr))
                    final_ls.append([tmp_day,'400',remove_comma(ls[0]),remove_comma(ls[2]),remove_comma(ls[4])])
            except:
                print("上櫃當沖網頁載入過程出錯，程式終止請稍候重試...")
                driver.quit()
                time.sleep(2)
                exit(0)
        driver.quit()
        #print(final_ls)
        with open(FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv','w+') as f:
            f.writelines('資料日期,證券代號,當日沖銷交易成交股數,當日沖銷交易買進成交金額,當日沖銷交易賣出成交金額\n')
            for ln in final_ls:
                f.writelines(f"{ln[0]},{ln[1]},{ln[2]},{ln[3]},{ln[4]}\n")
        print('日當沖數據: '+today_str+toHHMMSS_str+'.csv 下載完成!')

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

        if config['SETTING.delete_same_content_at_same_day'] and os.path.isfile(FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv'):
            # 清除同日期相同內容的文字檔，如果 SETTING.delete_same_content_at_same_day 為 True 的話
            # 遍歷資料夾中的所有檔案
            for filename in os.listdir(FINAL_CSV_DIR):
                file_path = os.path.join(FINAL_CSV_DIR, filename)
                #print(file_path)
                # 確保是檔案而不是資料夾
                if os.path.isfile(file_path):
                    tmp_date=str(file_path).split("\\")[-1][:8] # a=yyyymmdd
                    # 比對日期是否相同，若日期相同但檔名不同則比對文字檔內容，若文字檔內容相同則刪除先前已存在的文字檔，保留剛下載的文字檔，若不相同則不做刪除。
                    if tmp_date==today_str and file_path!=FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv':
                        #print(f"compare {file_path}")
                         # 比對兩個文字檔
                        txt1,txt2="",""
                        with open(FINAL_CSV_DIR+today_str+toHHMMSS_str+'.csv','r') as f:
                            txt1=f.read()
                        with open(file_path,'r') as f:
                            txt2=f.read()
                        if compare_two_txt_content(txt1,txt2):
                            # 若文字檔內容相同則刪除先前已存在的文字檔
                            os.remove(file_path)
                            print(f"文字檔內容相同已刪除:{file_path}")
    except Exception as e:
        print('執行期間發生不可預期之錯誤，強制終止程式...當前自動化Chrome視窗會在下一次採集程式執行時自動關閉。')
        time.sleep(1)
        exit(0)