# %%
import time,re,os,pathlib,time,configparser
from sys import exit,argv
from datetime import datetime
from time import gmtime,strftime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import ActionChains

from bs4 import BeautifulSoup

#TWPMI
url="https://index.ndc.gov.tw/n/zh_tw/data/NMI#/"

service = Service("C:\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(url)

show_table_link = driver.find_element(By.LINK_TEXT,"表格")
show_table_link.click()

show_table_link = driver.find_element(By.LINK_TEXT,"商業活動")
show_table_link.click()

show_table_link = driver.find_element(By.LINK_TEXT,"新增訂單")
show_table_link.click()

show_table_link = driver.find_element(By.LINK_TEXT,"人力僱用")
show_table_link.click()

show_table_link = driver.find_element(By.LINK_TEXT,"供應商交貨時間")
show_table_link.click()


drag = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div[2]/div[2]/div[3]/span[1]")))
drop = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div[2]/div[1]/div[2]/ul/li/a")))
ActionChains(driver).drag_and_drop(drag,drop).perform()

table = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div[2]/div[7]/div[2]/div[3]/table/tbody")

source = table.get_attribute('innerHTML')
source = source.replace("\n","").replace("                                    ","")
source=re.sub("<!-- .*? -->","",source)
source=re.sub("<div .*?>","",source)
source=re.sub("<span .*?>","",source)
source=re.sub("<img .*?>","",source)
source=re.sub("</div>","",source)
source=re.sub("<div>","",source)
source=re.sub("</span>","",source)
source=re.sub("<tr .*?>","<tr>",source)
source=re.sub("<td .*?>","<td>",source)
source = source.replace("    ","")

# web table欄位順序:
# 年月	臺灣非製造業NMI(%)	商業活動(%)	新增訂單(%)	人力僱用(%)	供應商交貨時間(%)
# 0     1                   2           3          4           5       
# 要輸出的順序:
# 年月,臺灣非製造業NMI(%),商業活動(%),新增訂單(%),人力僱用(%),供應商交貨時間(%)
# 0    1                   2            3       4           5

twpmi_ls=re.findall("<tr><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td></tr>",source)
with open("TWNMI.csv","w+") as f:
     f.writelines("年月,臺灣非製造業NMI(%),商業活動(%),新增訂單(%),人力僱用(%),供應商交貨時間(%)\n")
     for i in twpmi_ls:
         tmp_ym=i[0].replace("-","/")
         f.writelines(f"{tmp_ym},{i[1]},{i[2]},{i[3]},{i[4]},{i[5]}\n")

print("TWNMI.csv 下載完成")
driver.close()

