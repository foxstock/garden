# coding=UTF-8
import ftplib

with open('./ftp_info.json') as f:
	json_data = json.load(f)
	
if json_data['filename']=='':
	print("ERROR!今日當沖彙整CSV還沒準備好!")
	exit()

host = json_data['host']
username = json_data['username']
password = json_data['password']

f = ftplib.FTP(host)  # 實例化FTP對象
f.login(username, password)  # 登錄
# 獲取當前路徑
pwd_path = f.pwd()
print("FTP當前路徑:", pwd_path)


def ftp_upload(final_file):
    #‘‘‘以二進制形式上傳文件‘‘‘
    file_remote = '/www/TWDTD/'+final_file
    file_local = 'final\\'+final_file
    bufsize = 1024  # 設置緩沖器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()

ftp_upload(str(json_data['filename']))
f.quit()

print(final_file+' Upload completed!')
