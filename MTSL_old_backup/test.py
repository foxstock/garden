import time,json,os,pathlib
from time import gmtime, strftime
import lib.myModule as my


today_str=strftime("%Y%m%d", time.localtime())
toHHMMSS_str=strftime("%H%M%S", time.localtime())
today = today_str if my.check_today_is_workday_and_not_twse_rest_day(today_str) else False
print(("Current Date: %s" % today) if today!=False else "今天不是交易日")