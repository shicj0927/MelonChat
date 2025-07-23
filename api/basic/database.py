import pymysql
from io import BytesIO
import json

def sqlExecute(o1,o2):
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='MelonChat',
            password='MelonChat123',
            db='MelonChat',
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            print("Executing SQL:", o1, o2)
            cursor.execute(o1,o2)
            conn.commit()
            result = cursor.fetchall()
            print("SQL Result:", result)
            conn.close()
            return [True,result]
    except:
        return [False, "数据库错误"]