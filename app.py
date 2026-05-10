import random
import json
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- ADSTERRA & SMARTLINKS ---
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_728": """<div style="text-align:center; margin:20px 0;">
                        <script type="text/javascript">
                            atOptions = {'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};
                        </script>
                        <script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
                     </div>""",
    "SMARTLINK_1": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2",
    "SMARTLINK_2": "https://potterynaggingformerly.com/j0qft5iu?key=8e026f89e2d58ed640105a21f55908c6"
}

# --- DATABASE HANDLER ---
DB_FILE = 'quiz_db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        # Default empty structure for 5 subjects
        initial = {f"{sub}_ch{i}": [] for sub in ['ICT', 'Bangla', 'English', 'Math', 'Science'] for i in range(1, 6)}
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial, f)
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- CSS & HEAD (FIXED SYNTAX) ---
def get_header():
    return f"""
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {AD_CONFIG['POP_UNDER']}
    {AD_CONFIG['SOCIAL_BAR']}
    <style>
        :root {{ --primary: #5f27cd; --secondary: #341f97; }}
        body {{ background: #f0f3f7; font-family: 'Segoe UI', sans-serif; }}
        .hero {{ background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 40px 0; border-radius: 0 0 30px 30px; text-align: center; }}
        .main-card {{ background: white; border-radius: 20px; padding: 25px; margin-top: -30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
        .btn-earn {{ background: #ff9f43; color: white; border: none; padding: 12px; border-radius: 10px; width: 100%; font-weight: bold; margin-bottom: 15px; }}
        .q-box {{ background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 6px solid var(--primary); }}
        .opt {{ display: block; background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; cursor: pointer; border: 1px solid #ddd; }}
        .opt:hover {{ background: #efefff; border-color: var(--primary); }}
    </style>
    """

# --- ROUTES ---

@app.route('/')
def home():
    db = load_db()
    return render_template_string(get_header() + f"""
    <div class="hero">
        <h2 class="fw-bold">SSC MODEL TEST PRO</h2>
        <div class="badge bg-light text-dark p-2">Credits: <span id="cr_val">0</span></div>
    </div>
    <div class="container" style="max-width: 550px;">
        <div class="main-card">
            {AD_CONFIG['BANNER_728']}
            <button onclick="earn()" class="btn-earn shadow-sm">GET 100 CREDITS (AD)</button>
            
            <form action="/exam">
                <label class="small fw-bold text-muted">SELECT SUBJECT:</label>
                <select name="ch" class="form-select mb-4 mt-1">
                    {% for key in keys %}
                    <option value="{{key}}">{{ key.replace('_', ' ').upper() }} ({{db[key]|length}} Qs)</option>
                    {% endfor %}
                </select>
                <button type="button" onclick="start(this.form)" class="btn btn-primary w-100 p-3 fw-bold rounded-3">UNLOCK EXAM (50 Cr)</button>
            </form>
        </div>
    </div>
    <script>
        let cr = localStorage.getItem('user_credits') || 0;
        document.getElementById('cr_val').innerText = cr;
        function earn() {{
            window.open('{AD_CONFIG['SMARTLINK_1']}', '_blank');
            localStorage.setItem('user_credits', parseInt(cr) + 100);
            location.reload();
        }}
        function start(f) {{
            if(cr >= 50) {{
                localStorage.setItem('user_credits', cr - 50);
                f.submit();
            }} else alert("Not enough credits!");
        }}
    </script>
    """, keys=db.keys(), db=db)

@app.route('/exam')
def exam():
    ch = request.args.get('ch')
    db = load_db()
    questions = db.get(ch, [])
    if not questions: return "No questions! <a href='/admin'>Add Questions</a>"
    
    selected = random.sample(questions, min(len(questions), 30))
    q_html = ""
    for i, q_data in enumerate(selected):
        options = q_data[1:] # A, W1, W2, W3
        correct = q_data[1]
        random.shuffle(options)
        
        q_html += f'<div class="q-box shadow-sm"><h5>{i+1}. {q_data[0]}</h5>'
        for o in options:
            q_html += f'<label class="opt"><input type="radio" name="q{i}" value="{o}" data-ans="{correct}"> {o}</label>'
        q_html += '</div>'
        if (i+1) % 5 == 0: q_html += AD_CONFIG['BANNER_728']

    return render_template_string(get_header() + f"""
    <div class="bg-white sticky-top p-2 border-bottom shadow-sm">
        <div class="container d-flex justify-content-between align-items-center">
            <b>{ch.upper()}</b>
            <div id="timer" class="text-danger fw-bold">30:00</div>
            <button onclick="submit()" class="btn btn-sm btn-success">Finish</button>
        </div>
    </div>
    <div class="container mt-4" style="max-width: 750px;">
        {q_html}
        <button onclick="submit()" class="btn btn-primary w-100 p-3 mb-5">SUBMIT ANSWERS</button>
    </div>
    <script>
        let t = 1800;
        setInterval(() => {{
            t--;
            let m=Math.floor(t/60), s=t%60;
            document.getElementById('timer').innerText = m+":"+(s<10?'0'+s:s);
            if(t<=0) submit();
        }}, 1000);

        function submit() {{
            let score = 0;
            document.querySelectorAll('.q-box').forEach(b => {{
                let s = b.querySelector('input:checked');
                if(s && s.value === s.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('score', score);
            window.open('{AD_CONFIG['SMARTLINK_2']}', '_blank');
            setTimeout(() => location.href='/result', 800);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(get_header() + f"""
    <div class="container mt-5 text-center">
        <div class="main-card py-5 shadow mx-auto" style="max-width: 450px;">
            <h4 class="text-muted">YOUR RESULT</h4>
            <h1 class="display-2 fw-bold text-primary" id="sc">0</h1>
            {AD_CONFIG['BANNER_728']}
            <button onclick="window.open('{AD_CONFIG['SMARTLINK_2']}')" class="btn btn-dark w-100 mb-3">CLAIM REWARD (AD)</button>
            <a href="/" class="btn btn-outline-primary w-100">Try Again</a>
        </div>
    </div>
    <script>document.getElementById('sc').innerText = localStorage.getItem('score') + "/30";</script>
    """)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = load_db()
    if request.method == 'POST':
        ch = request.form.get('ch')
        raw = request.form.get('data')
        for line in raw.strip().split('\n'):
            p = line.split('|')
            if len(p) == 5: db[ch].append([i.strip() for i in p])
        save_db(db)
        return "Success! <a href='/admin'>Back</a>"
    return render_template_string(get_header() + """
    <div class="container mt-5" style="max-width: 700px;">
        <div class="main-card">
            <h3>Admin Panel</h3>
            <form method="POST">
                <select name="ch" class="form-select mb-3">
                    {% for k in keys %}<option value="{{k}}">{{k}}</option>{% endfor %}
                </select>
                <textarea name="data" class="form-control mb-3" rows="8" placeholder="Q | Correct | Wrong1 | Wrong2 | Wrong3"></textarea>
                <button type="submit" class="btn btn-success w-100">Upload Questions</button>
            </form>
            <a href="/" class="d-block mt-3 text-center">Go Home</a>
        </div>
    </div>
    """, keys=db.keys())

if __name__ == '__main__':
    app.run(debug=True)
