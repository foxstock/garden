# 景氣指標查詢系統
# https://index.ndc.gov.tw/n/zh_tw
import os,datetime,requests
from time import sleep
import pandas as pd
from zipfile import ZipFile  
from os.path import basename

def del_files_from_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

#import c_xls
def fix_year_month(arg):
    return arg.replace("-","/")

def fix_datetime_format(arg):
    return str(arg[:4])+'/'+arg[4:6]

def get_all_file_paths(directory): 
    # initializing empty file paths list 
    file_paths = [] 
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
    # returning all file paths 
    return file_paths

def step1():
    currDay = datetime.date.today()
    """try:
        last3monthDay = currDay.replace(month=currDay.month-3)
    except ValueError:
        if currDay.month == 1:
            last3monthDay = currDay.replace(year=currDay.year-1, month=(12-1))
        else:
            raise"""
    #last3monthDay
    url_list=[
    ["TWBID"+str(currDay.year)+str(currDay.month)+".xls","https://index.ndc.gov.tw/n/excel/data/eco/indicators?sy=%s&sm=%s&ey=%s&em=%s"%('1984','01',str(currDay.year),str(currDay.month))+"&id=2%2C12%2C13%2C14%2C25%2C26%2C33%2C34&sq=0,0,0"],
    ["TWPMI"+str(currDay.year)+str(currDay.month)+".xls","https://index.ndc.gov.tw/n/excel/data/PMI/total?sy=%s&sm=%s&ey=%s&em=%s"%('2012','07',str(currDay.year),str(currDay.month))+"&id=55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63%2C64%2C65%2C66&sq=0,0,0"],
    ["TWNMI"+str(currDay.year)+str(currDay.month)+".xls","https://index.ndc.gov.tw/n/excel/data/NMI/total?sy=%s&sm=%s&ey=%s&em=%s"%('2014','08',str(currDay.year),str(currDay.month))+"&id=160%2C161%2C162%2C163%2C164%2C165%2C166%2C167%2C168%2C169%2C170%2C171%2C172&sq=0,0,0"]
    ]
    #print(url_list)
    saveDir="SOURCE_XLS/"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    else:
        del_files_from_folder(saveDir)
    for i in url_list:
        c_xls=i[0]
        c_url=i[1]
        resp=requests.get(c_url)
        output = open(saveDir+c_xls, 'wb')
        output.write(resp.content)
        output.close()
        print(c_xls,resp)
        sleep(5)

def step2():
    """ XLS to CSV """
    currDay = datetime.date.today()
    XLS_arr=[]
    XLS_arr.append("TWBID"+str(currDay.year)+str(currDay.month))
    XLS_arr.append("TWPMI"+str(currDay.year)+str(currDay.month))
    XLS_arr.append("TWNMI"+str(currDay.year)+str(currDay.month))

    XLS_dir=os.getcwd()+"/SOURCE_XLS/"
    CSV_dir=os.getcwd()+"/SOURCE_CSV/"
    if not os.path.exists(CSV_dir):
        os.makedirs(CSV_dir)
    for i in XLS_arr:
        filePath=XLS_dir+i+'.xls'
        out_csv=CSV_dir+i+'.csv'
        data = pd.read_excel(filePath, sheet_name='Worksheet',skiprows=3)
        data.to_csv(out_csv, encoding='utf-8', index=False,sep=',')
        print(filePath+' convert to '+out_csv)

