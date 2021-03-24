import os,json

# 列出dir_loc目錄所有檔案，可用allow_file_type指定檔案副檔名類型
def dir_list(dir_loc,allow_file_type=[]):
    tmp_list=[]
    #print('allow_file_type length:'+len(allow_file_type))
    for path, subdirs, files in os.walk(dir_loc):
        for name in files:
            is_match=False
            if len(allow_file_type)>0: 
                if get_file_type(name) in allow_file_type:
                    is_match=True
            else:
                is_match=True
            if is_match==True:
                tmp_list.append(os.path.join(path, name))
    return tmp_list

# 取得副檔名格式
def get_file_type(file_path_and_name):
    return file_path_and_name.split(".")[-1]

def merge_all_txt(out_file_loc,txt_list):
    with open(out_file_loc, 'w+', encoding='utf-8') as outfile:
        for fname in txt_list:
            with open(fname,'r',encoding='utf-8') as infile:
                for line in infile:
                    if "\n" in line:
                        outfile.write(line)
                    else:
                        outfile.writelines(line+"\n")
    print(out_file_loc,'merge done!')

def get_file_name(file_path_and_name):
    return file_path_and_name.split("\\")[-1]

def list_to_txt(in_list,out_txt_loc):
    with open(out_txt_loc,'w+',encoding='utf-8') as outfile:
        for i in in_list:
            if "\n" in i:
                outfile.write(get_file_name(i))
            else:
                outfile.writelines(get_file_name(i)+"\n")

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #read ini file
    f = open('setting.json',)
    data = json.load(f)
    txts_path=data["source_txt_folder"]
    out_txt=".\\"+data["out_filename"]
    txt_path=dir_path+'\\'+txts_path+'\\'
    txt_list=dir_list(txt_path,["txt"])
    txt_list.sort()
    list_to_txt(txt_list,dir_path+"\\txts_list.txt")
    merge_all_txt(out_txt,txt_list)