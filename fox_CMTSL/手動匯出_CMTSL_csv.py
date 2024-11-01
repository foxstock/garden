# export example:
# 年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype
# 2024/06/19,0050,1066000,700000,0,20605000,2740459,0
from bs4 import BeautifulSoup
import re

def add_slash_to_date_str(date_str):
    return f"{date_str[0:4]}/{date_str[4:6]}/{date_str[6:8]}"

def remove_comma(num_str):
    return str(num_str).replace(",","")

today_str=input("CMTSL txt2csv 輸入要處理的日期:")

# 上市
with open(f"CMTSL_TW_{today_str}.txt","r") as f:
    source = f.read()
source=source.replace("\n","").replace("    ","")
#print(source)
soup = BeautifulSoup(source, 'html.parser')
result = soup.select('table:nth-of-type(1) tbody tr')
#print(result[0])
final_ls=[]
for i in result:
    tmp = re.findall("<td[^>]*>(.*?)</td>",str(i))
    #print(tmp)
    # ['6869', '雲豹能源', '214,000', '11,000', '5,000', '0', '220,000', '34,294,298', '4,646,000', v'5,000', '0', '0', '4,651,000', '1,264,613', ' ']
    # useful 0 9 10 11 12 13
    if tmp[0]!="" and len(tmp)>=14:
        final_ls.append([ add_slash_to_date_str(today_str),tmp[0],remove_comma(tmp[9]),remove_comma(tmp[10]),remove_comma(tmp[11]),remove_comma(tmp[12]),remove_comma(tmp[13]),'0' ])
#print(final_ls)

# 上櫃
with open(f"CMTSL_TO_{today_str}.txt","r") as f:
    source = f.read()
source=source.replace("\n","").replace("    ","")
soup = BeautifulSoup(source, 'html.parser')
result = soup.select('table:nth-of-type(1) tbody tr')
for i in result:
    tmp = re.findall("<td[^>]*>(.*?)</td>",str(i))
    #print(tmp)
    # ['6869', '雲豹能源', '214,000', '11,000', '5,000', '0', '220,000', '34,294,298', '4,646,000', v'5,000', '0', '0', '4,651,000', '1,264,613', ' ']
    # useful 0 9 10 11 12 13
    if tmp[0]!="" and len(tmp)>=14:
        final_ls.append([ add_slash_to_date_str(today_str),tmp[0],remove_comma(tmp[9]),remove_comma(tmp[10]),remove_comma(tmp[11]),remove_comma(tmp[12]),remove_comma(tmp[13]),'1' ])
#print(final_ls)
with open(f"{today_str}.csv","w+") as f:
    f.writelines("年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype\n")
    for ln in final_ls:
        f.writelines(f"{ln[0]},{ln[1]},{ln[2]},{ln[3]},{ln[4]},{ln[5]},{ln[6]},{ln[7]}\n")

print(f"{today_str}.csv SAVED!")