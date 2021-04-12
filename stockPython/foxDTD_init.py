# coding=UTF-8
"""
程式名稱: foxDTD_init.py
程式功能: 初始化 抓取每日上市＆上櫃當沖資訊
Editor: Dennis Yang
修改日期: 2019/04/23
"""
from MyModule.write_file import write_file
tmp='{"host":"","username":"","password":"","filename":""}'
write_file('./ftp_info.json','w',tmp)
