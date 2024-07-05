#-*- coding: utf-8 -*-
import TaskCfg
import Config
import datetime
import json
import Lobby
import ErrorCfg
import Shop
import Error
from proto.general_pb2 import *
import Action
import MessageCfg

def InitTaskCfg(userid, datestr):
    taskinfo = {}
    strkey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
    for id in TaskCfg.TASK_LIST:
        if id in TaskCfg.TASK_CFG:
            cfg = TaskCfg.TASK_CFG[id]
            taskinfo["count_"+str(id)] = 0
            taskinfo["total_"+ str(id)] = cfg["total"]
            taskinfo["state_"+str(id)] = TaskCfg.STATE_NOT_FINISH
            taskinfo["reward_"+ str(id)] = json.dumps(cfg["rewardlist"])
    # 以字典当中的键值对来设置哈希映射
    Config.grds.hset(strkey, mapping=taskinfo)

# 根据任务ID选择性初始化任务配置
def InitTaskCfgByField(userid, taskid, datestr):
    pass


def GetTaskDatestr(type, today):
    if type == TaskCfg.TYPE_DAY:
        datestr = today.strftime("%Y_%m_%d")
    elif type == TaskCfg.TYPE_WEEK:
        datestr = Lobby.GetMonday(today)
    elif type == TaskCfg.TYPE_MONTH:
        datestr = str(today.year)+"_"+ str(today.month)+ "_1"
    elif type == TaskCfg.TYPE_YEAR:
        datestr = str(today.year)+"_1_1"
    return datestr

def GetTask(userid, version):
    task = TaskCfg.TASK_LIST
    tasklist = []
    # 如果当天没有登陆过就会初始化
    now = datetime.date.today()
    datestr = now.strftime("%Y_%m_%d")
    strkey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
    if not Config.grds.exists(strkey):
        InitTaskCfg(userid , datestr)

    for id in task:
        if id in TaskCfg.TASK_CFG:
            cfg = TaskCfg.TASK_CFG[id]
            if version < cfg['version']:
                continue
            taskdic = {
                'tid': cfg['tid'],
                'type': cfg['type'],
                'iconid': cfg['iconid'],
                'series': cfg['series'],# 前置任务解锁条件
                'name':cfg['name'],
                'desc':cfg['desc'],
                'total': cfg['total'],
                'version': cfg['version'],
                'rewardlist':cfg['rewardlist'], 
                'count':0,
            }

            # 处理时间任务类型
            # 原版
            # if cfg["type"] == TaskCfg.TYPE_DAY:
            #     datestr = now.strftime("%Y_%m_%d")
            # elif cfg["type"] == TaskCfg.TYPE_WEEK:
            #     datestr = Lobby.GetMonday(now)
            # elif cfg["type"] == TaskCfg.TYPE_MONTH:
            #     datestr = str(now.year)+"_"+ str(now.month)+ "_1"
            # elif cfg["type"] == TaskCfg.TYPE_YEAR:
            #     datestr = str(now.year)+"_1_1"
            # 封装函数
            datestr = GetTaskDatestr(cfg["type"], now);
            
            strkey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
            if not Config.grds.exists(strkey):
                InitTaskCfg(userid , datestr)
            taskinfo = Config.grds.hgetall(strkey)
            if taskinfo:
                countfield = 'count_'+ str(id)
                statefield = 'state_'+ str(id)
                taskdic['count'] = taskinfo[countfield] if taskinfo.has_key(countfield) else 0
                taskdic['state'] = taskinfo[statefield] if taskinfo.has_key(statefield) else TaskCfg.STATE_INVALID
            tasklist.append(taskdic)
    return tasklist



def TaskReward(userid, taskid):
    # 判断任务id是否合法
    if taskid not in TaskCfg.TASK_LIST:
        return {'code':ErrorCfg.EC_TASK_ID_NOT_EXISTS, 'reason':ErrorCfg.ER_TASK_ID_NOT_EXISTS}
    # 判断用户是否完成任务
    # 根据类型
    now = datetime.date.today()
    cfg = TaskCfg.TASK_CFG[taskid]
    datestr = GetTaskDatestr(cfg['type'], now)

    strkey = TaskCfg.KEY_TASK.format(userid=userid, date = datestr)
    statefield = 'state_' + str(taskid)
    state = int(Config.grds.hget(strkey, statefield))
    if state != TaskCfg.STATE_FINISHED:
        return{'code': ErrorCfg.EC_TASK_NOT_FINISH, 'reason': ErrorCfg.ER_TASK_NOT_FINISH}
    
    # 发奖励
    rewardlist = json.loads(Config.grds.hget(strkey,'reward_'+str(taskid))) 
    for rewarddic in rewardlist:
        Shop.Present(userid, rewarddic['id'], rewarddic['num'])
    Config.grds.hset(strkey, statefield, TaskCfg.STATE_AWARDED)
    return{'code':0}

def UserSign(userid, signtype, date):
    if signtype == TaskCfg.SIGN_TYPE_TODAY:
        date = datetime.datetime.now().today()
    elif signtype == TaskCfg.SIGN_TYPE_AGO:
        date = datetime.datetime.strptime(str(date), "%Y_%m_%d")
    else:
        return Error.ErrResult(ErrorCfg.EC_TASK_SIGN_TYPE_ERROR, ErrorCfg.ER_TASK_SIGN_TYPE_ERROR)
    day = date.day
    moth_firstday = str(date.year) + "_" + str(date.month)+ "_1"
    strKey = TaskCfg.KEY_SIGN.format(userid = userid,date = moth_firstday)
    Config.grds.setbit(strKey, day, 1)
    # 消息队列和脚本传递消息给其他服务

    # 调用task的方法sendaction
    signproto = Sign()
    signproto.userid = userid
    signproto.signtype = signtype
    signproto.date = date.strftime("%Y_%m_%d")
    Action.SendAction(userid,MessageCfg.MSGID_SIGN, signproto.SerializeToString())
