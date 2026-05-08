import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'modern-quiz-app-2026'

# Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    subject = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- UI Layout ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background: #f4f4f9; font-family: 'Segoe UI', sans-serif; }
    .card { border-radius: 15px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .btn-main { background: #6c5ce7; color: white; padding: 20px; font-size: 20px; font-weight: bold; border-radius: 12px; transition: 0.3s; width: 100%; border: none; }
    .btn-main:hover { background: #a29bfe; color: white; }
    .ad-slot { width: 100%; height: 100px; background: #eee; display: flex; align-items: center; justify-content: center; margin: 10px 0; border: 1px dashed #bbb; }
    .hidden { display: none; }
</style>
"""

# --- Auth Routes ---
@app.route('/')
def index(): return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        p, pw = request.form.get('phone'), request.form.get('password')
        if not User.query.filter_by(phone=p).first():
            db.session.add(User(phone=p, password=generate_password_hash(pw)))
            db.session.commit()
            return redirect(url_for('login'))
    return render_template_string(UI_STYLE + '<div class="container mt-5"><div class="card p-4"><h3>Register</h3><form method="POST"><input name="phone" placeholder="Phone" class="form-control mb-3" required><input type="password" name="password" placeholder="Password" class="form-control mb-3" required><button class="btn btn-success w-100">Sign Up</button></form></div></div>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(phone=request.form.get('phone')).first()
        if u and check_password_hash(u.password, request.form.get('password')):
            login_user(u); return redirect(url_for('main_tab'))
    return render_template_string(UI_STYLE + '<div class="container mt-5"><div class="card p-4"><h3>Login</h3><form method="POST"><input name="phone" placeholder="Phone" class="form-control mb-3" required><input type="password" name="password" placeholder="Password" class="form-control mb-3" required><button class="btn btn-primary w-100">Login</button></form></div></div>')

# --- Main Feature Routes ---

@app.route('/main_tab')
@login_required
def main_tab():
    return render_template_string(UI_STYLE + """
    <div class="container mt-3">
        <!-- Ad at Corner/Top -->
        <div class="text-center mb-4">
             <script type="text/javascript">
                atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
             </script>
             <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>

        <div class="text-center" style="margin-top: 50px;">
            <button onclick="startPrep()" class="btn-main shadow">TEST MY PREPARATION</button>
        </div>

        <!-- 3 Sec Ad Overlay -->
        <div id="ad-overlay" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
            <h3>Loading Test...</h3>
            <h1 id="timer3">3</h1>
            <div class="mt-4">
                <script type="text/javascript">
                    atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
                </script>
                <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
            </div>
        </div>
    </div>
    <script>
    function startPrep() {
        document.getElementById('ad-overlay').classList.remove('hidden');
        let c = 3;
        let t = setInterval(() => {
            c--; document.getElementById('timer3').innerText = c;
            if(c <= 0) { clearInterval(t); window.location.href = '/choice'; }
        }, 1000);
    }
    </script>
    """)

@app.route('/choice')
@login_required
def choice():
    return render_template_string(UI_STYLE + """
    <div class="container mt-5">
        <div class="card p-4 text-center">
            <h3>Select Your Class & Subject</h3>
            <select class="form-select mb-3" id="class"><option>Class 6</option><option>Class 10</option></select>
            <select class="form-select mb-3" id="subject"><option>Math</option><option>ICT</option></select>
            <button onclick="window.location.href='/exam'" class="btn btn-primary w-100">Start MCQ</button>
        </div>
    </div>
    """)

@app.route('/exam')
@login_required
def exam():
    return render_template_string(UI_STYLE + """
    <div class="container mt-4">
        <div id="q-box" class="card p-4">
            <h4>Question: What is 2+2?</h4>
            <div class="form-check"><input type="radio" name="q" class="form-check-input"> 4</div>
            <div class="form-check"><input type="radio" name="q" class="form-check-input"> 5</div>
            <button onclick="submitExam()" class="btn btn-success mt-4 w-100">Submit</button>
        </div>

        <div id="result-ad" class="hidden text-center mt-5">
            <h3>Processing Result...</h3>
            <h1 id="timer5">5</h1>
            <script type="text/javascript">
                atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
            </script>
            <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>
    </div>
    <script>
    function submitExam() {
        document.getElementById('q-box').classList.add('hidden');
        document.getElementById('result-ad').classList.remove('hidden');
        let c = 5;
        let t = setInterval(() => {
            c--; document.getElementById('timer5').innerText = c;
            if(c <= 0) { clearInterval(t); window.location.href = '/final_result'; }
        }, 1000);
    }
    </script>
    """)

@app.route('/final_result')
@login_required
def final_result():
    return render_template_string(UI_STYLE + """
    <div class="container mt-5 text-center">
        <div class="card p-5">
            <h2 class="text-success">Success!</h2>
            <p>Your Score: 10/10</p>
            <a href="/main_tab" class="btn btn-primary">Go Home</a>
        </div>
    </div>
    """)

@app.route('/logout')
def logout(): logout_user(); return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run()
