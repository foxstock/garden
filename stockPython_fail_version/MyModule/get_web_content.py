import requests,re
import time
from MyModule.log_writer import log_writer
from MyModule.get_fake_userAgent import get_fake_userAgent

def get_web_content(url):
	while 1:
		try:
			headers=get_fake_userAgent()
			print(headers)
			r=requests.get(url,headers=headers, timeout=10)
			r.encode='utf-8'
			if(r.status_code==200):
				log_writer("Success on get_web_content(%s)" %(url))
				break
			else:
				log_writer("Status_code!=200 on get_web_content(%s) Retry requests.get" %(url))
				time.sleep(5)
		except:
			log_writer("Errors on get_web_content(%s)" %(url))
			time.sleep(5)
	return r.text