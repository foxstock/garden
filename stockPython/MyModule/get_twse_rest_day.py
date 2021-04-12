import re,requests

def parse_date_from_cht(arg):
	arg=re.sub("(\d{1,2})([^\d]+)(\d{1,2})([^\d]+)",r'\1,\3',arg)
	tmp_arr=arg.split(",")
	if int(tmp_arr[0])<10: tmp_arr[0]='0'+str(tmp_arr[0])
	if int(tmp_arr[1])<10: tmp_arr[1]='0'+str(tmp_arr[1])
	return (tmp_arr[0]+tmp_arr[1])

def get_twse_rest_day():
	url="http://www.twse.com.tw/zh/holidaySchedule/holidaySchedule"
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
	source = str(requests.get(url, headers=headers, timeout=10).text)
	#source=htmlTxt
	rest_day_arr=[]
	source=re.findall('<td align="center">(.*?)</td>', source)
	for i in range(0,len(source),1):
		if source[i].find('月')!=-1:
			#檢查字串內是否有<br/>
			if source[i].find('<br/>')==-1:
				#只有單一個日期 例如:1月2日
				rest_day_arr.append(parse_date_from_cht(source[i]))
			else:
				tmp_arr=source[i].split("<br/>")
				for j in tmp_arr:
					rest_day_arr.append(parse_date_from_cht(j))
	return rest_day_arr
