#-*- coding: utf-8 -*-
import logging.config
import web
import Account
import json
import ErrorCfg
import Error
import Config
import logging
import logging.config
import Shop

urls = (
    '/', 'hello',
    '/register', 'Register',  
    '/login', 'Login', 
    '/shop/cfg','Shop_cfg',
    '/shop/buy', 'Shop_buy',


)

app = web.application(urls, globals())
application = app.wsgifunc()
# print(Config.gdb)#测试Mysql

# 装饰器+日志模块
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('applog')

def CatchError(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            logger.exception(e)
    return wrapper
            

class hello:
    def GET(self, name):
        if not name:
            name = "World!"
        return 'Hello, '+name
    
class Register:
    @CatchError
    def POST(self):
        req = web.input(phonenum = '', password = '', nick = '', sex = '', idcard = '')
        phonenum = req.phonenum
        password = req.password
        nick = req.nick
        sex = req.sex
        idcard = req.idcard
        #检测手机号格式
        if not Account.CheckPhonenum(phonenum):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_PHONENYM_TYPE_ERROR, ErrorCfg.ER_REGISTER_PHONENYM_TYPE_ERROR)

        #检测账号是否重复
        if not Account.CheckUserIdNotRepeat(phonenum):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_USERID_REPEAT, ErrorCfg.ER_REGISTER_USERID_REPEAT)
        
        # #检测身份证号格式
        if not Account.CheckIdCard(idcard):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_IDCARD_TYPE_ERROR, ErrorCfg.ER_REGISTER_IDCARD_TYPE_ERROR)
        
        # # 检测密码格式
        if not Account.CheckPassword(password):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_PASSWORD_TYPE_ERROR, ErrorCfg.ER_REGISTER_PASSWORD_TYPE_ERROR)
        
        # 注册账号
        Account.InitUser(phonenum, password, nick, sex, idcard)
        return json.dumps({'code':0})


# 登陆
class Login:
    @CatchError
    def POST(self):
        req = web.input(userid = '', password = '')
        userid = req.userid
        password = req.password
        result = Account.VerifyAccount(userid,password)
        if result['code'] != 0:
            return Error.ErrResult(result['code'], result['reason'])
        # 登录处理
        result = Account.HandleLogin(userid)

        return json.dumps({'code':0})
       

class Shop_cfg:
    @CatchError
    def GET(self):
        req = web.input(version = '')
        version = int(req.version)
        shopcfg = Shop.GetShopCfg(version)
        return json.dumps({"code": 0, 'shopcfg':shopcfg})


class Shop_buy:
    @CatchError
    def GET(self):
        req = web.input(userid = '', propid = '', propnum = '', shopversion = '', version = '')
        userid = req.userid
        propid = req.propid
        propnum = req.propnum
        shopversion = req.shopversion
        version = req.version
        dictInfo = Shop.ShopBuy(userid , propid , propnum, shopversion, version)
        return json({'code': 0})
        



