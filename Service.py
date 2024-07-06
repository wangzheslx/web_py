#-*- coding:utf-8 -*-

from socket import *
from proto.message_pb2 import *
import struct

def SendSvrd(host, port ,info):
    if not info :
        # 打印日志
        return 
    ADDR =(host, port)
    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)
    buf = struct.pack(">cccccccci", b'H', b'R', b'P',b'C', chr(1), b'\0', b'\0',b'\0', len(info)) + info
    tcpCliSocket.send(buf)
    tcpCliSocket.close()