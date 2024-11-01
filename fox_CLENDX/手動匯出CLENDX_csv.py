# 年月日,股票代號,本日借券餘額股,mktype
# 2024/06/17,0050,29225000,0

from bs4 import BeautifulSoup
import re,json

def add_slash_to_date_str(date_str):
    return f"{date_str[0:4]}/{date_str[4:6]}/{date_str[6:8]}"

def remove_comma(num_str):
    return str(num_str).replace(",","")

today_str=input("CLENDX txt2csv 輸入要處理的日期:")

with open(f"CLENDX_TW_{today_str}.txt","r") as f:
    source = f.read()

json_str=re.findall(r"<pre>(.*?)</pre>",source)
#print(json_str)

with open("CMTSL_"+today_str+".csv","w") as csv_file:
    csv_file.writelines('年月日,股票代號,本日借券餘額股,mktype\n')
    json_array=json.loads(json_str[0])
    for i in json_array['data']:
        if(i[0]!='' and i[0]!='合計'):
            csv_file.writelines("%s,%s,%s,%s\n" % (add_slash_to_date_str(today_str),i[0],remove_comma(i[5]),('0' if i[8]=='集中市場' else '1')))
    print(today_str+"數據儲存完畢!")