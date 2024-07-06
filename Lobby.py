#-*- coding:utf-8 -*-
import Config
import datetime
from proto.general_pb2 import Mail
import ShopCfg
import json
import Service

def GetMoney(userid):
    strkey = Config.KEY_PACKAGE.format(userid=userid)
    money = 0
    if Config.grds.exists(strkey):
        # 接受键值要传hget 哈希方法
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

# 传datetime.date.today()
def GetMonday(today):
    today = datetime.datetime.strptime(str(today), "%Y-%m-%d")
    return datetime.datetime.strftime(today - datetime.timedelta(today.weekday()), "%Y_%m_%d")

# 传datetime.datetime.now()
# def GetMonday(today):
#     today = datetime.datetime.strptime(str(today), "%Y-%m-%d %H:%M:%S.%f")
#     monday = today - datetime.timedelta(days=today.weekday())
#     return datetime.datetime.strftime(monday, "%Y_%m_%d")

def SendMail(mailinfo):
    if not mailinfo:
        return
    mailproto = Mail()
    for userid in mailinfo['useridlist']:
        mailinfo.userid.append(userid)
    mailproto.title = mailinfo['title']
    mailproto.context = mailinfo['context']
    mailproto.type = mailinfo['type']
    attach = {}
    for propid, propnum in mailinfo['attach'].items():
        if propid in ShopCfg.SHOP_CFG:
            attach['propid'] = propnum
    mailproto.attach = json.dumps(attach)
    mailproto['getattach'] = 0
    mailproto['hasattach'] = 0
    if attach:
        mailproto['hasattach'] = 1
    
    # 之后 发给 邮件服务器#####################################################
    Service.SendSvrd('ip', 8080 ,mailproto.SerializeToString())
    #########################################################################

def GetGlobalMail(userid):
    pass


def GetMailList(userid):
    ## 获取全服邮件

    strKeyList = Config.KEY_MAIL_LIST.format(userid = userid)
    # 获取redis当中的mail的redis
    mailidlist = Config.grds.lrange(strKeyList, 0, -1)
    mailinfolist = []
    for mailid in mailidlist:
        strKey = Config.KEY_MAIL_DETAIL.format(mailid = mailid)
        result = Config.grds.hgetall(strKey)
        if not result:
            # 删除strkeylist对应过期的redis列表的当中的数据
            Config.grds.lrem(strKeyList, mailid, 0)
            continue
        mailinfo = {}
        mailinfo['mailid'] = mailid
        mailinfo['title'] = result['title']
        mailinfo['type'] = result['type']
        mailinfo['getattach'] = result['getattach']
        mailinfo['context'] = result['context']
        mailinfolist.append(mailinfo)
    return mailinfolist

def MailDelete(userid, mailid):
    strKeyList = Config.KEY_MAIL_LIST.format(userid = userid)
    Config.grds.lrem(strKeyList, mailid, 0)
    strKey = Config.KEY_MAIL_DETAIL.format(mailid = mailid)
    Config.grds.delete(strKey)

def MailDeleteALL(userid):
    strKeyList = Config.KEY_MAIL_LIST.format(userid = userid)
    mailidlist = Config.grds.lrange(strKeyList, 0 ,-1)
    for mailid in mailidlist:
        strKey = Config.KEY_MAIL_DETAIL.format(mailid = mailid)
        result = Config.grds.hgetall(strKey)
        if result['hasattach'] == 0 or result['getattach'] == 1:
            Config.grds.lrem(strKeyList, mailid, 0)
            Config.grds.delete(strKey)
    return {'code':0}
    
