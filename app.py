import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dashboard-ads-fixed-786'

# Render-er jonno Database path fix
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mcq_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    subject = db.Column(db.String(50))
    class_name = db.Column(db.String(10))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- CSS & Design ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .card { border-radius: 12px; border: none; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 15px; }
    .btn-custom { border-radius: 8px; padding: 12px; font-weight: 600; transition: 0.3s; }
    .dashboard-header { background: #007bff; color: white; padding: 20px; border-radius: 0 0 20px 20px; margin-bottom: 25px; }
    .ad-container { background: #fff; padding: 10px; border: 1px dashed #ccc; margin-top: 20px; }
</style>
"""

# --- Routes ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        p, pw = request.form.get('phone'), request.form.get('password')
        if User.query.filter_by(phone=p).first(): return "Phone already exists!"
        db.session.add(User(phone=p, password=generate_password_hash(pw)))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template_string(UI_STYLE + '<div class="container mt-5"><div class="card p-4"><h3>Register</h3><form method="POST"><input name="phone" class="form-control mb-3" placeholder="Phone Number" required><input type="password" name="password" class="form-control mb-3" placeholder="Password" required><button class="btn btn-success w-100 btn-custom">Sign Up</button></form></div></div>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(phone=request.form.get('phone')).first()
        if u and check_password_hash(u.password, request.form.get('password')):
            login_user(u); return redirect(url_for('dashboard'))
        return "Invalid phone or password!"
    return render_template_string(UI_STYLE + '<div class="container mt-5"><div class="card p-4"><h3>Login</h3><form method="POST"><input name="phone" class="form-control mb-3" placeholder="Phone Number" required><input type="password" name="password" class="form-control mb-3" placeholder="Password" required><button class="btn btn-primary w-100 btn-custom">Login</button></form><p class="mt-3 text-center">New? <a href="/register">Register</a></p></div></div>')

@app.route('/dashboard')
@login_required
def dashboard():
    results = Result.query.filter_by(user_id=current_user.id).all()
    return render_template_string(UI_STYLE + """
    <div class="dashboard-header text-center">
        <h3>My Dashboard</h3>
        <p>User: {{ current_user.phone }}</p>
        <a href="/logout" class="btn btn-sm btn-light">Logout</a>
    </div>
    <div class="container">
        <div class="card p-3">
            <h5>Available Exams:</h5>
            <div class="d-grid gap-2">
                <a href="/quiz/6/General-Science" class="btn btn-outline-primary text-start">Class 6 - General Science</a>
                <a href="/quiz/10/ICT" class="btn btn-outline-primary text-start">Class 10 - ICT</a>
            </div>
        </div>
        <div class="card p-3">
            <h5>My Test History:</h5>
            <table class="table table-sm">
                <thead><tr><th>Subject</th><th>Score</th></tr></thead>
                <tbody>
                    {% for r in results %}
                    <tr><td>{{ r.subject }}</td><td><span class="badge bg-success">{{ r.score }} / 10</span></td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    """)

@app.route('/quiz/<class_id>/<subject>')
@login_required
def quiz(class_id, subject):
    return render_template_string(UI_STYLE + """
    <div id="quiz-box" class="container mt-4">
        <div class="card p-4">
            <h4 class="text-primary">{{ subject }} Test</h4>
            <p class="text-muted">Class: {{ class_id }}</p>
            <hr>
            <div class="mb-4">
                <p><b>Q1. Which one is a programming language?</b></p>
                <div class="form-check"><input class="form-check-input" type="radio" name="q1" value="10"> Python</div>
                <div class="form-check"><input class="form-check-input" type="radio" name="q1" value="0"> Snake</div>
            </div>
            <button onclick="finishExam()" class="btn btn-primary w-100 btn-custom">Finish Exam</button>
        </div>
    </div>

    <div id="ad-box" style="display:none;" class="container mt-5 text-center">
        <div class="card p-5">
            <h4 class="text-success">Submitting your response...</h4>
            <p>Please wait <b id="timer">5</b> seconds.</p>
            
            <div class="ad-container">
                <!-- ADSTERRA BANNER -->
                <script type="text/javascript">
                    atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
                </script>
                <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
            </div>
        </div>
    </div>

    <script>
    function finishExam() {
        document.getElementById('quiz-box').style.display = 'none';
        document.getElementById('ad-box').style.display = 'block';
        let count = 5;
        let countdown = setInterval(() => {
            count--;
            document.getElementById('timer').innerText = count;
            if (count <= 0) {
                clearInterval(countdown);
                saveScore();
            }
        }, 1000);
    }

    function saveScore() {
        fetch('/save_result', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                score: 10,
                subject: '{{ subject }}',
                class_name: '{{ class_id }}'
            })
        }).then(() => {
            window.location.href = '/dashboard';
        });
    }
    </script>
    """, class_id=class_id, subject=subject)

@app.route('/save_result', methods=['POST'])
@login_required
def save_result():
    data = request.json
    new_res = Result(user_id=current_user.id, score=data['score'], subject=data['subject'], class_name=data['class_name'])
    db.session.add(new_res)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/logout')
def logout(): logout_user(); return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
  
