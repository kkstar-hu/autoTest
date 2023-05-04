loginurl = 'http://apserver.cloudtos-xm.com/api/auth'
url = 'http://apserver.cloudtos-xm.com'
BodyXICT = {
    "useraccount" : "admin",
    "password" : "77B7707169951B7246393E8395FB656C",
    "ExtendProperties": {"OP_TERMCD": "XICT"}
}

BodyXRCT = {                                         # β环境账号密码
    "useraccount" : "autotest",
    "password" : "77B7707169951B7246393E8395FB656C",
    "ExtendProperties" : {"OP_TERMCD":"XRCT"}
}

head = {
    "Authorization": "Bearer",
    "Content-Type": "application/json; charset=UTF-8"
}

global boxNumber
# boxNumber = 'DP123'
global boxPosition
# boxPosition = 'Q9033011'

global boxNumbertwo    # 换箱操作的第一个箱号
# boxNumbertwo = 'KX140'

global boxNumberthree  # 换箱操作的第二个箱号
# boxNumberthree = 'KX133'

