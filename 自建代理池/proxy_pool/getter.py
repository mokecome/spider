"""
    获取免费代理的模块
"""
import time

import requests
import re
from db import RedisClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
proxy_pattern = re.compile('.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,5}).*?', re.S)


def spider_yun_proxy():
    """
    爬取云代理的ip
    目标网址: http://www.ip3366.net/
    """

    for page in range(1, 11):
        time.sleep(1)
        print('云代理:', f'http://www.ip3366.net/?stype=1&page={page}')
        html_data = requests.get(f'http://www.ip3366.net/?stype=1&page={page}', headers=headers).text
        ip_port = re.findall(proxy_pattern, html_data)
        # print(ip_port)

        for ip, port in ip_port:
            yield ip + ':' + port


def spider_89_proxies():
    """
    爬取89代理ip
    目标网址: https://www.89ip.cn/
    """
    for page in range(1, 11):
        time.sleep(1)
        print('89代理', f'https://www.89ip.cn/index_{page}.html')
        html_data = requests.get(url=f'https://www.89ip.cn/index_{page}.html', headers=headers).text
        ip_port = re.findall(proxy_pattern, html_data)
        # print(ip_port)
        for ip, port in ip_port:
            # 返回一个生成器对象,可以用for循环取值
            yield ip + ":" + port


def spider_kuai_proxies():
    """
    爬取快代理ip
    目标网址：https://www.kuaidaili.com/free/
    """
    for page in range(1, 11):
        time.sleep(1)
        print('快代理', f'https://www.kuaidaili.com/free/inha/{page}/')
        response = requests.get(f'https://www.kuaidaili.com/free/inha/{page}/', headers=headers)
        ip_port = re.findall(proxy_pattern, response.text)
        # print(ip_port)
        for ip, port in ip_port:
            # 返回一个生成器对象(在for循环中一个一个返回数据)
            yield ip + ":" + port


proxy_func_list = [spider_yun_proxy, spider_89_proxies, spider_kuai_proxies]


if __name__ == '__main__':

    proxy_func_list = [spider_yun_proxy, spider_89_proxies, spider_kuai_proxies]

    for func in proxy_func_list:
        proxies = func()
        for proxy in proxies:
            print(proxy)

            client = RedisClient()
            client.add(proxy)




