import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'final-fix-2026'

# Render-er jonno exact database path setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='student')

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    subject = db.Column(db.String(50))
    class_name = db.Column(db.String(10))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Simple Responsive HTML ---
HEAD = """<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#f0f2f5;padding:20px; font-family:sans-serif;}.card{border-radius:15px; border:none; box-shadow:0 5px 15px rgba(0,0,0,0.1);}</style>"""

@app.route('/')
def index(): return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        p, pw = request.form.get('phone'), request.form.get('password')
        if User.query.filter_by(phone=p).first(): return "Phone number already exists!"
        db.session.add(User(phone=p, password=generate_password_hash(pw)))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template_string(HEAD + '<div class="card p-4"><h3>Register</h3><form method="POST"><input name="phone" placeholder="Phone" class="form-control mb-2" required><input type="password" name="password" placeholder="Pass" class="form-control mb-2" required><button class="btn btn-success w-100">Register</button></form><p class="mt-2 text-center"><a href="/login">Back to Login</a></p></div>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(phone=request.form.get('phone')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        return "Invalid Credentials!"
    return render_template_string(HEAD + '<div class="card p-4"><h3>Login</h3><form method="POST"><input name="phone" placeholder="Phone" class="form-control mb-2" required><input type="password" name="password" placeholder="Pass" class="form-control mb-2" required><button class="btn btn-primary w-100">Login</button></form><p class="mt-2 text-center"><a href="/register">Register New</a></p></div>')

@app.route('/dashboard')
@login_required
def dashboard():
    res = Result.query.filter_by(user_id=current_user.id).all()
    return render_template_string(HEAD + '<h4>Welcome, {{current_user.phone}}</h4><a href="/quiz/10/Math" class="btn btn-info w-100 mb-3">Take Math Test</a><hr><h6>Results:</h6><ul>{% for r in results %}<li>{{r.subject}}: {{r.score}}</li>{% endfor %}</ul><a href="/logout" class="btn btn-danger btn-sm">Logout</a>', results=res)

@app.route('/quiz/<class_id>/<subject>')
@login_required
def quiz(class_id, subject):
    return render_template_string(HEAD + """<div id="q-ui" class="card p-4"><h5>{{subject}} (Class {{class_id}})</h5><p>What is 5x5?</p><input type="radio" name="a" value="25"> 25 <br><button onclick="done()" class="btn btn-primary mt-3">Finish</button></div>
    <div id="ad-ui" style="display:none; text-align:center;"><h3>Wait 5s...</h3><h1 id="timer">5</h1>
    <script type="text/javascript">atOptions={'key':'e0fe653541837054d29ca1be1eb04acc','format':'iframe','height':300,'width':160,'params':{}};</script>
    <script src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script></div>
    <script>function done(){document.getElementById('q-ui').style.display='none';document.getElementById('ad-ui').style.display='block';let c=5;let t=setInterval(()=>{c--;document.getElementById('timer').innerText=c;if(c<=0){clearInterval(t);fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({score:10,subject:'{{subject}}',class_name:'{{class_id}}'})}).then(()=>window.location.href='/dashboard');}},1000);}</script>""", subject=subject, class_id=class_id)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    d = request.json
    db.session.add(Result(user_id=current_user.id, score=d['score'], subject=d['subject'], class_name=d['class_name']))
    db.session.commit()
    return jsonify({"ok":True})

@app.route('/logout')
def logout(): logout_user(); return redirect(url_for('login'))

# Server start logic
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Tables toiri nishchit korbe
    app.run()
      
