"""
    检测模块

    从数据库中取出所有代理, 然后挨个检测

"""
import requests
from db import RedisClient
import concurrent.futures
from config import TEST_URL


# 实例化redis数据库模块对象
client = RedisClient()


# TEST_URL = 'https://www.baidu.com'  # 测试网址
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}


def verify_proxy(proxy):
    """
    检测代理是否可用的函数
    """
    proxies = {
        "http": "http://" + proxy,
        "https": "https://" + proxy,
    }

    try:
        response = requests.get(url=TEST_URL, proxies=proxies, timeout=2)
        if response.status_code in [200, 206, 302]:  # 判断请求返回的状态码是不是成功的状态码 500
            # 如果请求成功, 表示代理可用, 将此代理设置为100分, 调用数据库模块的 max() 方法
            client.max(proxy)
            print('*******代理可用******', proxy)

        else:
            # 如果请求不成功, 表示代理不可用, 将此代理执行降分操作, 调用数据库模块的 decrease() 方法
            client.decrease(proxy)
            print('--请求的状态码不合法--', proxy)
    except:
        # 请求超时也表示代理不可用, 将此代理执行降分操作, 调用数据库模块的 decrease() 方法
        client.decrease(proxy)
        print('=====请求超时=====', proxy)


# 检测速度太慢了? 多任务: 多进程<消耗系统资源太多>, 多线程
def verify_thread_pool():
    """线程池测试代理"""
    # 1. 首先从数据库中取到所有的代理
    proxies_list = client.all()  # --列表
    # 2. 线程池检测代理
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for proxy in proxies_list:
            executor.submit(verify_proxy, proxy)



if __name__ == '__main__':
    # proxy = ['1.196.177.160:9999', '1.196.177.180:9999', '1.196.177.254:9999',
    #          '1.197.203.189:9999','1.198.73.252:9999', '1.199.31.33:9999']
    #
    # for pro in proxy:
    #     verify_proxy(pro)

    verify_thread_pool()


