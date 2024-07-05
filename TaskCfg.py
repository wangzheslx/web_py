#-*- coding: utf-8 -*-

import Config
import ActionCfg
#################################
KEY_TASK = "KEY_TASK_{userid}_{date}"
#################################
ID_INVALID = -1
ID_SIGN = 20001
ID_SIGN_SEVENDAYS = 20002
ID_SIGN_SERIES_1 = 20003
ID_SIGN_SERIES_2 = 20004
ID_SIGN_SERIES_3 = 20005

TYPE_DAY = 1
TYPE_WEEK = 2
TYPE_MONTH = 3
TYPE_YEAR = 4

# 任务列表
TASK_LIST = [
    ID_SIGN,
    ID_SIGN_SEVENDAYS,
    ID_SIGN_SERIES_1,
    ID_SIGN_SERIES_2,
    ID_SIGN_SERIES_3,
]

# 任务状态字段

STATE_INVALID    = -1
STATE_NOT_FINISH =  1
STATE_FINISHED   =  2
STATE_AWARDED    =  3 

# 签到类型
SIGN_TYPE_TODAY = 1
SIGN_TYPE_AGO = 2

# 签到用户键位名称

KEY_SIGN = "KEY_SIGN_{userid}_{date}"

###########################################################
TASK_CFG = {
    ID_SIGN:{
        'tid': ID_SIGN,
        'type': TYPE_DAY,
        'iconid': 20001,
        'series': ID_INVALID,# 前置任务解锁条件
        'action':ActionCfg.ACTION_SIGN,
        'name':"每日签到",
        'desc':"每日签到后领取奖励",
        'total': 1,
        'version': 10000,
        'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}], 
    },
    ID_SIGN_SEVENDAYS:{
        'tid': ID_SIGN_SEVENDAYS,
        'type': TYPE_WEEK,
        'iconid': 20002,
        'series': ID_INVALID,# 前置任务解锁条件
        'action':ActionCfg.ACTION_SIGN,
        'name':"签到七天",
        'desc':"连续签到七天后领取奖励",
        'total': 7,
        'version': 10000,
        'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}], 
    },
    ID_SIGN_SERIES_1:{
        'tid': ID_SIGN_SERIES_1,
        'type': TYPE_DAY,
        'iconid': 20003,
        'series': ID_INVALID,# 前置任务解锁条件
        'action':ActionCfg.ACTION_PLAY,
        'name':"每日对局5场",
        'desc':"每日对局5场后领取奖励",
        'total': 5,
        'version': 10000,
        'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}], 
    },
    ID_SIGN_SERIES_2:{
        'tid': ID_SIGN_SERIES_2,
        'type': TYPE_DAY,
        'iconid': 20004,
        'series': ID_SIGN_SERIES_1,# 前置任务解锁条件
        'action':ActionCfg.ACTION_PLAY,
        'name':"每日对局10场",
        'desc':"每日对局10场后领取奖励",
        'total': 10,
        'version': 10000,
        'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}], 
    },
    ID_SIGN_SERIES_3:{
        'tid': ID_SIGN_SERIES_3,
        'type': TYPE_DAY,
        'iconid': 20005,
        'series': ID_SIGN_SERIES_2,# 前置任务解锁条件
        'action':ActionCfg.ACTION_PLAY,
        'name':"每日对局20场",
        'desc':"每日对局20场后领取奖励",
        'total': 20,
        'version': 10000,
        'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}], 
    },
     
    
    
}