def step3():
    s_folder='SOURCE_CSV/'
    e_folder='TEMP_CSV/'
    if not os.path.exists(e_folder):
        os.makedirs(e_folder)
    else:
        del_files_from_folder(e_folder)
    currDay = datetime.date.today()
    csv_file=[]
    csv_file.append("TWBID"+str(currDay.year)+str(currDay.month))
    csv_file.append("TWPMI"+str(currDay.year)+str(currDay.month))
    csv_file.append("TWNMI"+str(currDay.year)+str(currDay.month))
    csv_save_filename=['TWPI','TWPMI','TWNMI']
    #處理BID.start
    with open(s_folder+csv_file[0]+".csv","r",encoding="utf-8") as text_file:
        lines = text_file.read().split('\n')
    text_file.close()

    csv_file2 = open(e_folder+csv_save_filename[0]+".csv", "w",encoding="utf-8")
    csv_file2.writelines("年月,景氣對策信號(分),領先指標不含趨勢指數(點),同時指標不含趨勢指數(點),落後指標不含趨勢指數(點)\n")
    for i in range(0,len(lines)):
        tmp_list=lines[i].split(',')
        if(tmp_list[0]!=''):
            print("%s,%s,%s,%s,%s" % (fix_year_month(tmp_list[0]),str(tmp_list[2]),str(tmp_list[4]),str(tmp_list[6]),str(tmp_list[8])))
            csv_file2.writelines("%s,%s,%s,%s,%s\n" % (fix_year_month(tmp_list[0]),str(tmp_list[2]),str(tmp_list[4]),str(tmp_list[6]),str(tmp_list[8])))
    csv_file2.close()
    #處理BID.end

    #處理PMI.start
    with open(s_folder+csv_file[1]+".csv","r",encoding="utf-8") as text_file:
        lines = text_file.read().split('\n')
    text_file.close()

    csv_file2 = open(e_folder+csv_save_filename[1]+".csv", "w",encoding="utf-8")
    csv_file2.writelines("年月,製造業PMI(%),新增訂單數量(%),生產數量(%),人力僱用數量(%),供應商交貨時間(%),存貨(%)\n")
    for i in range(0,len(lines)):
        tmp_list=lines[i].split(',')
        if(tmp_list[0]!=''):
            print("%s,%s,%s,%s,%s,%s,%s" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5]),str(tmp_list[6])))
            csv_file2.writelines("%s,%s,%s,%s,%s,%s,%s\n" % (fix_year_month(tmp_list[0]),str(tmp_list[9]),str(tmp_list[10]),str(tmp_list[11]),str(tmp_list[12]),str(tmp_list[1]),str(tmp_list[2])))
    csv_file2.close()
    #處理PMI.end

    #處理NMI.start
    with open(s_folder+csv_file[2]+".csv","r",encoding="utf-8") as text_file:
        lines = text_file.read().split('\n')
    text_file.close()

    csv_file2 = open(e_folder+csv_save_filename[2]+".csv", "w",encoding="utf-8")
    csv_file2.writelines("年月,臺灣非製造業NMI(%),商業活動(%),新增訂單(%),人力僱用(%),供應商交貨時間(%)\n")
    for i in range(0,len(lines)):
        tmp_list=lines[i].split(',')
        if(tmp_list[0]!=''):
            print("%s,%s,%s,%s,%s,%s" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5])))
            csv_file2.writelines("%s,%s,%s,%s,%s,%s\n" % (fix_year_month(tmp_list[0]),str(tmp_list[1]),str(tmp_list[2]),str(tmp_list[3]),str(tmp_list[4]),str(tmp_list[5])))
    csv_file2.close()
    #處理NMI.end

def step4():
    """ description """
    d = datetime.datetime.now()
    currentDateStr=d.strftime("%Y%m%d%H%M%S")
    # path to folder which needs to be zipped 
    tmp_csv_dir = 'TEMP_CSV'
    output_dir ='OUTPUT/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # calling function to get all file paths in the directory 
    file_paths = get_all_file_paths(tmp_csv_dir) 

    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file_name in file_paths: 
        print(file_name) 

    # writing files to a zipfile 
    with ZipFile(output_dir+'TWPI_'+currentDateStr+'.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths:
            zip.write(file,basename(file)) 
    zip.close
    print('[ TWPI_'+currentDateStr+'.zip ] All files zipped successfully!')      


if __name__ == '__main__':
    step1()
    step2()
    step3()
    step4()
    #pass