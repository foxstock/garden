import time
from datetime import datetime, timedelta

def check_work_day(dateStr):
	ckday = datetime.strptime(dateStr, '%Y%m%d').weekday()
	if ckday<5:
		return True # Mon - Fri
	else:
		return False # Sat - Sun