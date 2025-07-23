from api.basic.database import *

def login(uid, passwordHash):
    sql = "SELECT * FROM users WHERE uid = %s AND passwordHash = %s"
    params = (uid, passwordHash)
    result = sqlExecute(sql, params)
    
    if result[0]:
        if result[1]:
            return True
        else:
            return False
    else:
        return False