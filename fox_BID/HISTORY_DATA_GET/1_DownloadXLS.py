import urllib.request
from time import sleep
url_list=[
["景氣指標及燈號_from1982.xls","https://index.ndc.gov.tw/n/excel/data/eco/indicators?sy=1982&sm=1&ey=2019&em=10&id=2%2C12%2C13%2C14%2C25%2C26%2C33%2C34&sq=0,0,0"],
["製造業採購經理人指數_from2012.xls","https://index.ndc.gov.tw/n/excel/data/PMI/total?sy=2012&sm=1&ey=2019&em=10&id=55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63%2C64%2C65%2C66&sq=0,0,0"],
["非製造業經理人指數_from2014.xls","https://index.ndc.gov.tw/n/excel/data/NMI/total?sy=2014&sm=1&ey=2019&em=10&id=160%2C161%2C162%2C163%2C164%2C165%2C166%2C167%2C168%2C169%2C170%2C171%2C172&sq=0,0,0"]
]
#urllib.request.urlretrieve(url,"testDL.xls")
for i in url_list:
	c_xls=i[0]
	c_url=i[1]
	#print(url_list[0][0])
	urllib.request.urlretrieve(c_url,c_xls)
	print(c_xls+'download OK')
	sleep(5)
"""
import requests
url="https://index.ndc.gov.tw/n/excel/data/eco/indicators?sy=1982&sm=1&ey=2019&em=7&id=2%2C12%2C13%2C14%2C25%2C26%2C33%2C34&sq=0,0,0"
r=requests.get(url)
print(r.text)

with open('testDL.txt', 'w') as the_file:
    the_file.write(r.text)
"""