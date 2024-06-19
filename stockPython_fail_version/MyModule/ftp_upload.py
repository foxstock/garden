# coding=UTF-8
import ftplib
def ftp_upload(file_local,final_file,loginInfo):
	FTP = ftplib.FTP(loginInfo['host'],loginInfo['username'],loginInfo['password'])
	FTP.cwd('/www/TWDTD/')
	FILE = file_local
	FTP.storbinary("STOR " + final_file, open(FILE, 'rb'))
	FTP.quit()
	return True
