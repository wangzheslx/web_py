#-*- coding:utf-8 -*-
import web
DB_HOST = '192.168.3.36'
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

DEFAULT_SECPASSWORD = '123456'

USER_STATUS_NOLMAL = 0
USER_STATUS_FREEZE = 1



