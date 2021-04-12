
text_file = open("workDate.txt", "r")
lines = text_file.read().split('\n')
text_file.close()
#json_file=lines[3490]
#sprint(json_file)

import json

def clean_outdatetime(arg):
	tmp_arr=arg.replace(' 00:00:00','').split('-')
	return str(int(tmp_arr[0])-1900)+str(tmp_arr[1])+str(tmp_arr[2])

def calc_time_from_1900(arg):
	return str(int(arg[:4])-1900)+arg[4:6]+arg[6:8]

def fix_datetime_format(arg):
	return str(arg[:4])+'/'+arg[4:6]+'/'+arg[6:8]

def num_comma_clear(arg):
	return arg.replace(",","")

csv_file = open("TO借券賣出_從"+lines[0]+"至"+lines[len(lines)-1]+".csv", "w")

csv_file.writelines('年月日,股票代號,當日賣出,當日還券,當日調整,當日餘額,次一營業日可限額,mktype\n')
for json_file in lines:
	input_file = open ("SOURCE_JSON_TO\\"+json_file+'.json',encoding='utf-8')
	json_array = json.load(input_file)
	#print(json_array['data'])
	for i in json_array['aaData']:
		if(i[0]!=''):
			if int(json_file)<20120317:
				print("%s,%s,%s,%s,%s,%s,%s" % (fix_datetime_format(json_file),i[0],num_comma_clear(i[7]),num_comma_clear(i[8]),num_comma_clear(i[9]),num_comma_clear(i[10]),num_comma_clear(i[11])))
				csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,1\n" % (fix_datetime_format(json_file),i[0],num_comma_clear(i[7]),num_comma_clear(i[8]),num_comma_clear(i[9]),num_comma_clear(i[10]),num_comma_clear(i[11])))
			elif (int(json_file)>20120317 and int(json_file)<20121002):
				print("%s,%s,%s,%s,%s,%s,%s" % (fix_datetime_format(json_file),i[0],num_comma_clear(i[8]),num_comma_clear(i[9]),num_comma_clear(i[10]),num_comma_clear(i[11]),num_comma_clear(i[12])))
				csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,1\n" % (fix_datetime_format(json_file),i[0],num_comma_clear(i[8]),num_comma_clear(i[9]),num_comma_clear(i[10]),num_comma_clear(i[11]),num_comma_clear(i[12])))
			else:
				print("%s,%s,%s,%s,%s,%s,%s" % (fix_datetime_format(json_file),i[0],num_comma_clear(i[9]),num_comma_clear(i[10]),num_comma_clear(i[11]),num_comma_clear(i[12]),num_comma_clear(i[13])))
				csv_file.writelines("%s,%s,%s,%s,%s,%s,%s,1\n" % (fix_datetime_format(json_file),i[0],num_comma_clear(i[9]),num_comma_clear(i[10]),num_comma_clear(i[11]),num_comma_clear(i[12]),num_comma_clear(i[13])))
csv_file.close()