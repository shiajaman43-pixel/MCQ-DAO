import random
import json
import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# --- ADSTERRA & SMARTLINKS (UPDATED) ---
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_728": """<div class="ad-container" style="text-align:center; margin:20px 0;">
                        <script type="text/javascript">
                            atOptions = {'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};
                        </script>
                        <script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
                     </div>""",
    "SMARTLINK_1": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2",
    "SMARTLINK_2": "https://potterynaggingformerly.com/j0qft5iu?key=8e026f89e2d58ed640105a21f55908c6"
}

# --- DATABASE HANDLER ---
DB_FILE = 'ssc_master_db.json'

def init_db():
    subjects = ['ICT', 'Bangla', 'English', 'Math', 'Science']
    default_db = {}
    for sub in subjects:
        for i in range(1, 6):
            default_db[f"{sub}_ch{i}"] = []
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_db, f)
    return default_db

def load_db():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- CSS STYLES ---
STYLE = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{AD_CONFIG['POP_UNDER']}
{AD_CONFIG['SOCIAL_BAR']}
<style>
    :root {{ --primary: #6c5ce7; --secondary: #a29bfe; --dark: #2d3436; }}
    body {{ background: #f9f9fb; font-family: 'SolaimanLipi', sans-serif; }}
    .hero-section {{ background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 60px 0; border-radius: 0 0 50px 50px; text-align: center; }}
    .card-custom {{ border-radius: 20px; border: none; box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: 0.3s; }}
    .btn-main {{ background: var(--primary); color: white; border-radius: 12px; padding: 12px; font-weight: bold; border: none; width: 100%; }}
    .btn-earn {{ background: #ff7675; color: white; border-radius: 12px; font-weight: bold; padding: 12px; width: 100%; border: none; margin-bottom: 15px; }}
    .q-card {{ background: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; border-left: 6px solid var(--primary); }}
    .opt-label {{ display: block; background: #f1f2f6; padding: 15px; margin: 10px 0; border-radius: 10px; cursor: pointer; border: 2px solid transparent; transition: 0.2s; }}
    .opt-label:hover {{ background: #e0e0ff; border-color: var(--primary); }}
    .sticky-timer {{ position: sticky; top: 0; background: white; z-index: 1000; padding: 15px; border-bottom: 2px solid #eee; }}
</style>
"""

# --- ROUTES ---

@app.route('/')
def home():
    db = load_db()
    return render_template_string(STYLE + f"""
    <div class="hero-section">
        <h1 class="fw-bold">SSC EXAM MASTER 2026</h1>
        <p>Prepare yourself with 30-MCQ Challenges</p>
        <div class="badge bg-white text-dark p-2 px-4 rounded-pill">
            <i class="fas fa-coins text-warning"></i> Credits: <span id="cr_val">0</span>
        </div>
    </div>

    <div class="container" style="max-width: 600px; margin-top: -40px;">
        <div class="card card-custom p-4 bg-white">
            {AD_CONFIG['BANNER_728']}
            <button onclick="addCredits()" class="btn-earn shadow-sm">
                <i class="fas fa-bolt"></i> GET 100 FREE CREDITS (AD)
            </button>
            
            <form action="/exam" method="GET">
                <label class="fw-bold text-muted mb-2">Select Subject & Chapter:</label>
                <select name="ch" class="form-select mb-4" style="border-radius: 12px; height: 50px;">
                    {% for key in db_keys %}
                    <option value="{{key}}">{{ key.replace('_', ' ').upper() }} (Qs: {{db[key]|length}})</option>
                    {% endfor %}
                </select>
                <button type="button" onclick="checkCr(this.form)" class="btn-main shadow">
                    <i class="fas fa-play-circle"></i> START MISSION (50 Cr)
                </button>
            </form>
            <div class="text-center mt-3">
                <a href="/admin" class="text-muted text-decoration-none small">Admin Dashboard</a>
            </div>
        </div>
    </div>

    <script>
        let credits = localStorage.getItem('user_credits') || 0;
        document.getElementById('cr_val').innerText = credits;

        function addCredits() {{
            window.open('{AD_CONFIG['SMARTLINK_1']}', '_blank');
            credits = parseInt(credits) + 100;
            localStorage.setItem('user_credits', credits);
            document.getElementById('cr_val').innerText = credits;
            alert("100 Credits Added!");
        }}

        function checkCr(form) {{
            if(credits >= 50) {{
                localStorage.setItem('user_credits', credits - 50);
                form.submit();
            }} else {{
                alert("Insufficient Credits! Please click the red button.");
            }}
        }}
    </script>
    """, db_keys=db.keys(), db=db)

@app.route('/exam')
def exam():
    ch = request.args.get('ch')
    db = load_db()
    questions = db.get(ch, [])
    
    if len(questions) < 1:
        return "<h3>No questions found! Add them from admin.</h3><a href='/admin'>Admin</a>"

    # Select 30 random or max available
    selected = random.sample(questions, min(len(questions), 30))
    
    processed_qs = []
    for q_data in selected:
        options = q_data[1:] # Correct + 3 Wrongs
        correct = q_data[1]
        random.shuffle(options)
        processed_qs.append({'q': q_data[0], 'options': options, 'correct': correct})

    q_html = ""
    for i, q in enumerate(processed_qs):
        q_html += f"""
        <div class="q-card shadow-sm">
            <h5 class="fw-bold mb-3">{i+1}. {q['q']}</h5>
            {"".join([f'<label class="opt-label"><input type="radio" name="q{i}" value="{o}" data-ans="{q["correct"]}"> {o}</label>' for o in q['options']])}
        </div>
        """
        # Inject Banner Ad every 5 questions
        if (i+1) % 5 == 0:
            q_html += AD_CONFIG['BANNER_728']

    return render_template_string(STYLE + f"""
    <div class="sticky-timer shadow-sm">
        <div class="container d-flex justify-content-between align-items-center">
            <span class="fw-bold text-primary"><i class="fas fa-book"></i> {ch.replace('_',' ')}</span>
            <div id="timer" class="fw-bold text-danger fs-5">30:00</div>
            <button onclick="finishExam()" class="btn btn-dark btn-sm rounded-pill px-3">Finish</button>
        </div>
    </div>

    <div class="container mt-4" style="max-width: 800px;">
        {q_html}
        <button onclick="finishExam()" class="btn-main mb-5 shadow-lg py-3">SUBMIT FINAL ANSWERS</button>
    </div>

    <script>
        let time = 1800;
        setInterval(() => {{
            time--;
            let m = Math.floor(time/60);
            let s = time%60;
            document.getElementById('timer').innerText = `${{m}}:${{s<10?'0'+s:s}}`;
            if(time <= 0) finishExam();
        }}, 1000);

        function finishExam() {{
            let score = 0;
            document.querySelectorAll('.q-card').forEach(card => {{
                let selected = card.querySelector('input:checked');
                if(selected && selected.value === selected.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('last_score', score);
            window.open('{AD_CONFIG['SMARTLINK_2']}', '_blank');
            setTimeout(() => window.location.href = '/result', 800);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 500px;">
        <div class="card card-custom p-5">
            <h3 class="fw-bold text-muted">EXAM COMPLETED</h3>
            <h1 class="display-1 fw-bold text-primary" id="final_sc">0</h1>
            <p class="mb-4">Great job! Keep practicing to improve.</p>
            {AD_CONFIG['BANNER_728']}
            <button onclick="window.open('{AD_CONFIG['SMARTLINK_2']}')" class="btn-main mb-3">
                <i class="fas fa-file-download"></i> DOWNLOAD CERTIFICATE (AD)
            </button>
            <a href="/" class="btn btn-outline-secondary w-100 p-3 rounded-4 fw-bold">Try Another Subject</a>
        </div>
    </div>
    <script>
        document.getElementById('final_sc').innerText = localStorage.getItem('last_score') + "/30";
    </script>
    """)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = load_db()
    if request.method == 'POST':
        ch = request.form.get('ch')
        raw_text = request.form.get('bulk_data')
        lines = raw_text.strip().split('\n')
        count = 0
        for line in lines:
            p = line.split('|')
            if len(p) == 5:
                db[ch].append([i.strip() for i in p])
                count += 1
        save_db(db)
        return f"<div style='text-align:center; padding:50px;'><h3>Added {count} Questions!</h3><a href='/admin'>Go Back</a></div>"

    return render_template_string(STYLE + """
    <div class="container mt-5">
        <div class="card card-custom p-4 bg-white" style="max-width: 800px; margin: auto;">
            <h2 class="fw-bold text-primary"><i class="fas fa-user-shield"></i> Admin Panel</h2>
            <hr>
            <form method="POST">
                <label class="fw-bold mb-2">Target Chapter:</label>
                <select name="ch" class="form-select mb-3">
                    {% for key in db_keys %}
                    <option value="{{key}}">{{key}}</option>
                    {% endfor %}
                </select>
                
                <label class="fw-bold mb-2">Paste Questions (Format below):</label>
                <div class="alert alert-secondary small">
                    Question | Correct Ans | Wrong 1 | Wrong 2 | Wrong 3
                </div>
                <textarea name="bulk_data" class="form-control mb-3" rows="10" placeholder="Dhaka is capital of? | Bangladesh | India | Pakistan | Nepal"></textarea>
                
                <button type="submit" class="btn btn-success w-100 p-3 fw-bold">SAVE TO DATABASE</button>
            </form>
            <a href="/" class="mt-3 d-block text-center text-muted">Go to Homepage</a>
        </div>
    </div>
    """, db_keys=db.keys())

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
