# 資料來源網址 https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
# 這個版本僅適用於linux或macOS作業系統
import requests,zipfile,os,shutil
import numpy as np
import pandas as pd
from zipfile import ZipFile
from os.path import basename
import array_setting as arr_as

""" 取得檔名(不含路徑及副檔名) """
def get_file_name(input_str1):
    return (input_str1.split("/")[-1]).split(".")[0]

def get_short_name(arg):
    tmp_arg=arg.replace('"','')
    for si in range(0,len(arr_as.want_arr),1):
        if tmp_arg==arr_as.want_arr[si][0]:
            #print(want_arr2[si][2])
            return arr_as.want_arr[si][2]

def clean_outdatetime(arg):
    tmp_arr=arg.replace(' 00:00:00','').split('-')
    return str(int(tmp_arr[0])-1900)+str(tmp_arr[1])+str(tmp_arr[2])

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
    """ 下載zip並解壓縮為xls """
    url_list=[
        ["dea_fut_xls_2019.zip","https://www.cftc.gov/files/dea/history/dea_fut_xls_2019.zip"],
        ["dea_fut_xls_2020.zip","https://www.cftc.gov/files/dea/history/dea_fut_xls_2020.zip"],
        ["dea_fut_xls_2021.zip","https://www.cftc.gov/files/dea/history/dea_fut_xls_2021.zip"]
    ]
    zip_folder='SOURCE_ZIP/'
    # 如果沒有 SOURCE_ZIP 資料夾就新增
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)
    source_xls_folder='SOURCE_XLS/'
    if not os.path.exists(source_xls_folder):
        os.makedirs(source_xls_folder)
    for i in url_list:
        c_zip_name=i[0]
        c_zip_url=i[1]
        myfile = requests.get(c_zip_url, allow_redirects=True)
        open(zip_folder+c_zip_name, 'wb').write(myfile.content)
        #解壓縮 zip 檔
        with zipfile.ZipFile(zip_folder+c_zip_name, 'r') as zip_ref:
            zip_ref.extractall(source_xls_folder)
        source_xls=source_xls_folder+'annual.xls'
        dest_xls=source_xls_folder+get_file_name(c_zip_name)+'.xls'
        if os.path.isfile(dest_xls):
            os.remove(dest_xls)
        os.rename(source_xls, dest_xls)
        print(dest_xls+' 下載完成!')

