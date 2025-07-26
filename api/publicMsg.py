from flask import Blueprint, jsonify, request
from api.basic.database import *
from api.basic.login import *

publicMsg_bp = Blueprint('publicMsg', __name__)

@publicMsg_bp.route('/')
def index():
    return jsonify({'status': 'success', 'message': 'api.publicMsg is running'})

@publicMsg_bp.route('/num', methods=['GET'])
def getNum():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    sql = "SELECT COUNT(*) FROM public_messages"
    result = sqlExecute(sql,None)
    if result[0]:
        return jsonify({'status': 'success', 'num': result[1][0][0]})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@publicMsg_bp.route('/get/from=<int:fromId>&to=<int:toId>', methods=['GET'])
def getPublicMsg(fromId, toId):
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    if fromId < 0 or toId < 0 or fromId > toId:
        return jsonify({'status': 'fail', 'message': '参数错误'}), 400
    sql = "SELECT * FROM public_messages WHERE mid BETWEEN %s AND %s"
    params = (fromId, toId)
    result = sqlExecute(sql, params)
    if result[0]:
        messages = [{'id': row[0], 'uid': row[1], 'username': row[2], 'content': row[3], 'timestamp': row[4]} for row in result[1]]
        return jsonify({'status': 'success', 'messages': messages})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500

@publicMsg_bp.route('/send/', methods=['POST'])
def sendPublicMsg():
    uid_cookie = request.cookies.get('uid')
    passwordHash = request.cookies.get('passwordHash')
    if not login(uid_cookie, passwordHash):
        return jsonify({'status': 'fail', 'message': '登录信息错误'}), 403
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'status': 'fail', 'message': '缺少内容'}), 400
    content = data['content']
    if len(content) > 10000:
        return jsonify({'status': 'fail', 'message': '消息内容过长'}), 400
    uid = int(uid_cookie)
    username = request.cookies.get('username', 'Unknown')
    sql = "INSERT INTO public_messages (uid, username, content) VALUES (%s, %s, %s)"
    params = (uid, username, content)
    result = sqlExecute(sql, params)
    if result[0]:
        return jsonify({'status': 'success', 'message': '消息发送成功'})
    else:
        return jsonify({'status': 'fail', 'message': result[1]}), 500