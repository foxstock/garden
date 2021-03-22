s_folder='SOURCE_CSV\\'
e_folder='TEMP_CSV\\'

import datetime
currDay = datetime.date.today()

csv_file=[]
csv_file.append("TWBID"+str(currDay.year)+str(currDay.month))
csv_file.append("TWPMI"+str(currDay.year)+str(currDay.month))
csv_file.append("TWNMI"+str(currDay.year)+str(currDay.month))

csv_save_filename=['TWPI','TWPMI','TWNMI']
def fix_year_month(arg):
	return arg.replace("-","/")

def fix_datetime_format(arg):
	return str(arg[:4])+'/'+arg[4:6]

#處理BID.start
with open(s_folder+csv_file[0]+".csv","r",encoding="utf-8") as text_file:
	lines = text_file.read().split('\n')
text_file.close()

csv_file2 = open(e_folder+csv_save_filename[0]+".csv", "w",encoding="utf-8")
csv_file2.writelines("年月,景氣對策信號(分),領先指標不含趨勢指數(點),同時指標不含趨勢指數(點),落後指標不含趨勢指數(點)\n")
for i in range(0,len(lines)):
	tmp_list=lines[i].split(',')
	if(tmp_list[0]!=''):
		print("%s,%s,%s,%s,%s" % (fix_year_month(tmp_list[0]),str(tmp_list[2]),str(tmp_list[4]),str(tmp_list[6]),str(tmp_list[8])))
		csv_file2.writelines("%s,%s,%s,%s,%s\n" % (fix_year_month(tmp_list[0]),str(tmp_list[2]),str(tmp_list[4]),str(tmp_list[6]),str(tmp_list[8])))
csv_file2.close()
#處理BID.end

#處理PMI.start
with open(s_folder+csv_file[1]+".csv","r",encoding="utf-8") as text_file:
	lines = text_file.read().split('\n')
text_file.close()

csv_file2 = open(e_folder+csv_save_filename[1]+".csv", "w",encoding="utf-8")
csv_file2.writelines("年月,製造業PMI(%),新增訂單數量(%),生產數量(%),人力僱用數量(%),供應商交貨時間(%),存貨(%)\n")
for i in range(0,len(lines)):
	tmp_list=lines[i].split(',')
	if(tmp_list[0]!=''):
		print("%s,%s,%s,%s,%s,%s,%s" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5]),str(tmp_list[6])))
		csv_file2.writelines("%s,%s,%s,%s,%s,%s,%s\n" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5]),str(tmp_list[6])))
csv_file2.close()
#處理PMI.end

#處理NMI.start
with open(s_folder+csv_file[2]+".csv","r",encoding="utf-8") as text_file:
	lines = text_file.read().split('\n')
text_file.close()

csv_file2 = open(e_folder+csv_save_filename[2]+".csv", "w",encoding="utf-8")
csv_file2.writelines("年月,臺灣非製造業NMI(%),商業活動(%),新增訂單(%),人力僱用(%),供應商交貨時間(%)\n")
for i in range(0,len(lines)):
	tmp_list=lines[i].split(',')
	if(tmp_list[0]!=''):
		print("%s,%s,%s,%s,%s,%s" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5])))
		csv_file2.writelines("%s,%s,%s,%s,%s,%s\n" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5])))
csv_file2.close()
#處理NMI.end