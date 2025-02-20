# encoding:utf-8
import random

import fofa
import requests
import multiprocessing
from tqdm import tqdm
from gooey import Gooey, GooeyParser

requests.packages.urllib3.disable_warnings()

RED = '\033[91m'
RESET = '\033[0m'


# ip+端口组合的列表去重
def ip_quchong(ip_port_list):
    # 使用集合来去重
    unique_ip_port_list = set(ip_port_list)
    # 将集合转换回列表
    return list(unique_ip_port_list)


# 请求头获取函数
def get_request_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
]
    other_headers = {
        "Content-Type: ":"application/x-www-form-urlencoded",
        "Content-Type: ": "application/json",
        "Content-Type: ": "multipart/form-data",
    }

    return random.choice(user_agents)

# GET请求漏洞POC
def get_req(url,ua,match1):
    try:
        # 发送 GET 请求
        response = requests.get(url, headers=ua,verify=False)

        if response.status_code == 200 and match1 in response.text:
            print("响应状态码为200，内容为%s" % response.text)
            print(f"{RED}URL[{url} 存在漏洞{RESET}")
            # result.append(url)
            return url
        else:
            print(f"URL[{url}]漏洞并不存在，响应状态码:{response.status_code}")

    except requests.RequestException as e:
        print(f"URL[{url}] 请求失败：{e}")


# POST请求漏洞POC
def post_req(url,ua,data,match2):
    # 发送POST请求
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=ua,data=data,verify=False)

        if response.status_code == 200 and match2 in response.text:
            print("响应状态码为200，内容为%s" % response.text)
            print(f"{RED}URL[{url} 存在漏洞{RESET}")
            # result.append(url)
            return url
        else:
            print(f"URL[{url}]漏洞并不存在，响应状态码:{response.status_code}")

    except requests.RequestException as e:
        print(f"URL[{url}] 请求失败：{e}")


# 自动生成POC
# 最终目的：*******
def create_vul_poc():
    pass



@Gooey(program_name="漏洞批量复测工具V1.0",
       default_size=(800,700), # 设置默认窗口大小
       image_dir="xxx",  # 图标文件所在目录,命名为config_icon.png
       navigation="TABBED", # 创建选项卡式界面，分页显示
       header_bg_color='#3264a8',
       terminal_font_family='Consolas',# 设置字体
       # theme='dark',  # 暗色主题
       # styling={'terminal_font_color':'#FF0000',   # 文本颜色
       #          'terminal_panel_color':'#000000'}, # 背景颜色
       language='chinese',  # 设置界面语言

       # 设置窗口位置
       window_position=(50, 100), # (左侧位置, 顶部位置)
       window_size=(900, 800),     # (宽度, 高度)

       # 进度条配置
       progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
       progress_expr="current / total * 100"
       )
def main():
    #定义fofa等搜索引擎结果文件位置，后续将fofa结果自动化实现
    file_path = "D:xxx"

    # 设置fofa key
    key = 'xxxx'
    # 调用fofa sdk接口
    client = fofa.Client(key)
    # 设置查询条件
    # query_str = 'body="themes/tenant/css/login.css"'

    parser = GooeyParser(description="对单一漏洞从空间搜索引擎获取结果并批量验证的工具")
    parser.add_argument('query_str',type=str,help='查询条件')
    parser.add_argument('size', type=int, help='每页查询数量',default=100)
    parser.add_argument('page', type=int, help='翻页数',default=1)

    parser.add_argument('extend_uri1', type=str, help='漏洞uri')
    parser.add_argument('match1', type=str, help='漏洞匹配字段')

    # store_true 表示如果在命令行中提供了该参数，则将其值设置为 True；如果没有提供，则设置为 False
    # 在参数名称前加 -- 表示该参数为非必选参数
    parser.add_argument('--req_method', help='选择请求方法,默认GET，勾选则为POST',action='store_true',widget='CheckBox')
    parser.add_argument('--req_content_type', type=str, help='请求数据格式')
    # 单行用TextField，多行用Textarea
    parser.add_argument('--post_data',help='输入请求体',widget='Textarea',required=False,
                        gooey_options={
                            'height': 300,  # 设置文本框高度
                            'placeholder': "请输入您的文本内容..."
                        }
                        )



    #获取添加的参数
    args = parser.parse_args()

    print(f"漏洞批量复测GUI程序开始，查询参数为：{args.query_str}")
    print(f"佛法无边，回头是岸！！！")
    print(f"-----------------------------------------------------------------------")
    # 返回数据获取，默认为3项：host,ip,port
    # 其他项字段还有 *******
    data = client.search(args.query_str, args.page, args.size, fields="ip,port,city")
    # print(data)

    post_data = args.post_data

    final_result = []
    for ip, port,city in data["results"]:
        # print("%s:%s" % (ip, port))
        req_url = "http://" + ip + ":" + port + args.extend_uri1
        headers = {"User-Agent":get_request_headers(),"Content-Type":"args.req_content_type"}
        if args.req_method == 0:
            # 不勾选请求方法选项，则使用GET请求方法
            match_url = get_req(req_url,headers,args.match1)
            # print(match_url)
            final_result.append(match_url)
        else:
            match_url = post_req(req_url,headers,post_data,args.match1)
            final_result.append(match_url)

    # 打印结果
    print(final_result)


if __name__ == "__main__":
    main()
