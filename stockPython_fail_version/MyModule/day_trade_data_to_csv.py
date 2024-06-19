import json
from MyModule.log_writer import log_writer

def day_trade_data_to_csv(c_date,s_url,d_url,d_type):
	if d_type=='TWSE':
		with open(s_url) as json_data:
				tmpDate=c_date
				d = json.load(json_data)
				d_array=d['data']
				file = open(d_url, 'w+')
				for tmpI in d_array:
					file.write(tmpDate+','+tmpI[0]+','+tmpI[3].replace(',','')+','+tmpI[4].replace(',','')+','+tmpI[5].replace(',','')+'\n')
				file.close()
		log_writer("Success on day_trade_data_to_csv(%s)" %(d_url))
	elif d_type=='100':
		with open(s_url) as json_data:
			tmpDate=c_date
			d = json.load(json_data)
			if d['creditList']!="":
				file = open(d_url, 'w+')
				file.write(tmpDate+',100,'+str(d['creditList'][0][0]).replace(',','')+','+str(d['creditList'][0][2]).replace(',','')+','+str(d['creditList'][0][4]).replace(',','')+'\n')
				file.close()
		log_writer("Success on day_trade_data_to_csv(%s)" %(d_url))
	elif d_type=='TPEX':
		with open(s_url) as json_data:
			tmpDate=c_date
			d = json.load(json_data)
			d_array=d['aaData']
			file = open(d_url, 'w+')
			for tmpI in d_array:
				file.write(tmpDate+','+tmpI[0]+','+tmpI[3].replace(',','')+','+tmpI[4].replace(',','')+','+tmpI[5].replace(',','')+'\n')
			file.close()
		log_writer("Success on day_trade_data_to_csv(%s)" %(d_url))
	elif d_type=='400':
		with open(s_url) as json_data:
			tmpDate=c_date
			d = json.load(json_data)
			if d['stat_0']!="":
				file = open(d_url, 'w+')
				file.write(tmpDate+',400,'+d['stat_0'].replace(',','')+','+d['stat_2'].replace(',','')+','+d['stat_4'].replace(',','')+'\n')
				file.close()
		log_writer("Success on day_trade_data_to_csv(%s)" %(d_url))
	else:
		pass


