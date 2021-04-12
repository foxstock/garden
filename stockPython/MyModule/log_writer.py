import time,os,pathlib
from time import gmtime, strftime
from datetime import datetime, timedelta

def log_writer(arg):
	today_str=strftime("%Y%m%d", time.localtime())
	toHHMM_str=strftime("%H%M%S", time.localtime())
	#print("%s %s" %(today_str,toHHMM_str))
	base_dir = os.path.dirname(os.path.realpath(__file__))+"\\log\\"
	pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True) 
	file=open(base_dir+'event.log','a+')
	file.writelines("'%s %s', '%s'\r\n" %(today_str,toHHMM_str,arg))
	file.close

