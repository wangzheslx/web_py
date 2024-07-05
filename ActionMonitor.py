#-*- coding: utf-8 -*-

import ActionCfg
import Config
from proto.message_pb2 import Message
import MessageCfg

def DistributeAction(actiontype, actionmsg):
    for key in ActionCfg.ACTION_MAPPINT[actiontype]:
        Config.grds.rpush(key, actionmsg)


def ActionMonitor():
    while True:
        strKey = ActionCfg.KEY_ACTION_LIST
        res = Config.grds.blpop(strKey)[1]
        msg = Message()
        msg.ParseFromString(res)

        # 根据事件分发配置, 发送数据
        msgid =  int(msg.msgid) & MessageCfg.MSGID
        if msgid == MessageCfg.MSGID_SIGN:
            DistributeAction(MessageCfg.MSGID_SIGN, res)
        elif msgid == MessageCfg.MSGID_LOGIN:
            DistributeAction(MessageCfg.MSGID_LOGIN, res)

if __name__ == "__main__":
    ActionMonitor()