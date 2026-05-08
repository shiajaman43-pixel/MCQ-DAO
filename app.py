import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mcq-secret-key-2026'
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

# --- HTML Templates (Inline) ---

REGISTER_HTML = """
<div style="font-family:sans-serif; text-align:center; margin-top:50px;">
    <h2>Register (Class 6-10 MCQ)</h2>
    <form method="POST">
        <input name="phone" placeholder="Phone Number" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit" style="background:green; color:white; padding:10px; border:none; cursor:pointer;">Create Account</button>
    </form>
    <p>Already have an account? <a href="/login">Login</a></p>
</div>
"""

LOGIN_HTML = """
<div style="font-family:sans-serif; text-align:center; margin-top:50px;">
    <h2>Login</h2>
    <form method="POST">
        <input name="phone" placeholder="Phone Number" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit" style="background:blue; color:white; padding:10px; border:none; cursor:pointer;">Login</button>
    </form>
    <p>New user? <a href="/register">Register</a></p>
</div>
"""

DASHBOARD_HTML = """
<div style="font-family:sans-serif; padding:20px;">
    <h2>Dashboard - Welcome {{ current_user.phone }}</h2>
    <a href="/logout" style="color:red;">Logout</a>
    <hr>
    <h3>Select Class to Start Test:</h3>
    <a href="/quiz/6/General-Science">Class 6 Science</a> | <a href="/quiz/10/Mathematics">Class 10 Math</a>
    <hr>
    <h3>Your History:</h3>
    <table border="1" width="100%" style="border-collapse: collapse;">
        <tr style="background:#f2f2f2;"><th>Class</th><th>Subject</th><th>Score</th></tr>
        {% for res in results %}
        <tr><td>{{ res.class_name }}</td><td>{{ res.subject }}</td><td>{{ res.score }}</td></tr>
        {% endfor %}
    </table>
</div>
"""

QUIZ_HTML = """
<div style="font-family:sans-serif; padding:20px; max-width:600px; margin:auto;" id="quiz-div">
    <h2>{{ subject }} Test - Class {{ class_id }}</h2>
    <hr>
    <div style="background:#f9f9f9; padding:15px; border-radius:10px;">
        <p><b>Q1. Python ki dhoroner language?</b></p>
        <input type="radio" name="q1" value="10"> High Level <br>
        <input type="radio" name="q1" value="0"> Low Level <br><br>
    </div>
    <br>
    <button onclick="startTimer()" style="background:orange; color:white; padding:12px 20px; border:none; cursor:pointer; font-weight:bold;">Submit Test</button>
</div>

<!-- Adsterra Overlay Screen -->
<div id="ad-div" style="display:none; text-align:center; padding:30px; font-family:sans-serif;">
    <h2>Result Processing...</h2>
    <p style="font-size:30px; color:red; font-weight:bold;" id="timer">5</p>
    
    <div style="display:inline-block; margin-top:20px; border:1px solid #ddd; padding:10px;">
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

<script>
function startTimer() {
    document.getElementById('quiz-div').style.display = 'none';
    document.getElementById('ad-div').style.display = 'block';
    let count = 5;
    let x = setInterval(function() {
        count--;
        document.getElementById('timer').innerHTML = count;
        if (count <= 0) {
            clearInterval(x);
            // Automaticaly result save korbe
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

ADMIN_HTML = """
<div style="font-family:sans-serif; padding:20px;">
    <h2>Admin Panel - All Student Performance</h2>
    <table border="1" width="100%" style="border-collapse: collapse;">
        <tr style="background:#333; color:white;"><th>Phone</th><th>Class</th><th>Subject</th><th>Score</th></tr>
        {% for res, user in data %}
        <tr><td>{{ user.phone }}</td><td>{{ res.class_name }}</td><td>{{ res.subject }}</td><td>{{ res.score }}</td></tr>
        {% endfor %}
    </table>
</div>
"""

# --- Routes Logic ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        if User.query.filter_by(phone=phone).first():
            return "Phone number already exists!"
        new_user = User(phone=phone, password=generate_password_hash(password, method='pbkdf2:sha256'))
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
        return "Invalid login credentials!"
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
    new_res = Result(user_id=current_user.id, score=data['score'], subject=data['subject'], class_name=data['class_name'])
    db.session.add(new_res)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route('/admin')
@login_required
def admin():
    # Admin check manually database e 'admin' role dile hbe
    if current_user.role != 'admin': return "Access Denied!"
    data = db.session.query(Result, User).join(User).all()
    return render_template_string(ADMIN_HTML, data=data)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
