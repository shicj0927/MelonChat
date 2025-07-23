from flask import Blueprint, jsonify, request
from api.basic.database import *
from api.basic.login import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'success', 'message': 'api.user is running'})

@user_bp.route('/getName/<int:uid>', methods=['GET'])
def getName(uid):
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    sql = "SELECT username FROM users WHERE uid = %s"
    params = (uid,)
    result = sqlExecute(sql, params)
    if result[0]:
        if result[1]:
            return jsonify({'status': 'success', 'username': result[1][0][0]})
        else:
            return jsonify({'status': 'fail', 'message': '用户不存在'}), 404
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/getUid/<string:username>', methods=['GET'])
def getUid(username):
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    sql = "SELECT uid FROM users WHERE username = %s"
    params = (username,)
    result = sqlExecute(sql, params)
    if result[0]:
        if result[1]:
            return jsonify({'status': 'success', 'uid': result[1][0][0]})
        else:
            return jsonify({'status': 'fail', 'message': '用户不存在'}), 404
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/search/<keyword>', methods=['GET'])
def search(keyword):
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    if len(keyword) < 2:
        return jsonify({'status': 'fail', 'message': '搜索关键字长度不能小于2'}), 400
    sql = "SELECT uid, username FROM users WHERE username LIKE %s"
    params = (keyword + '%',)
    result = sqlExecute(sql, params)
    if result[0]:
        if result[1]:
            users = [{'uid': row[0], 'username': row[1]} for row in result[1]]
            return jsonify({'status': 'success', 'users': users})
        else:
            return jsonify({'status': 'fail', 'message': '没有找到用户'}), 404
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/getInfo/<int:uid>', methods=['GET'])
def getUserInfo(uid):
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    sql = "SELECT uid, username, label, homepage, iid FROM users WHERE uid = %s"
    params = (uid,)
    result = sqlExecute(sql, params)
    if result[0]:
        if result[1]:
            user_info = {
                'uid': result[1][0][0],
                'username': result[1][0][1],
                'label': result[1][0][2],
                'homepage': result[1][0][3],
                'iid': result[1][0][4]
            }
            return jsonify({'status': 'success', 'user_info': user_info})
        else:
            return jsonify({'status': 'fail', 'message': '用户不存在'}), 404
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/checkLogin', methods=['GET'])
def checkLogin():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not uid_cookie or not passwordHash:
        return jsonify({'status': 'fail', 'message': '未登录'}), 403
    if login(uid_cookie, passwordHash):
        return jsonify({'status': 'success', 'message': '已登录'})
    else:
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403

@user_bp.route('/create', methods=['POST'])
def createUser():
    username = request.json.get('username')
    passwordHash = request.cookies.get('passwordHash')
    print("Creating user:", username, passwordHash)
    querySql = "SELECT * FROM users WHERE username = %s"
    queryParams = (username,)
    result = sqlExecute(querySql, queryParams)
    if result[0] and result[1]:
        return jsonify({'status': 'fail', 'message': '用户名已存在'}), 400
    elif not result[0]:
        return jsonify({'status': 'fail', 'message': result[1]}), 500
    insertSql = "INSERT INTO users (username, passwordHash) VALUES (%s, %s)"
    insertParams = (username, passwordHash)
    insertResult = sqlExecute(insertSql, insertParams)
    if insertResult[0]:
        uidSql = "SELECT uid FROM users WHERE username = %s"
        uidParams = (username,)
        uidResult = sqlExecute(uidSql, uidParams)
        uid = None
        if uidResult[0] and uidResult[1]:
            uid = uidResult[1][0][0]
        else:
            return jsonify({'status': 'fail', 'message': uidResult[1]}), 500
        return jsonify({'status': 'success', 'uid': uid, 'message': '用户创建成功'}), 200
    else:
        return jsonify({'status': 'fail', 'message': insertResult[1]}), 500

@user_bp.route('/setLabel', methods=['POST'])
def setLabel():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    label = request.json.get('label')
    if not label:
        return jsonify({'status': 'fail', 'message': '缺少参数'}), 400
    if len(label) > 100:
        return jsonify({'status': 'fail', 'message': '标签长度不能超过100个字符'}), 400
    sql = "UPDATE users SET label = %s WHERE uid = %s"
    params = (label, uid_cookie)
    result = sqlExecute(sql, params)
    if result[0]:
        return jsonify({'status': 'success', 'message': '标签更新成功'})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/setHomepage', methods=['POST'])
def setHomepage():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    homepage = request.json.get('homepage')
    if not homepage:
        return jsonify({'status': 'fail', 'message': '缺少参数'}), 400
    if len(homepage) > 10000:
        return jsonify({'status': 'fail', 'message': '主页内容长度不能超过10000个字符'}), 400
    sql = "UPDATE users SET homepage = %s WHERE uid = %s"
    params = (homepage, uid_cookie)
    result = sqlExecute(sql, params)
    if result[0]:
        return jsonify({'status': 'success', 'message': '主页更新成功'})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/setImage', methods=['POST'])
def setImage():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    iid = request.json.get('iid')
    if not iid:
        return jsonify({'status': 'fail', 'message': '缺少参数'}), 400
    sql = "UPDATE users SET iid = %s WHERE uid = %s"
    params = (iid, uid_cookie)
    result = sqlExecute(sql, params)
    if result[0]:
        return jsonify({'status': 'success', 'message': '头像更新成功'})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@user_bp.route('/setPassword', methods=['POST'])
def setPassword():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    new_password_hash = request.json.get('newPasswordHash')
    if not new_password_hash:
        return jsonify({'status': 'fail', 'message': '缺少参数'}), 400
    sql = "UPDATE users SET passwordHash = %s WHERE uid = %s"
    params = (new_password_hash, uid_cookie)
    result = sqlExecute(sql, params)
    if result[0]:
        return jsonify({'status': 'success', 'message': '密码更新成功'})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500