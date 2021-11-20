"""
    调度模块
"""

# 调度模块的类
import time
import multiprocessing
from db import RedisClient
from getter import proxy_func_list
from verify import verify_thread_pool
from api import app
from config import GETTER_PROXY, VERIFY_PROXY

client = RedisClient()

class Schedule:
    # 1. 调度获取代理模块
    def getter_proxy(self):
        while True:
            for func in proxy_func_list:
                proxies = func()
                for proxy in proxies:
                    print('--代理写入数据库--', proxy)
                    client.add(proxy)
            time.sleep(GETTER_PROXY)  # 每五分钟爬取一次代理进行入库

    # 2. 调度验证代理模块
    def verify_proxy(self):
        while True:
            verify_thread_pool()
            time.sleep(VERIFY_PROXY)

    # 3. 调度api服务模块
    def api_server(self):
        app.run()

    def run(self):
        # 调度这三个函数一起去执行, 每一个函数都当做独立的个体
        getter_proxy = multiprocessing.Process(target=self.getter_proxy)
        getter_proxy.start()

        # 数据库没有代理
        if client.count() > 0:
            verify_proxy = multiprocessing.Process(target=self.verify_proxy)
            verify_proxy.start()

        api_server = multiprocessing.Process(target=self.api_server)
        api_server.start()


if __name__ == '__main__':
    work = Schedule()
    work.run()




