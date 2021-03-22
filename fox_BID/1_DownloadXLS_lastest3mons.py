import urllib.request,datetime,requests
from time import sleep

currDay = datetime.date.today()
try:
	last3monthDay = currDay.replace(month=currDay.month-3)
except ValueError:
	if currDay.month == 1:
		last3monthDay = currDay.replace(year=currDay.year-1, month=(12-2))
	else:
		raise

url_list=[
["TWBID"+str(currDay.year)+str(currDay.month)+".xls","https://index.ndc.gov.tw/n/excel/data/eco/indicators?sy=%s&sm=%s&ey=%s&em=%s"%(str(last3monthDay.year),str(last3monthDay.month),str(currDay.year),str(currDay.month))+"&id=2%2C12%2C13%2C14%2C25%2C26%2C33%2C34&sq=0,0,0"],
["TWPMI"+str(currDay.year)+str(currDay.month)+".xls","https://index.ndc.gov.tw/n/excel/data/PMI/total?sy=%s&sm=%s&ey=%s&em=%s"%(str(last3monthDay.year),str(last3monthDay.month),str(currDay.year),str(currDay.month))+"&id=55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63%2C64%2C65%2C66&sq=0,0,0"],
["TWNMI"+str(currDay.year)+str(currDay.month)+".xls","https://index.ndc.gov.tw/n/excel/data/NMI/total?sy=%s&sm=%s&ey=%s&em=%s"%(str(last3monthDay.year),str(last3monthDay.month),str(currDay.year),str(currDay.month))+"&id=160%2C161%2C162%2C163%2C164%2C165%2C166%2C167%2C168%2C169%2C170%2C171%2C172&sq=0,0,0"]
]
#print(url_list)

saveDir="SOURCE_XLS\\"
for i in url_list:
	c_xls=i[0]
	c_url=i[1]
	resp=requests.get(c_url)
	output = open(saveDir+c_xls, 'wb')
	output.write(resp.content)
	output.close()
	print(resp)
	sleep(5)
