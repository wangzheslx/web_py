#-*- coding:utf-8 -*-
import json

def ErrResult(code, reason):
    return json.dumps({'code':code, 'reason':reason})
