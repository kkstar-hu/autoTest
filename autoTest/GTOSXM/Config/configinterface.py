url = 'http://apserver.cloudtos.com/api/auth'

BodyXICT = {
    "useraccount" : "admin",
    "password" : "ECB004AB0C9F3A86675A7A67822D8A31",
    "ExtendProperties": {"OP_TERMCD": "XICT"}
}

BodyXRCT = {
    "useraccount" : "admin",
    "password" : "ECB004AB0C9F3A86675A7A67822D8A31",
    "ExtendProperties" : {"OP_TERMCD":"XRCT"}
}

head = {
    "Authorization": "Bearer",
    "Content-Type": "application/json; charset=UTF-8"
}