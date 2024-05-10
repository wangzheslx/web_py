#-*- coding: utf-8 -*-
import ShopCfg
import ErrorCfg
import datetime
import math
import Lobby
import Config
import DBManage



def GetShopCfg(version):
    shop = ShopCfg.SHOP_CFG
    shoplist = []# 预留返回的商品列表
    for id in shop:
        if id in ShopCfg.SHOP_CFG:
            cfg = ShopCfg.SHOP_CFG[id]
            if version < cfg['version']:
                # 版本小于商品上线版本
                continue
            propdict = {
                'pid':cfg['pid'],
                'name':cfg['name'],
                'type':cfg['type'],
                'money':cfg['money'],
                'coin':cfg['coin'],
                'paytype':cfg['paytype'],
                'iconid':cfg['iconid'],
                'version':cfg['version'],
                'discount':cfg['discount'],
                'inventory':cfg['inventory'],
                'buylimittype':cfg['buylimittype'],
                'buylimitnum':cfg['buylimitnum'],
                'proplist':cfg['proplist'],
            }
            # 添加物品
            shoplist.append(propdict)
    return {'shoplist': shoplist, 'shopversion': ShopCfg.SHOP_VERSION,}

# 实现商城购买功能
def ShopBuy(userid , propid , propnum, shopversion, version):
    if shopversion < ShopCfg.SHOP_VERSION:
        return {'code': ErrorCfg.EC_SHOP_VERSION_LOW,'reason': ErrorCfg.ER_SHOP_VERSION_LOW}
    #  查看购买商品， 校验版本号
    if propid not in ShopCfg.SHOP_LIST:
        return {'code': ErrorCfg.EC_SHOP_BUY_LIST_NOT_EXIST,'reason': ErrorCfg.ER_SHOP_BUY_LIST_NOT_EXIST}
    if propid not in ShopCfg.SHOP_CFG:
        return {'code': ErrorCfg.EC_SHOP_BUY_PROP_NOT_EXIST,'reason': ErrorCfg.ER_SHOP_BUY_PROP_NOT_EXIST}
    cfg = ShopCfg.SHOP_CFG[propid]
    if cfg['version'] > version:
        return{'code': ErrorCfg.EC_SHOP_BUY_CLIENT_VERSION_LOW,'reason': ErrorCfg.ER_SHOP_BUY_CLIENT_VERSION_LOW}
    # 计算购买数量和剩余数量
    # 后续应该是在缓存中取出这个商品的剩余数量
    #############################################
    if cfg['inventory'] != -1 and propnum > cfg['inventory']  :
        return{'code': ErrorCfg.EC_SHOP_BUY_INVENTORY_NOT_ENOUGH,'reason': ErrorCfg.ER_SHOP_BUY_INVENTORY_NOT_ENOUGH}
    ##############################################
    # 购买redis 保证购买的原子性
    needmoney = int(math.floor(cfg['money'] * cfg['discount']))

    # 获取金额
    
    money = Lobby.GetMoney(userid)
    
    if money < needmoney:
        return {'code' : ErrorCfg.EC_SHOP_BUY_MONEY_NOT_ENOUGH, 'reason' : ErrorCfg.ER_SHOP_BUY_MONEY_NOT_ENOUGH}
    now = datetime.datetime.now()
    strkey = Config.KEY_PACKAGE.format(userid=userid)

    # 原子性保证
    money = Config.grds.hincrby(strkey, 'money', -needmoney)
    if money < 0:
        Config.grds.hincrby(strkey, 'money', needmoney)
        return {'code' : ErrorCfg.EC_SHOP_BUY_MONEY_NOT_ENOUGH, 'reason' : ErrorCfg.ER_SHOP_BUY_MONEY_NOT_ENOUGH}
    now = datetime.datetime.now()
    DBManage.UpdateMoney(userid, money, now)
    return {"return money ":{money}}
    # 发货