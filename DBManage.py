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

def UpdateProp(userid, propdict, now):
    propstr = ""
    for k, v in propdict.items():
        # 注意末尾多了一个字符 ”  ，“
        propstr+=str(k)+"="+str(v)+","
    Config.gdb.query(
    "update package set {propstr} freshtime = '{now}' where userid = {userid}".format(propstr=propstr, now = now, userid = userid)  
    )
    