def step2():
    """ description """
    source_xls_folder='SOURCE_XLS/'
    source_csv_folder='SOURCE_CSV/'
    if not os.path.exists(source_csv_folder):
        os.makedirs(source_csv_folder)
    XLS_arr=['FUT86_06','FUT07_14','FUT15_16','FUT17','FUT18','dea_fut_xls_2019','dea_fut_xls_2020','dea_fut_xls_2021']
    for xi in XLS_arr:
        source_xls=source_xls_folder+xi+'.xls'
        dest_csv=source_csv_folder+xi+'.csv'
        if os.path.isfile(dest_csv):
            os.remove(dest_csv)
        data = pd.read_excel(source_xls, sheet_name='XLS')
        data.columns = ['Market_and_Exchange_Names','As_of_Date_In_Form_YYMMDD','Report_Date_as_MM_DD_YYYY','CFTC_Contract_Market_Code','CFTC_Market_Code','CFTC_Region_Code','CFTC_Commodity_Code','Open_Interest_All','NonComm_Positions_Long_All','NonComm_Positions_Short_All','NonComm_Postions_Spread_All','Comm_Positions_Long_All','Comm_Positions_Short_All','Tot_Rept_Positions_Long_All','Tot_Rept_Positions_Short_All','NonRept_Positions_Long_All','NonRept_Positions_Short_All','Open_Interest_Old','NonComm_Positions_Long_Old','NonComm_Positions_Short_Old','NonComm_Positions_Spread_Old','Comm_Positions_Long_Old','Comm_Positions_Short_Old','Tot_Rept_Positions_Long_Old','Tot_Rept_Positions_Short_Old','NonRept_Positions_Long_Old','NonRept_Positions_Short_Old','Open_Interest_Other','NonComm_Positions_Long_Other','NonComm_Positions_Short_Other','NonComm_Positions_Spread_Other','Comm_Positions_Long_Other','Comm_Positions_Short_Other','Tot_Rept_Positions_Long_Other','Tot_Rept_Positions_Short_Other','NonRept_Positions_Long_Other','NonRept_Positions_Short_Other','Change_in_Open_Interest_All','Change_in_NonComm_Long_All','Change_in_NonComm_Short_All','Change_in_NonComm_Spead_All','Change_in_Comm_Long_All','Change_in_Comm_Short_All','Change_in_Tot_Rept_Long_All','Change_in_Tot_Rept_Short_All','Change_in_NonRept_Long_All','Change_in_NonRept_Short_All','Pct_of_Open_Interest_All','Pct_of_OI_NonComm_Long_All','Pct_of_OI_NonComm_Short_All','Pct_of_OI_NonComm_Spread_All','Pct_of_OI_Comm_Long_All','Pct_of_OI_Comm_Short_All','Pct_of_OI_Tot_Rept_Long_All','Pct_of_OI_Tot_Rept_Short_All','Pct_of_OI_NonRept_Long_All','Pct_of_OI_NonRept_Short_All','Pct_of_Open_Interest_Old','Pct_of_OI_NonComm_Long_Old','Pct_of_OI_NonComm_Short_Old','Pct_of_OI_NonComm_Spread_Old','Pct_of_OI_Comm_Long_Old','Pct_of_OI_Comm_Short_Old','Pct_of_OI_Tot_Rept_Long_Old','Pct_of_OI_Tot_Rept_Short_Old','Pct_of_OI_NonRept_Long_Old','Pct_of_OI_NonRept_Short_Old','Pct_of_Open_Interest_Other','Pct_of_OI_NonComm_Long_Other','Pct_of_OI_NonComm_Short_Other','Pct_of_OI_NonComm_Spread_Other','Pct_of_OI_Comm_Long_Other','Pct_of_OI_Comm_Short_Other','Pct_of_OI_Tot_Rept_Long_Other','Pct_of_OI_Tot_Rept_Short_Other','Pct_of_OI_NonRept_Long_Other','Pct_of_OI_NonRept_Short_Other','Traders_Tot_All','Traders_NonComm_Long_All','Traders_NonComm_Short_All','Traders_NonComm_Spread_All','Traders_Comm_Long_All','Traders_Comm_Short_All','Traders_Tot_Rept_Long_All','Traders_Tot_Rept_Short_All','Traders_Tot_Old','Traders_NonComm_Long_Old','Traders_NonComm_Short_Old','Traders_NonComm_Spead_Old','Traders_Comm_Long_Old','Traders_Comm_Short_Old','Traders_Tot_Rept_Long_Old','Traders_Tot_Rept_Short_Old','Traders_Tot_Other','Traders_NonComm_Long_Other','Traders_NonComm_Short_Other','Traders_NonComm_Spread_Other','Traders_Comm_Long_Other','Traders_Comm_Short_Other','Traders_Tot_Rept_Long_Other','Traders_Tot_Rept_Short_Other','Conc_Gross_LE_4_TDR_Long_All','Conc_Gross_LE_4_TDR_Short_All','Conc_Gross_LE_8_TDR_Long_All','Conc_Gross_LE_8_TDR_Short_All','Conc_Net_LE_4_TDR_Long_All','Conc_Net_LE_4_TDR_Short_All','Conc_Net_LE_8_TDR_Long_All','Conc_Net_LE_8_TDR_Short_All','Conc_Gross_LE_4_TDR_Long_Old','Conc_Gross_LE_4_TDR_Short_Old','Conc_Gross_LE_8_TDR_Long_Old','Conc_Gross_LE_8_TDR_Short_Old','Conc_Net_LE_4_TDR_Long_Old','Conc_Net_LE_4_TDR_Short_Old','Conc_Net_LE_8_TDR_Long_Old','Conc_Net_LE_8_TDR_Short_Old','Conc_Gross_LE_4_TDR_Long_Other','Conc_Gross_LE_4_TDR_Short_Other','Conc_Gross_LE_8_TDR_Long_Other','Conc_Gross_LE_8_TDR_Short_Other','Conc_Net_LE_4_TDR_Long_Other','Conc_Net_LE_4_TDR_Short_Other','Conc_Net_LE_8_TDR_Long_Other','Conc_Net_LE_8_TDR_Short_Other','Contract_Units']
        data.to_csv(dest_csv, encoding='utf-8', index=False,sep='\t')
        print(source_xls+' convert to '+dest_csv)

    for xi in XLS_arr:
        source_csv=source_csv_folder+xi+'.csv'
        with open(source_csv) as f:
            content = f.read()
        f.close
        content=content.replace('"','')
        with open(source_csv,'w',encoding='utf-8') as df:
            df.write(content)
        df.close

