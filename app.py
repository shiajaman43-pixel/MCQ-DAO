import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mobile-mcq-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mcq_site.db'
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

# --- HTML Templates with Mobile Responsive Design (Bootstrap) ---

COMMON_HEAD = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background-color: #f8f9fa; }
    .card { border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .btn-custom { border-radius: 10px; padding: 10px 20px; font-weight: bold; }
</style>
"""

REGISTER_HTML = COMMON_HEAD + """
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-11 col-md-4 card p-4 bg-white">
            <h3 class="text-center mb-4">Account Khulun</h3>
            <form method="POST">
                <input name="phone" class="form-control mb-3" placeholder="Phone Number" required>
                <input type="password" name="password" class="form-control mb-3" placeholder="Password" required>
                <button type="submit" class="btn btn-success w-100 btn-custom">Register</button>
            </form>
            <p class="text-center mt-3">Account ache? <a href="/login">Login</a></p>
        </div>
    </div>
</div>
"""

LOGIN_HTML = COMMON_HEAD + """
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-11 col-md-4 card p-4 bg-white">
            <h3 class="text-center mb-4">Login</h3>
            <form method="POST">
                <input name="phone" class="form-control mb-3" placeholder="Phone Number" required>
                <input type="password" name="password" class="form-control mb-3" placeholder="Password" required>
                <button type="submit" class="btn btn-primary w-100 btn-custom">Login</button>
            </form>
            <p class="text-center mt-3">Notun user? <a href="/register">Register</a></p>
        </div>
    </div>
</div>
"""

DASHBOARD_HTML = COMMON_HEAD + """
<nav class="navbar navbar-dark bg-primary p-3">
    <span class="navbar-brand mb-0 h1">MCQ Portal</span>
    <a href="/logout" class="btn btn-outline-light btn-sm">Logout</a>
</nav>
<div class="container mt-4">
    <div class="card p-3 mb-4">
        <h5>Shagotom, {{ current_user.phone }}</h5>
    </div>
    
    <h5 class="mb-3">Test Shuru Korun:</h5>
    <div class="d-grid gap-2 mb-4">
        <a href="/quiz/6/General-Science" class="btn btn-outline-primary btn-lg">Class 6 Science</a>
        <a href="/quiz/10/Mathematics" class="btn btn-outline-primary btn-lg">Class 10 Math</a>
    </div>

    <h5>Apnar Result History:</h5>
    <div class="table-responsive">
        <table class="table table-striped card">
            <thead class="table-dark">
                <tr><th>Class</th><th>Subject</th><th>Score</th></tr>
            </thead>
            <tbody>
                {% for res in results %}
                <tr><td>{{ res.class_name }}</td><td>{{ res.subject }}</td><td>{{ res.score }}</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
"""

QUIZ_HTML = COMMON_HEAD + """
<div id="quiz-ui" class="container mt-4">
    <div class="card p-4">
        <h4 class="text-primary">{{ subject }} (Class {{ class_id }})</h4>
        <hr>
        <div class="p-3 bg-light rounded border mb-4">
            <p><b>Q1. Python ki dhoroner language?</b></p>
            <div class="form-check">
              <input class="form-check-input" type="radio" name="q1" value="10" id="opt1">
              <label class="form-check-label" for="opt1">High Level</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" name="q1" value="0" id="opt2">
              <label class="form-check-label" for="opt2">Low Level</label>
            </div>
        </div>
        <button onclick="startTimer()" class="btn btn-warning btn-lg btn-custom w-100">Submit Test</button>
    </div>
</div>

<div id="ad-div" style="display:none;" class="container mt-5 text-center">
    <div class="card p-5 border-danger">
        <h3 class="text-danger">Result Processing...</h3>
        <div class="display-1 fw-bold my-3" id="timer">5</div>
        <p>Please wait for 5 seconds</p>
        
        <div class="mt-4 p-2 border">
            <!-- ADSTERRA BANNER CODE START -->
            <script type="text/javascript">
              atOptions = {
                'key' : 'e0fe653541837054d29ca1be1eb04acc',
                'format' : 'iframe',
                'height' : 300,
                'width' : 160,
                'params' : {}
              };
            </script>
            <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
            <!-- ADSTERRA BANNER CODE END -->
        </div>
    </div>
</div>

<script>
function startTimer() {
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

# --- Baki Logic Agertai Thakbe ---

@app.route('/')
def index():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone, password = request.form.get('phone'), request.form.get('password')
        if User.query.filter_by(phone=phone).first(): return "Phone exists!"
        db.session.add(User(phone=phone, password=generate_password_hash(password, method='pbkdf2:sha256')))
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
    return jsonify({"status": "ok"})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)
