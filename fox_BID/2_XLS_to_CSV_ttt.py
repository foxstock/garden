# coding:utf-8
from win32com.client import Dispatch
import os
#import pandas as pd,xlrd
import datetime
currDay = datetime.date.today()

XLS_arr=[]
XLS_arr.append("TWBID"+str(currDay.year)+str(currDay.month))
XLS_arr.append("TWPMI"+str(currDay.year)+str(currDay.month))
XLS_arr.append("TWNMI"+str(currDay.year)+str(currDay.month))

XLS_dir=os.getcwd()+"\\SOURCE_XLS\\"
CSV_dir=os.getcwd()+"\\SOURCE_CSV\\"



def xls_to_csv():
	for i in XLS_arr:
		filePath=XLS_dir+i+'.xls'
		print(XLS_dir+i+'.xls')
		xl = Dispatch('Excel.Application')
		wb = xl.Workbooks.Open(filePath)
		wb.Worksheets(1)
		wb.SaveAs(CSV_dir+i+'.csv',6)
		"""
		ws = wb.Worksheets(1)
		info = ws.UsedRange
		rowsLen=info.Rows.count
		rows = info.Rows
		with open(CSV_dir+i+'.csv','w',encoding='utf-8') as f:
			for j in range(2,rowsLen):
				f.writelines(str(rows[j]).replace("(","").replace("),)","").replace(" ","").replace("'","")+'\n')
		f.close()
		"""
		wb.Close(True)
		#print (rows[2])
		#tmpXLS=pd.read_excel(XLS_dir+i+'.xls',header=0, skiprows=2)
		#tmpXLS.to_csv(CSV_dir+i+'.csv',index=False,encoding='utf-8')

if __name__ == '__main__':
	xls_to_csv()