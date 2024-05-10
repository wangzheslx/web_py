#-*- coding:utf-8 -*-
import web
import redis
# Mysql配置
DB_HOST = '192.168.3.103'
DB_PORT = 3306
DB_USER = 'root'
DB_PW = '123456'
DB_NAME = 'webdatas'


gdb = web.database(
    dbn='mysql',
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    pw=DB_PW,
    db=DB_NAME
)

# 用户初始密码
DEFAULT_SECPASSWORD = '123456'
# 用户背包初始或货币
NEWUSER_DEFAULT_MONEY = 10000
# 用户状态
USER_STATUS_NOLMAL = 0
USER_STATUS_FREEZE = 1

# Redis

RDS_HOST = '127.0.0.1'
RDS_PORT = 6379
RDS_PW = '123456'
# 设置session过期时间
SESSION_EXPIRETIME = 30
LOGIN_INVALID_TIME = 30

grds = redis.Redis(
    host = RDS_HOST,
    port = RDS_PORT,
    password = RDS_PW,
)

#  测试redis
# grds.set('name', 'zhangsan')

# 账号背包命名
KEY_PACKAGE = "KEY_PACKAGE_{userid}"
# 登录session
KEY_LOGIN = "KEY_LOGIN_{userid}"