def step3():
    """ description """
    source_csv_folder='SOURCE_CSV/'
    temp_csv_folder='TEMP_CSV/'
    if not os.path.exists(temp_csv_folder):
        os.makedirs(temp_csv_folder)
    XLS_arr=['FUT86_06','FUT07_14','FUT15_16','FUT17','FUT18','dea_fut_xls_2019','dea_fut_xls_2020','dea_fut_xls_2021']
    want_arr=[]
    for ti in arr_as.want_arr:
        if ti[0] not in want_arr:
            want_arr.append(ti[0])
    for ci in XLS_arr:
        source_csv=source_csv_folder+ci+'.csv'
        dest_csv=temp_csv_folder+ci+'.csv'
        with open(dest_csv,'w',encoding='utf-8') as df:
            df.write('Market_and_Exchange_Names,Report_Date,Open_Interest_All,NonComm_Positions_Long_All,NonComm_Positions_Short_All\n')
        df.close
        with open(source_csv) as f:
            content = f.read()
        f.close
        lines=content.split('\n')
        with open(dest_csv,'a',encoding='utf-8') as df:
            for li in range(len(lines)):
                if lines[li]=='' or li<1:
                    pass
                else:
                    tmp_arr=lines[li].split('\t')
                    if tmp_arr[0] in want_arr:
                        df.write(get_short_name(tmp_arr[0])+','+clean_outdatetime(tmp_arr[2])+','+tmp_arr[7]+','+tmp_arr[8]+','+tmp_arr[9]+'\n')

def step4():
    """ description """
    XLS_arr=['FUT86_06','FUT07_14','FUT15_16','FUT17','FUT18','dea_fut_xls_2019','dea_fut_xls_2020','dea_fut_xls_2021']
    dest_csv='TEMP_CSV/FUT_ALL.csv'
    with open(dest_csv,'w',encoding='utf-8') as df:
        df.write('Market_and_Exchange_Names,Report_Date,Open_Interest_All,NonComm_Positions_Long_All,NonComm_Positions_Short_All\n')
    df.close

    for xlsi in XLS_arr:
        filename='TEMP_CSV/'+xlsi+'.csv'
        with open(filename) as f:
            content = f.read()
        f.close
        lines=content.split('\n')
        with open(dest_csv,'a',encoding='utf-8') as df:
            for li in range(len(lines)):
                if lines[li]=='' or li<1:
                    pass
                else:
                    df.write(lines[li]+'\n')
    print(dest_csv+' 合併CSV_ALL完成!')

    #讀入dist_csv到pandas作排序
    df = pd.read_csv(dest_csv)
    result = df.sort_values(['Market_and_Exchange_Names','Report_Date'], ascending=[1, 1])
    print(result)
    result.to_csv(dest_csv,index=False, encoding='utf-8')

def step5():
    """ output final csv files """
    folder = 'FINAL_CSV/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    want_arr=[]
    for ti in arr_as.want_arr:
        if ti[2] not in want_arr:
            want_arr.append(ti[2])
    #print(want_arr)
    file_path="TEMP_CSV/FUT_ALL.csv"
    df = pd.read_csv(file_path)
    #print(df)
    numpy_matrix = df.values
    #print(numpy_matrix)
    tmplen=len(numpy_matrix)
    for m in want_arr:
        txt_name=m
        #print(txt_name)
        with open('FINAL_CSV/'+str(txt_name)+'.csv', 'w') as f:
            f.writelines('Report_Date,Open_Interest_All,NonComm_Positions_Long_All,NonComm_Positions_Short_All\n')
            for i in range(0,tmplen):
                if(numpy_matrix[i][0]==txt_name):
                    f.writelines(str(numpy_matrix[i][1])+','+str(numpy_matrix[i][2])+','+str(numpy_matrix[i][3])+','+str(numpy_matrix[i][4])+'\n')
            f.close
    print("[OK] output final csvs files completed!")

def step6():
    """ description """
    # path to folder which needs to be zipped 
    directory = 'FINAL_CSV'

    # calling function to get all file paths in the directory 
    file_paths = get_all_file_paths(directory) 

    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file_name in file_paths: 
        print(file_name) 

    # writing files to a zipfile 
    with ZipFile('USCF.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths:
            zip.write(file,basename(file)) 
    zip.close
    print('[ USCF.zip ] All files zipped successfully!')         


if __name__=='__main__':
    #下載zip並解壓縮為xls
    step1()
    step2()
    step3()
    step4()
    step5()
    step6()

