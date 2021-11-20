import redis   # 导入redis数据库模块, 安装 pip install redis


# 创建redis数据库的连接对象
db = redis.Redis(host='127.0.0.1',  # 指定操作redis数据库所在的地址 , 127.0.0.1 表示本地计算机的地址
            port=6379,  # redis数据库运行的端口, 默认是6379
            db=0,  # 指定操作的数据库, redis默认有16个
            decode_responses=True  # redis数据库默认是存储二进制数据, True 是解码存储的形式存储数据
            )

print(db)

redis_sets = [{'188.45.56.123:6523': 1}, {'16.36.56.369:6523': 2}, {'69.45.56.123:6523': 3},
              {'145.36.56.369:6523': 4}, {'256.45.56.123:6523': 5}, {'192.36.56.369:6523': 6}]

"""zadd 添加有序集合"""
for sets in redis_sets:
    # zadd  插入一个有序集合
    # proxies  有序集合的名字
    # sets  集合(redis数据库的概念)
    db.zadd('proxies', sets)

"""zrangebyscore  指定有序集合的分数获取代理"""
result = db.zrangebyscore('proxies', 1, 3)
print(result)


"""zscore 查询数据在集合中的序列号"""
# 查询到了就返回数据的序列号
# 没有查询到就返回 None
score = db.zscore('proxies', '145.36.56.369:6523')
print(score)


"""zincrby  修改集合序列的值"""  # 代理的分数
# -1  操作序列(可正可负)
# 指定集合的元素
db.zincrby('proxies', -1, '145.36.56.369:6523')
score = db.zscore('proxies', '145.36.56.369:6523')
print('修改后的序列号: ', score)
"""zrem 刪除集合序列的值""" 
db.zrem('proxies','145.36.56.369:6523')

"""zcard 获取有序集合的数量"""
count = db.zcard('proxies')
print(count)



