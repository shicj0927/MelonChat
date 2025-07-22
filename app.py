from flask import Flask, render_template

app = Flask(__name__)

from api.user import user_bp
from api.publicMsg import publicMsg_bp
from api.file import file_bp
from api.image import image_bp
from api.chat import chat_bp
from api.note import note_bp
from api.admin import admin_bp

def registerBlueprint(part, url):
    app.register_blueprint(
        part,
        url_prefix=url,
        static_folder='static',
        template_folder='templates'
    )

registerBlueprint(user_bp, '/api/user')
registerBlueprint(publicMsg_bp, '/api/publicMsg')
registerBlueprint(file_bp, '/api/file')
registerBlueprint(image_bp, '/api/image')
registerBlueprint(chat_bp, '/api/chat')
registerBlueprint(note_bp, '/api/note')
registerBlueprint(admin_bp, '/api/admin')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/publicMsg')
def publicMsg():
    return render_template('publicMsg.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/user/<int:uid>')
def user_page(uid):
    return render_template('user.html', uid=uid)

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/note')
def note_page():
    return render_template('note.html')

@app.route('/note/<int:nid>')
def note_detail_page(nid):
    return render_template('note_detail.html', nid=nid)

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)