import random

import fofa
import requests
import multiprocessing
from tqdm import tqdm
from gooey import Gooey, GooeyParser

requests.packages.urllib3.disable_warnings()

RED = '\033[91m'
RESET = '\033[0m'

def post_req(url,ua,data,match2):
    # 发送POST请求
    try:
        # 发送 POST 请求
        response = requests.get(url, headers=ua,data=data,verify=False)

        if response.status_code == 200 and match2 in response.text:
            print("响应状态码为200，内容为%s" % response.text)
            print(f"{RED}URL[{url} 存在漏洞{RESET}")
            # result.append(url)
            return url
        else:
            print(f"URL[{url}]漏洞并不存在，响应状态码:{response.status_code}")

    except requests.RequestException as e:
        print(f"URL[{url}] 请求失败：{e}")



@Gooey(default_size=(800,700), # 设置默认窗口大小
       header_bg_color='#3264a8',
       )
def main():
    parser = GooeyParser(description="多行字符串输入示例")
    parser.add_argument('--req_content_type', type=str, help='请求数据格式')
    parser.add_argument('--multiline_text',
                        metavar='输入内容',
                        widget='Textarea',
                        help='请输入多行文本',
                        gooey_options={
                            'height':300, #设置文本框高度
                            'placeholder':"请输入您的文本内容..."
                        })

    args = parser.parse_args()

    print(args.multiline_text.format(args.req_content_type))


    # url = 'http://www.baidu.com'
    # ua = 'Mozilla/5.0 (Windows NT 10'
    # headers = {"User-Agent": ua, }
    # headers["Content-Type"] = args.multiline_text
    # # print(headers)
    # response = requests.get(url,headers=headers,data=args.multiline_text,verify=False)
    # prepared = response.request.url
    # # 打印请求的内容
    # print("请求的 URL:", response.request.url)
    # print("请求的 方法:", response.request.method)
    # print("请求的 头部:", response.request.headers)
    # print("请求的 数据:", response.request.body)

if __name__ == '__main__':
    main()