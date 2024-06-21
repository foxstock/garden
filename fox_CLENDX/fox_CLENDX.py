import time,re,os,pathlib,time,configparser,json
from sys import exit,argv
from datetime import datetime
from time import gmtime,strftime
from WindowMgr import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

def scrapy():
    global config,today_str,toHHMMSS_str,FINAL_CSV_DIR,url_dict
    try:
        service = Service(config['SETTING.chromedriver_loc'])
        # 初始化 Chrome 選項
        options = Options()
        # 添加參數，使 Chrome 瀏覽器最大化
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        try:
            if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(5)
            driver.get(url_dict["證交所首頁"])
        except:
            if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(10)
            driver.get(url_dict["證交所LENDX"])
        if config['SETTING.twse_home_skip']: driver.set_page_load_timeout(10)
        driver.get(url_dict["證交所LENDX"])

        time.sleep(3)

        source_code = driver.page_source
        #print(source_code)
        if len(source_code)<500:
            print("LENDX 無數據或尚未更新...")
            driver.quit()
            #exit(0)
            return True
        #print(source_code)
        json_str=re.findall(r"<pre>(.*?)</pre>",str(source_code))
        #print(json_str)
        with open(FINAL_CSV_DIR+today_str+".csv","w") as csv_file:
            csv_file.writelines('年月日,股票代號,本日借券餘額股,mktype\n')
            json_array=json.loads(json_str[0])
            for i in json_array['data']:
                if(i[0]!='' and i[0]!='合計'):
                    csv_file.writelines("%s,%s,%s,%s\n" % (add_slash_to_date_str(today_str),i[0],remove_comma(i[5]),('0' if i[8]=='集中市場' else '1')))
            print(today_str+"數據儲存完畢!")
        driver.quit()
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
        return True
    except Exception as e:
        print('執行期間發生不可預期之錯誤，強制終止程式...10秒後採集程式會重新執行。')
        driver.quit()
        return False
if __name__ == "__main__":
    #先檢查是否有先前還沒結束的task
    #將當前視窗名設為"CLENDX-DAILY"
    w=WindowMgr()
    w.set_cmd_title("C-L-E-N-D-X-T-E-M-P")
    while 1:
        w.find_window_wildcard("CLENDX-DAILY")
        if w.is_exist==True:
            print("PREV-CLENDX-DAILY FOUND.KILL IT!")
            w.set_foreground()
            w.close_current_window()
            time.sleep(1)
        else:
            break
        time.sleep(1)
    #將DOS視窗名設為"MTSL-DAILY"
    w.find_window_wildcard("C-L-E-N-D-X-T-E-M-P")
    w.set_cmd_title("CLENDX-DAILY") 
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
    yy=today_str[0:4]
    mm=str(int(today_str[4:6]))
    dd=str(int(today_str[6:8]))
    url_dict={
        "證交所首頁":"https://www.twse.com.tw/zh/index.html",
        "證交所LENDX":f"https://www.twse.com.tw/rwd/zh/lending/TWT72U?date={today_str}"
    }
    while 1:
        result=scrapy()
        #print(f"result:{result}")
        if result:
            exit(0)
        else:
            time.sleep(10)