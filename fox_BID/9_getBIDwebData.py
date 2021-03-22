import re
from requests_html import HTMLSession

url_list=[
['TWBID01','https://index.ndc.gov.tw/n/zh_tw/data/eco/indicators_table1'],
['TWBID02','https://index.ndc.gov.tw/n/zh_tw/data/eco/indicators_table2'],
['TWBID03','https://index.ndc.gov.tw/n/zh_tw/coincident#/'],
['TWBID04','https://index.ndc.gov.tw/n/zh_tw/lagged#/'],
['TWPMI','https://index.ndc.gov.tw/n/zh_tw/PMI#/'],
['TWNMI','https://index.ndc.gov.tw/n/zh_tw/NMI#/'],
]

for i in url_list:
	c_url=i[1]
	c_fname=i[0]
	print(c_url)
	session = HTMLSession()
	r = session.get(c_url)
	r.html.render(sleep=15)
	content=r.html.html

	with open(c_fname+'.htm','w',encoding='utf-8') as f:
		f.write(content)