#-*- coding:utf-8 -*-
import Config

def GetMoney(userid):
    strkey = Config.KEY_PACKAGE.format(userid=userid)
    money = 0
    if Config.grds.exists(strkey):
        money = Config.grds.hget(strkey, 'money')
    else:
        result = Config.gdb.select('package', what = "*", where="userid=$userid", vars=dict(userid=userid))
        packageinfo = dict(result[0])
        # {
        #     'money':result[0]['money'],
        #     'coin':result[0]['coin'],
        #     'prop_1001':result[0]['prop_1001'],
        #     'prop_1002':result[0]['prop_1002'],
        #     'prop_1003':result[0]['prop_1003'],
        #     'prop_1006':result[0]['prop_1006'],
        #     'prop_1007':result[0]['prop_1007'],
        #     'freshtime':result[0]['freshtime'],# 背包当前时间      
        # }
        Config.grds.hmset(strkey, packageinfo)
        Config.grds.expire(strkey, 30 * 24 * 60 * 60)
        money = int(packageinfo['money'])
    return money
