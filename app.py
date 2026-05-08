import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure-mcq-key-789'

# Database configuration for Render
# Ekhane database file-er absolute path set kora hoyeche jate Render error na dey
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
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

# --- CSS & Responsive Design ---
HEAD = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background: #f0f2f5; font-family: sans-serif; }
    .card-custom { border-radius: 15px; border:none; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .btn-m { border-radius: 10px; padding: 12px; font-weight: bold; }
</style>
"""

# --- Templates ---
LOGIN_HTML = HEAD + """
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-11 col-md-4 card card-custom p-4">
            <h3 class="text-center mb-4">Login</h3>
            <form method="POST">
                <input name="phone" class="form-control mb-3" placeholder="Phone Number" required>
                <input type="password" name="password" class="form-control mb-3" placeholder="Password" required>
                <button type="submit" class="btn btn-primary w-100 btn-m">Sign In</button>
            </form>
            <p class="text-center mt-3">New? <a href="/register">Register</a></p>
        </div>
    </div>
</div>
"""

REGISTER_HTML = HEAD + """
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-11 col-md-4 card card-custom p-4">
            <h3 class="text-center mb-4">Register</h3>
            <form method="POST">
                <input name="phone" class="form-control mb-3" placeholder="Phone Number" required>
                <input type="password" name="password" class="form-control mb-3" placeholder="Password" required>
                <button type="submit" class="btn btn-success w-100 btn-m">Create Account</button>
            </form>
            <p class="text-center mt-3">Have account? <a href="/login">Login</a></p>
        </div>
    </div>
</div>
"""

DASHBOARD_HTML = HEAD + """
<div class="container mt-4">
    <div class="card card-custom p-3 mb-4 bg-primary text-white">
        <h5>ID: {{ current_user.phone }}</h5>
        <a href="/logout" class="text-white small">Logout</a>
    </div>
    <h6>Start Test:</h6>
    <div class="d-grid gap-2">
        <a href="/quiz/6/Science" class="btn btn-white bg-white btn-m shadow-sm text-start">Class 6 Science</a>
        <a href="/quiz/10/Math" class="btn btn-white bg-white btn-m shadow-sm text-start">Class 10 Math</a>
    </div>
</div>
"""

QUIZ_HTML = HEAD + """
<div id="q-ui" class="container mt-4">
    <div class="card card-custom p-4">
        <h5>{{ subject }} (Class {{ class_id }})</h5>
        <hr>
        <p>Q1. Python is a ___ language?</p>
        <input type="radio" name="q1" value="10"> High Level <br>
        <input type="radio" name="q1" value="0"> Low Level <br><br>
        <button onclick="finish()" class="btn btn-primary w-100 btn-m">Submit</button>
    </div>
</div>
<div id="ad-ui" style="display:none;" class="container mt-5 text-center">
    <div class="card card-custom p-5">
        <h4>Wait 5 Seconds...</h4>
        <h1 id="timer" class="text-danger">5</h1>
        <div class="mt-3">
            <script type="text/javascript">
                atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
            </script>
            <script src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>
    </div>
</div>
<script>
function finish() {
    document.getElementById('q-ui').style.display='none';
    document.getElementById('ad-ui').style.display='block';
    let c = 5;
    let t = setInterval(()=>{
        c--; document.getElementById('timer').innerText=c;
        if(c<=0){
            clearInterval(t);
            fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({score: 10, subject: '{{subject}}', class_name: '{{class_id}}'})
            }).then(()=>window.location.href='/dashboard');
        }
    },1000);
}
</script>
"""

# --- Routes ---
@app.route('/')
def home(): return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        p, pw = request.form.get('phone'), request.form.get('password')
        if User.query.filter_by(phone=p).first(): return "Phone exists"
        db.session.add(User(phone=p, password=generate_password_hash(pw)))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(phone=request.form.get('phone')).first()
        if u and check_password_hash(u.password, request.form.get('password')):
            login_user(u); return redirect(url_for('dashboard'))
        return "Wrong Info"
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
@login_required
def dashboard():
    res = Result.query.filter_by(user_id=current_user.id).all()
    return render_template_string(DASHBOARD_HTML, results=res)

@app.route('/quiz/<class_id>/<subject>')
@login_required
def quiz(class_id, subject):
    return render_template_string(QUIZ_HTML, class_id=class_id, subject=subject)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    d = request.json
    db.session.add(Result(user_id=current_user.id, score=d['score'], subject=d['subject'], class_name=d['class_name']))
    db.session.commit()
    return jsonify({"ok": True})

@app.route('/logout')
def logout(): logout_user(); return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run()
