#-*- coding: utf-8 -*-
import Config

def InsertRegisterUser(phonenum, password, nick, sex, idcard, now):
    Config.gdb.insert(
        "user_data",
        userid = int(phonenum),
        password = password,
        secpassword = Config.DEFAULT_SECPASSWORD,
        nick = nick,
        phonenum = phonenum,
        sex = sex,
        idcard = idcard,
        status = Config.USER_STATUS_NOLMAL,
        createtime = now,
        lastlogintime = now,
    )


def InitPackage(packageinfo):
    Config.gdb.insert(
        "package",
        **packageinfo
    )


def UpdateMoney(userid, money, now):
    Config.gdb.update(
        'package',
        where = "userid = $userid",
        vars = dict(userid = userid),
        money = money,
        freshtime = str(now),    
    )