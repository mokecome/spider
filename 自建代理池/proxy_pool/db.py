"""
    数据库模块, 提供了我们后续数据库操作的所有方法
"""
import random
import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DATABASE, REDIS_OBJECT
from config import INIT_SCORE, HIGH_SCORE, MINIMUM_SCORE, HIGHEST_SCORE, CHANGE_SCORE


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE):
        """初始化redis客户端"""
        self.db = redis.Redis(host=host,  port=port, db=db, decode_responses=True)

    def exists(self, proxy):
        """判断传入的代理有没有存储到数据库"""
        # 传进来的代理在数据库中有, 就返回True
        # 传进来的代理在数据库中没有, 就返回False
        return not self.db.zscore(REDIS_OBJECT, proxy) is None

    def add(self, proxy, score=INIT_SCORE):
        """添加代理到数据库, 设置初始分数为10分"""
        if not self.exists(proxy):  # 如果数据库中没有这个代理才满足 if 判断的逻辑
            return self.db.zadd(REDIS_OBJECT, {proxy: score})

    def random(self):
        """随机选择一个代理的方法"""
        # 1. 尝试获取评分为100分的代理
        proxies = self.db.zrangebyscore(REDIS_OBJECT, HIGH_SCORE, HIGH_SCORE)  # 返回列表
        if len(proxies):#有
            return random.choice(proxies)
        # 2. 获取指定评分范围的代理
        proxies = self.db.zrangebyscore(REDIS_OBJECT, MINIMUM_SCORE, HIGHEST_SCORE)  # 返回列表
        if len(proxies):
            return random.choice(proxies)
        # 3. 如果数据库没有代理, 就提示"数据库为空"
        print('########---数据库为空---#######')

    def decrease(self, proxy):
        """传入一个代理, 如果检测不过关就降低代理的分数"""
        self.db.zincrby(REDIS_OBJECT, CHANGE_SCORE, proxy)  # 一旦检测不过关就代理减一分
        score = self.db.zscore(REDIS_OBJECT, proxy)  # 查询分数
        if score <= 0:
            self.db.zrem(REDIS_OBJECT, proxy)  # 删除代理

    def max(self, proxy):
        """如果检测的代理可用, 那么久将代理设置最大分数"""
        return self.db.zadd(REDIS_OBJECT, {proxy: HIGH_SCORE})

    def count(self):
        """获取数据库中代理的数量"""
        return self.db.zcard(REDIS_OBJECT)

    def all(self):
        """获取所有代理, 返回列表"""
        proxies = self.db.zrangebyscore(REDIS_OBJECT, MINIMUM_SCORE, HIGH_SCORE)
        if proxies:
            return proxies
        else:
            print('########---数据库无代理---#######')

    def count_for_num(self, number):
        """指定数量获取代理, 返回列表"""
        all_proxies = self.all()
        proxies = random.sample(all_proxies, k=number)
        return proxies


if __name__ == '__main__':
    proxies = ['927.72.91.211:9999', '927.12.91.211:8888', '927.792.91.219:7777', '927.732.91.211:6666']

    client = RedisClient()
    # for proxy in proxies:
    #     client.add(proxy)

    # result = client.random()
    # print(result)

    count = client.count()
    print('当前数据库有代理数量: ', count)

    all = client.all()
    print('当前数据库所有代理: ', all)

    result = client.count_for_num(2)
    print(result)




