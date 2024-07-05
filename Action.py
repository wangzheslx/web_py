#-*- coding: utf-8 -*-
import ActionCfg
from proto.message_pb2 import Message
import Config

def SendAction(userid, msgid, protoinfo):
    strkey = ActionCfg.KEY_ACTION_LIST
    msg = Message()
    msg.userid = userid
    msg.msgid = msgid
    msg.string = protoinfo
    Config.grds.rpush(strkey, msg.SerializeToString())
