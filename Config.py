#-*- coding:utf-8 -*-
import web
import redis
# Mysql配置
DB_HOST = '192.168.12.248'
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
SESSION_EXPIRETIME = 30*4
LOGIN_INVALID_TIME = 30*4

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

# 货币代码

MONEY_ID = 800
COIN_ID = 900

# 用户邮件列表
KEY_MAIL_LIST = "KEY_MAIL_LIST_{userid}"
# 邮件详细信息列表
KEY_MAIL_DETAIL = "KEY_MAIL_DETAIL_{mailid}"

#邮件服务器的IP和端口
MAIL_HOST = "127.0.0.1"
MAIL_PORT = 1234
