import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mobile-mcq-secure-key-2026'
# Database file path setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mcq_site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Database Models ---
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

# --- CSS & JS (Mobile Responsive) ---
COMMON_HEAD = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background-color: #f1f3f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .card-mobile { border-radius: 20px; border: none; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .btn-main { border-radius: 12px; padding: 12px; font-weight: 600; transition: 0.3s; }
</style>
"""

# --- Templates ---

LOGIN_HTML = COMMON_HEAD + """
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-11 col-md-4 card-mobile card p-4 bg-white">
            <h3 class="text-center mb-4 text-primary">Login</h3>
            <form method="POST">
                <div class="mb-3"><input name="phone" class="form-control" placeholder="Phone Number" required></div>
                <div class="mb-3"><input type="password" name="password" class="form-control" placeholder="Password" required></div>
                <button type="submit" class="btn btn-primary w-100 btn-main">Sign In</button>
            </form>
            <p class="text-center mt-3 text-muted">Don't have an account? <a href="/register" class="text-decoration-none">Register</a></p>
        </div>
    </div>
</div>
"""

REGISTER_HTML = COMMON_HEAD + """
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-11 col-md-4 card-mobile card p-4 bg-white">
            <h3 class="text-center mb-4 text-success">Create Account</h3>
            <form method="POST">
                <div class="mb-3"><input name="phone" class="form-control" placeholder="Phone Number" required></div>
                <div class="mb-3"><input type="password" name="password" class="form-control" placeholder="Password" required></div>
                <button type="submit" class="btn btn-success w-100 btn-main">Register Now</button>
            </form>
            <p class="text-center mt-3 text-muted">Already registered? <a href="/login" class="text-decoration-none">Login</a></p>
        </div>
    </div>
</div>
"""

DASHBOARD_HTML = COMMON_HEAD + """
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="text-dark">Dashboard</h4>
        <a href="/logout" class="btn btn-danger btn-sm">Logout</a>
    </div>
    <div class="card p-3 mb-4 card-mobile bg-primary text-white">
        <p class="mb-1">Student Phone:</p>
        <h3>{{ current_user.phone }}</h3>
    </div>
    <h6 class="mb-3 fw-bold">SELECT YOUR CLASS:</h6>
    <div class="d-grid gap-2">
        <a href="/quiz/6/General-Science" class="btn btn-white bg-white btn-main shadow-sm text-start">📚 Class 6 - Science</a>
        <a href="/quiz/10/Math" class="btn btn-white bg-white btn-main shadow-sm text-start">📐 Class 10 - Math</a>
    </div>
    <div class="mt-5">
        <h6 class="fw-bold mb-3">LAST EXAM RESULTS:</h6>
        <div class="table-responsive">
            <table class="table bg-white card-mobile">
                <thead class="table-light"><tr><th>Sub</th><th>Class</th><th>Score</th></tr></thead>
                <tbody>
                    {% for res in results %}
                    <tr><td>{{ res.subject }}</td><td>{{ res.class_name }}</td><td>{{ res.score }}</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
"""

QUIZ_HTML = COMMON_HEAD + """
<div id="quiz-ui" class="container mt-4">
    <div class="card card-mobile p-4">
        <h5 class="text-primary mb-3">{{ subject }} (Class {{ class_id }})</h5>
        <div class="p-3 bg-light rounded border mb-4">
            <p class="mb-3"><b>Q1. Python ki dhoroner language?</b></p>
            <div class="form-check mb-2"><input class="form-check-input" type="radio" name="q1" value="10" id="o1"><label class="form-check-label" for="o1">High Level</label></div>
            <div class="form-check"><input class="form-check-input" type="radio" name="q1" value="0" id="o2"><label class="form-check-label" for="o2">Low Level</label></div>
        </div>
        <button onclick="submitTest()" class="btn btn-primary btn-main w-100 shadow">Finish Exam</button>
    </div>
</div>

<div id="ad-div" style="display:none;" class="container mt-5 text-center">
    <div class="card card-mobile p-5">
        <h3 class="text-primary">Calculating Marks...</h3>
        <div class="display-1 fw-bold text-danger my-3" id="timer">5</div>
        <div class="mt-4">
            <!-- ADSTERRA BANNER -->
            <script type="text/javascript">
              atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
            </script>
            <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>
    </div>
</div>

<script>
function submitTest() {
    document.getElementById('quiz-ui').style.display = 'none';
    document.getElementById('ad-div').style.display = 'block';
    let count = 5;
    let x = setInterval(function() {
        count--;
        document.getElementById('timer').innerHTML = count;
        if (count <= 0) {
            clearInterval(x);
            fetch('/submit_score', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({score: 10, subject: '{{subject}}', class_name: '{{class_id}}'})
            }).then(() => window.location.href = '/dashboard');
        }
    }, 1000);
}
</script>
"""

# --- Logic ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        if User.query.filter_by(phone=phone).first():
            return "Phone already registered!"
        # Simplified Hashing to avoid 500 Error
        hashed_password = generate_password_hash(password)
        new_user = User(phone=phone, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(phone=request.form.get('phone')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        return "Invalid Phone or Password!"
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
@login_required
def dashboard():
    results = Result.query.filter_by(user_id=current_user.id).all()
    return render_template_string(DASHBOARD_HTML, results=results)

@app.route('/quiz/<class_id>/<subject>')
@login_required
def quiz(class_id, subject):
    return render_template_string(QUIZ_HTML, class_id=class_id, subject=subject)

@app.route('/submit_score', methods=['POST'])
@login_required
def submit_score():
    data = request.json
    db.session.add(Result(user_id=current_user.id, score=data['score'], subject=data['subject'], class_name=data['class_name']))
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
