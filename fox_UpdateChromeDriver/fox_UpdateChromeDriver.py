import requests,re,configparser,zipfile,os,shutil

# 檢測 Chrome 瀏覽器版本
def get_chrome_version():
    stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
    output = stream.read()
    version_index = output.find('DisplayVersion')
    version_start = version_index + len('DisplayVersion    REG_SZ')
    version_end = output.find('\\n', version_start)
    version = output[version_start:version_end].strip()
    return version.strip()

def ini_to_dict(ini_loc):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(ini_loc,encoding='utf-8')
    sections=config.sections()
    tmp_dict={}
    for i in sections:
        options=config.options(i)
        for j in options:
            tmp_dict[i+'.'+j]=config[i][j]
    return tmp_dict

if __name__=='__main__':
    base_dir = os.getcwd()
    config=ini_to_dict(f"{base_dir}\\setting.ini")
    ver=get_chrome_version().split('\n')[0]
    print(f"Chrome客戶端版本號:{ver}")
    url="https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    r=requests.get(url)
    r.encode='utf-8'
    #print(r.text)
    #ver="125.0.6422.141"
    ver=ver.split('.')[0]
    aa=re.findall(f"https://storage.googleapis.com/chrome-for-testing-public/{ver}[^/]*/win64/chromedriver-win64.zip",r.text)
    url=(aa[-1])
    # 下載地址
    #url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.141/win64/chromedriver-win64.zip'
    print(f"下載 chromedriver.zip : {url}")
    # 下載文件並保存到本地
    local_zip_path = 'chromedriver.zip'
    response = requests.get(url)
    with open(local_zip_path, 'wb') as file:
        file.write(response.content)
    print(f"解壓縮 chromedriver.zip 到 : chromedriver_folder")
    # 解壓縮文件
    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall('chromedriver_folder')
    print(f"複制 chromedriver.exe 到 : {config['SETTING.chromedriver_loc']}")
    # 複制文件到指定路徑
    shutil.copy('chromedriver_folder\\chromedriver-win64\\chromedriver.exe', config['SETTING.chromedriver_loc'])
    print("清理下載和解壓縮後的文件...")
    # 清理下載和解壓縮後的文件
    os.remove(local_zip_path)
    shutil.rmtree('chromedriver_folder')
    print('Chromedriver 更新完成！')