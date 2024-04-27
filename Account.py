#-*- coding: utf-8 -*-
import Config
import AccountCfg
import re
import datetime
import DBManage
import ErrorCfg

def CheckPhonenum(phonenum):
    phonelist = [139, 138, 137, 136, 134, 135, 147, 150, 151, 152, 157, 158, 159, 172, 178,
            130, 131, 132, 140, 145, 146, 155, 156, 166, 185, 186, 175, 176, 196,
            133, 149, 153, 177, 173, 180, 181, 189, 191, 193, 199,
            162, 165, 167, 170, 171]
    if len(phonenum) == 11 and str(phonenum).isdigit() and (int(phonenum[:3])) in phonelist:
        return True
    else:
        return False

def CheckUserIdNotRepeat(userid):
    # 检测账号是否重复
    result = Config.gdb.select("user_data", where = "userid=$userid", vars=dict(userid=userid), what='count(*) as num')
    if result and result[0].num >= 1:
        return False
    else:
        return True


def CheckIdCard(idcard):
    # 正则表达式匹配身份证号码格式
    pattern = re.compile(r'^\d{17}[\dXx]$')
    if not re.match(pattern, idcard):
        return False

    # 加权因子
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码字符集
    check_codes = '10X98765432'
    
    # 计算校验位
    sum = 0
    for i in range(17):
        sum += int(idcard[i]) * factors[i]
    remainder = sum % 11
    if idcard[-1] != check_codes[remainder]:
        return False

    return True
    # stridcard = str(idcard)
    # stridcard = stridcard.strip()
    # idcard_list = list(stridcard)
    # # 地区校验
    # if (stridcard)[0:2] not in AccountCfg.AREAID:
    #     return False

    # # 15位身份号码检测
    # if len(stridcard) == 15:
    #     if ((int(stridcard[6:8]) + 1900) % 400 == 0 or (
    #             (int(stridcard[6:8]) + 1900) % 100 != 0 and (int(stridcard[6:8]) + 1900) % 4 == 0)):
    #         pattern = re.compile(
    #             '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
    #     else:
    #         pattern = re.compile(
    #             '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
    #     if re.match(pattern, stridcard):
    #         return True
    #     else:
    #         return False
    # # 18位身份号码检测
    # elif len(stridcard) == 18:
    #     # 出生日期的合法性检查
    #     # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
    #     # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
    #     if (int(stridcard[6:10]) % 400 == 0 or (int(stridcard[6:10]) % 100 != 0 and int(stridcard[6:10]) % 4 == 0)):
    #         # 闰年出生日期的合法性正则表达式
    #         pattern = re.compile(
    #             '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')
    #     else:
    #         # 平年出生日期的合法性正则表达式
    #         pattern = re.compile(
    #             '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')
    #     # 测试出生日期的合法性
    #     if re.match(pattern, stridcard):
    #         # 计算校验位
    #         ten = ['X', 'x']
    #         ID = ["10" if x in ten else x for x in idcard_list]     #将字母X/x替换为10
    #         IDWeight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    #         Checkcode = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
    #         sum = 0
    #         for i in range(17):
    #             sum += int(ID[i]) * IDWeight[i]
    #         if Checkcode[sum % 11] == int(ID[17]):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
    # else:
    #     return False
    



def CheckPassword(password):
    # 检查密码格式
    pattern = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z0-9@$!%*?&]{8,16}$')

    if re.match(pattern, password):
        return True
    return False

# 注册用户
def InitUser(phonenum, password, nick, sex, idcard):
    now = datetime.datetime.now()
    DBManage.InsertRegisterUser(phonenum, password, nick, sex, idcard, now)
    # 初始化用户背包

# 检测用户的登录
def VerifyAccount(userid,password):
    result = Config.gdb.select("user_data" , what = "password", vars = dict(userid=userid), where="userid=$userid")
    if not result:
        return{"code":ErrorCfg.EC_LOGIN_USERID_ERROR,"reason":ErrorCfg.ER_LOGIN_USERID_ERROR}
    if result[0]['password'] != password:
        return{"code":ErrorCfg.EC_LOGIN_PASSWORD_ERROR,"reason":ErrorCfg.ER_LOGIN_PASSWORD_ERROR}
    # 帐号不正常，拒绝登录
    # if result[0]['status'] != Config.USER_STATUS_NOLMAL:
    #     return{"code":ErrorCfg.EC_LOGIN_STATUS_ERROR,"reason":ErrorCfg.ER_LOGIN_STATUS_ERROR}
    return {"code":0}


def HandleLogin(userid):
    now = datetime.datetime.now()
    Config.gdb.update(
        "user_data",
        lastlogintime = now,
        where="userid=$userid",
        vars=dict(userid=userid)    
    )
    return {"code":0}