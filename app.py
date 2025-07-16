from flask import Flask, render_template, request, send_file
import pymysql
from io import BytesIO
import json


app = Flask(__name__)

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
#            print("Executing SQL:", o1, o2)
            cursor.execute(o1,o2)
            conn.commit()
            result = cursor.fetchall()
            conn.close()
            return [True,result]
    except:
        return [False, None]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/chat/')
def chat():
    return render_template('chat.html')

def checkLogin():
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username and password:
        result = sqlExecute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        if result[0] and result[1]:
            return True
        else:
            return False
    return False

@app.route('/api/login/')
def login():
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username and password:
        result = sqlExecute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        print(result)
        if result[0] and result[1]:
            print("Login successful:", username)
            return "OK"
        elif result[0]:
            print("User not found:", username)
            return "Not found"
        else:
            print("SQL execution error")
            return "Server error"
    else:
        print("Client error: Missing username or password")
        return "Cilent error"

@app.route("/api/register/")
def register():
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    print(username, password)
    if username and password:
        result = sqlExecute("SELECT * FROM users WHERE username=%s", (username))
        print(result)
        if result[0] and result[1]:
            return "Already exists"
        elif result[0]:
            print(username, password)
            result = sqlExecute("INSERT INTO users VALUES (NULL, %s, %s)", (username, password))
            if result[0]:
                print("Registration successful:", username)
                return "OK"
            else:
                print("SQL execution error during registration")
                return "Server Error"
        else:
            print("SQL execution error")
            return "Server Error"
    else:
        print("Client error: Missing username or password")
        return "Cilent error"

@app.route('/api/getMsgNum/')
def getMsgNum():
    if not checkLogin():
        return "Login error"
    else:
        result = sqlExecute("SELECT COUNT(*) FROM messages", ())
        if result[0] and result[1]:
            return str(result[1][0][0])
        else:
            return "Server error"
        
@app.route('/api/getMsg/id=<int:id>')
def getMsg(id):
    if not checkLogin():
        return "Login error"
    else:
        result = sqlExecute("SELECT * FROM messages WHERE id=%s", (id,))
        if result[0] and result[1]:
            return str(result[1][0])
        else:
            return "Server error"

@app.route('/api/getMsgList/from=<int:from_id>&to=<int:to_id>')
def getMsgList(from_id, to_id):
    if not checkLogin():
        return "Login error"
    else:
        result = sqlExecute("SELECT * FROM messages WHERE id BETWEEN %s AND %s", (str(from_id), str(to_id)))
        print("SQL result:", result)
        if result[0] and result[1]:
            dat=[]
            for i in range(len(result[1])):
                dat.append([str(result[1][i][0]), str(result[1][i][1]), str(result[1][i][2]), str(result[1][i][3]), str(result[1][i][4])])
            print("Data prepared:", dat)
            return json.dumps(dat)
        else:
            return "Server error"

@app.route('/api/sendMsg/', methods=['POST'])
def sendMsg():
    if not checkLogin():
        return "Login error"
    else:
        username = request.cookies.get("username")
        content = request.get_data(as_text = True)
        print("content:",content)
        if content:
            result = sqlExecute("INSERT INTO messages VALUES (NULL,sysdate(),%s,%s,'text')", (username, content))
            if result[0]:
                return "OK"
            else:
                return "Server error"
        else:
            return "server error"

def allowImgtype(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg', 'tiff', 'ico'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def allowImgSize(file):
    max_size = 32 * 1024 * 1024  # 32 MB
    return len(file.read()) <= max_size

def allowFileSize(file):
    max_size = 256 * 1024 * 1024  # 256 MB
    return len(file.read()) <= max_size

@app.route('/api/sendImg/', methods=['POST'])
def sendImg():
    print("sendImg called")
    if not checkLogin():
        return "Login error"
    else:
        print(request.files)
        if 'image' not in request.files:
            print("No file part in request")
            return "No file part"
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        if not allowImgtype(file.filename):
            return "Invalid file type"
        if not allowImgSize(file):
            return "File too large"
        username = request.cookies.get("username")
        file.seek(0)
        result = sqlExecute("INSERT INTO images VALUES (NULL, %s, %s, %s)", (username, file.filename, file.read()))
        if result[0]:
            getid = sqlExecute("SELECT COUNT(*) FROM images", ())
            if getid[0] and getid[1]:
                imgHtml = '<img src="/api/img/id=' + str(getid[1][0][0]) + '" alt="' + file.filename + '" style="max-width: 20%; max-height: 20%;">'
                send = sqlExecute("INSERT INTO messages VALUES (NULL, sysdate(), %s, %s, 'img')", (username, imgHtml))
                if send[0]:
                    return "OK"
                else:
                    return "Server error"
            else:
                return "Server error"
        else:
            return "Server error"

@app.route('/api/sendFile/', methods=['POST'])
def sendFile():
    if not checkLogin():
        return "Login error"
    else:
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if not allowFileSize(file):
            return "File too large"
        username = request.cookies.get("username")
        file.seek(0)
        result = sqlExecute("INSERT INTO files VALUES (NULL, %s, %s, %s)", (username, file.filename, file.read()))
        if result[0]:
            getid = sqlExecute("SELECT COUNT(*) FROM files", ())
            if getid[0] and getid[1]:
                fileHtml = 'file: <a href="/api/file/id=' + str(getid[1][0][0]) + '" download="' + file.filename + '">' + file.filename + '</a>'
                send = sqlExecute("INSERT INTO messages VALUES (NULL, sysdate(), %s, %s, 'file')", (username, fileHtml))
                if send[0]:
                    return "OK"
                else:
                    return "Server error"
            else:
                return "Server error"
        else:
            return "Server error"

@app.route('/api/img/id=<int:id>')
def getImg(id):
    result = sqlExecute("SELECT * FROM images WHERE id=%s", (id,))
    if result[0] and result[1]:
        return send_file(BytesIO(result[1][0][3]), download_name = result[1][0][2])
    else:
        return "Server error"

@app.route('/api/file/id=<int:id>')
def getFile(id):
    result = sqlExecute("SELECT * FROM files WHERE id=%s", (id,))
    if result[0] and result[1]:
        return send_file(BytesIO(result[1][0][3]), download_name = result[1][0][2])
    else:
        return "Server error"

if __name__ == '__main__':
    app.run(host='0.0.0.0')