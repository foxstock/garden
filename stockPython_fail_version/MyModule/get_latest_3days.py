import numpy as np

def get_latest_3days(dateStr,work_day_str):
	work_day_arr=work_day_str.split("\n")#np.loadtxt(work_day_str,dtype=str,unpack=True, ndmin = 1)
	print('日期: '+dateStr)
	tmpnum=0
	today_inT2=0
	for i in work_day_arr:
		#print(i)
		if i==dateStr:
			today_inT2=1
			break
		else:
			tmpnum=tmpnum+1
	if today_inT2==0:
		print("今天不是交易日!")
		return False

	t2 = []
	t2.append(str(work_day_arr[tmpnum-2]))
	t2.append(str(work_day_arr[tmpnum-1]))
	t2.append(str(work_day_arr[tmpnum]))
	return (t2)