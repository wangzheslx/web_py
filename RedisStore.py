#-*- coding:utf-8 -*-

from web.session import Store
import json


class RedisStore(Store):
    def __init__(self, grds, timeout):
        self.redis = grds
        self.timeout = timeout
    # 编码 将字典对象转换为json格式字符串
    def encode(self, session_dict):
        return json.dumps(session_dict)
    # 解码 将json格式字符串转换为字典对象
    def decode(self, session_data):
        return json.loads(session_data)
    #用于检查给定的会话 ID 是否存在于数据库中。
    def __contains__(self, key):
        return self.redis.exists(key)
    # 用于获取给定对话id的对应会话数据
    def __getitem__(self, key):
        value = self.redis.get(key)
        if value:
            self.redis.expire(key, self.timeout)
            return self.decode(value)
        else:
            raise KeyError(key)
    # 将键值对设置到 Redis 中    
    def __setitem__(self, key, value):
        self.redis.setex(key, self.timeout, self.encode(value))

    #  删除 Redis 中指定的键值对
    def __delitem__(self, key):
        self.redis.delete(key)
    # Redis自身支持过期时间，因此这里不需要实现清理逻辑
    def cleanup(self, timeout):
        pass

