#-*- coding: utf-8 -*-
# 当前版本号
SHOP_VERSION = 10000

#使用方法
TYPE_USE = 1
TYPE_TIME  = 2
#购买方法
TYPE_PAY_MONEY = 1
TYPE_PAY_COIN = 2
# 限购类型
BYLIMITTYPE_INVALID = 0
BYLIMITTYPE_DAY = 1
BYLIMITTYPE_WEEK = 2
BYLIMITTYPE_MONTH = 3
BYLIMITTYPE_YEAR = 3
# 内容
ID_EXPCARD = 1001
ID_RENAMECARD = 1002
ID_GAMECLEARCARD = 1003
ID_YEARVIP_PACKAGE = 1004
ID_MONTHVIP_PACKAGE = 1005
ID_YEARVIP = 1006
ID_MONTHVIP = 1007
# 商品列表
SHOP_LIST = [
    ID_EXPCARD,
    ID_RENAMECARD,
    ID_GAMECLEARCARD,
    ID_YEARVIP_PACKAGE,
    ID_MONTHVIP_PACKAGE,  
]

SHOP_CFG = {
    ID_EXPCARD:{"pid":ID_EXPCARD,
            "name":"经验卡",
            "type":TYPE_USE,
            "money":100,
            "coin": -1,
            "paytype":TYPE_PAY_MONEY,
            "iconid":1001,
            "version":10000,
            "discount":1,
            "inventory":-1,
            "buylimittype":BYLIMITTYPE_INVALID,
            "buylimitnum":-1,
            "proplist":[{"id":ID_EXPCARD,"num":1},],
            },
    ID_RENAMECARD:{"pid":ID_RENAMECARD,
            "name":"改名卡",
            "type":TYPE_USE,
            "money":100,
            "coin": -1,
            "paytype":TYPE_PAY_MONEY,
            "iconid":1002,
            "version":10000,
            "discount":1,
            "inventory":-1,
            "buylimittype":BYLIMITTYPE_INVALID,
            "buylimitnum":-1,
            "proplist":[{"id":ID_RENAMECARD,"num":1},],
            }, 
    ID_GAMECLEARCARD:{"pid":ID_GAMECLEARCARD,
            "name":"战绩清零卡",
            "type":TYPE_USE,
            "money":100,
            "coin": -1,
            "paytype":TYPE_PAY_MONEY,
            "iconid":1003,
            "version":10000,
            "discount":1,
            "inventory":-1,
            "buylimittype":BYLIMITTYPE_INVALID,
            "buylimitnum":-1,
            "proplist":[{"id":ID_GAMECLEARCARD,"num":1},],
            } ,  
    ID_YEARVIP_PACKAGE:{"pid":ID_YEARVIP_PACKAGE,
            "name":"经验卡",
            "type":TYPE_USE,
            "money":-1,
            "coin": 100,
            "paytype":TYPE_PAY_COIN,
            "iconid":1004,
            "version":10000,
            "discount":1,
            "inventory":-1,
            "buylimittype":BYLIMITTYPE_INVALID,
            "buylimitnum":-1,
            "proplist":[{"id":ID_EXPCARD,"num":1},{"id":ID_RENAMECARD,"num":1},{"id":ID_MONTHVIP,"num":1},],
            } ,
    ID_MONTHVIP_PACKAGE:{"pid":ID_MONTHVIP_PACKAGE,
            "name":"经验卡",
            "type":TYPE_USE,
            "money":-1,
            "coin":1000,
            "paytype":TYPE_PAY_COIN,
            "iconid":1005,
            "version":10000,
            "discount":1,
            "inventory":-1,
            "buylimittype":BYLIMITTYPE_INVALID,
            "buylimitnum":-1,
            "proplist":[{"id":ID_EXPCARD,"num":10},{"id":ID_RENAMECARD,"num":10},{"id":ID_YEARVIP,"num":1},],
            } , 
}