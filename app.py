import random
import json
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- ADSTERRA & CONFIG ---
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_728": '<div style="text-align:center; margin:15px 0;"><script type="text/javascript">atOptions = {"key" : "3ba591d1fc0f098ac02b41fdd3ceb0c5","format" : "iframe","height" : 90,"width" : 728,"params" : {}};</script><script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script></div>',
    "SMARTLINK_1": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2",
    "SMARTLINK_2": "https://potterynaggingformerly.com/j0qft5iu?key=8e026f89e2d58ed640105a21f55908c6"
}

DB_FILE = 'ssc_data_v2.json'

def load_db():
    if not os.path.exists(DB_FILE):
        default_data = {f"{s}_ch{i}": [] for s in ['ICT', 'Bangla', 'English', 'Math', 'Science'] for i in range(1, 6)}
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f)
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- UI COMPONENTS ---
LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSC Exam Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {{ pop_under|safe }}
    {{ social_bar|safe }}
    <style>
        body { background: #f4f7f6; font-family: sans-serif; }
        .hero { background: #6c5ce7; color: white; padding: 30px 0; text-align: center; border-radius: 0 0 20px 20px; }
        .card-main { background: white; border-radius: 15px; padding: 20px; margin-top: -20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .q-card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #6c5ce7; }
        .opt-btn { display: block; padding: 10px; margin: 5px 0; background: #f8f9fa; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; }
        .opt-btn:hover { background: #e9ecef; }
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def home():
    db = load_db()
    content = """
    <div class="hero">
        <h2>SSC Exam Master</h2>
        <div class="badge bg-warning text-dark">Credits: <span id="cr_display">0</span></div>
    </div>
    <div class="container" style="max-width: 500px;">
        <div class="card-main">
            {{ banner|safe }}
            <button onclick="earnCr()" class="btn btn-danger w-100 mb-3 fw-bold">GET 100 FREE CREDITS</button>
            <form action="/exam">
                <label class="fw-bold small">Select Subject & Chapter:</label>
                <select name="ch" class="form-select mb-3">
                    {% for key in keys %}
                    <option value="{{key}}">{{ key.replace('_', ' ').upper() }} ({{ db[key]|length }} Qs)</option>
                    {% endfor %}
                </select>
                <button type="button" onclick="checkCr(this.form)" class="btn btn-primary w-100">Start Exam (50 Cr)</button>
            </form>
            <hr><a href="/admin" class="text-muted small">Admin Dashboard</a>
        </div>
    </div>
    <script>
        let credits = parseInt(localStorage.getItem('user_credits') || 0);
        document.getElementById('cr_display').innerText = credits;
        function earnCr() {
            window.open('{{ sl1|safe }}', '_blank');
            localStorage.setItem('user_credits', credits + 100);
            location.reload();
        }
        function checkCr(form) {
            if(credits >= 50) {
                localStorage.setItem('user_credits', credits - 50);
                form.submit();
            } else { alert('Not enough credits! Click the red button.'); }
        }
    </script>
    """
    return render_template_string(LAYOUT, content=content, keys=db.keys(), db=db, 
                                 pop_under=AD_CONFIG['POP_UNDER'], social_bar=AD_CONFIG['SOCIAL_BAR'],
                                 banner=AD_CONFIG['BANNER_728'], sl1=AD_CONFIG['SMARTLINK_1'])

@app.route('/exam')
def exam():
    ch = request.args.get('ch')
    db = load_db()
    raw_qs = db.get(ch, [])
    if not raw_qs: return "No questions! <a href='/admin'>Add Questions</a>"
    
    selected = random.sample(raw_qs, min(len(raw_qs), 30))
    final_qs = []
    for q in selected:
        opts = q[1:]
        correct = q[1]
        random.shuffle(opts)
        final_qs.append({'q': q[0], 'opts': opts, 'ans': correct})

    content = """
    <div class="bg-white p-2 sticky-top border-bottom shadow-sm">
        <div class="container d-flex justify-content-between">
            <span class="fw-bold text-primary">Time: <span id="timer">30:00</span></span>
            <button onclick="finish()" class="btn btn-sm btn-success">Submit</button>
        </div>
    </div>
    <div class="container mt-4" style="max-width: 700px;">
        {% for q in final_qs %}
            <div class="q-card shadow-sm">
                <h6>{{ loop.index }}. {{ q.q }}</h6>
                {% for o in q.opts %}
                <label class="opt-btn">
                    <input type="radio" name="q{{ loop.index0 }}" value="{{ o }}" data-ans="{{ q.ans }}"> {{ o }}
                </label>
                {% endfor %}
            </div>
            {% if loop.index % 5 == 0 %}{{ banner|safe }}{% endif %}
        {% endfor %}
        <button onclick="finish()" class="btn btn-primary w-100 p-3 mb-5">SUBMIT FINAL ANSWERS</button>
    </div>
    <script>
        let t = 1800;
        setInterval(() => {
            t--; let m=Math.floor(t/60), s=t%60;
            document.getElementById('timer').innerText = m+":"+(s<10?'0'+s:s);
            if(t<=0) finish();
        }, 1000);
        function finish() {
            let score = 0;
            document.querySelectorAll('.q-card').forEach(card => {
                let sel = card.querySelector('input:checked');
                if(sel && sel.value === sel.getAttribute('data-ans')) score++;
            });
            localStorage.setItem('last_score', score);
            window.open('{{ sl2|safe }}', '_blank');
            setTimeout(() => { location.href='/result'; }, 800);
        }
    </script>
    """
    return render_template_string(LAYOUT, content=content, final_qs=final_qs, banner=AD_CONFIG['BANNER_728'], sl2=AD_CONFIG['SMARTLINK_2'])

@app.route('/result')
def result():
    content = """
    <div class="container mt-5 text-center" style="max-width: 450px;">
        <div class="card-main py-5">
            <h4 class="text-muted">SCORE</h4>
            <h1 class="display-1 fw-bold text-primary" id="sc_val">0</h1>
            {{ banner|safe }}
            <button onclick="window.open('{{ sl2|safe }}')" class="btn btn-dark w-100 mb-3">GET CERTIFICATE (AD)</button>
            <a href="/" class="btn btn-outline-primary w-100">Back Home</a>
        </div>
    </div>
    <script>document.getElementById('sc_val').innerText = localStorage.getItem('last_score') + "/30";</script>
    """
    return render_template_string(LAYOUT, content=content, banner=AD_CONFIG['BANNER_728'], sl2=AD_CONFIG['SMARTLINK_2'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = load_db()
    if request.method == 'POST':
        ch = request.form.get('ch')
        data = request.form.get('data')
        for line in data.strip().split('\n'):
            p = line.split('|')
            if len(p) == 5: db[ch].append([i.strip() for i in p])
        save_db(db)
        return "Saved! <a href='/admin'>Back</a>"
    
    content = """
    <div class="container mt-4" style="max-width: 600px;">
        <div class="card-main">
            <h3>Admin Panel</h3>
            <form method="POST">
                <select name="ch" class="form-select mb-3">
                    {% for k in keys %}<option value="{{k}}">{{k}}</option>{% endfor %}
                </select>
                <textarea name="data" class="form-control mb-3" rows="10" placeholder="Question | Correct | Wrong 1 | Wrong 2 | Wrong 3"></textarea>
                <button class="btn btn-success w-100">Bulk Upload</button>
            </form>
            <a href="/" class="d-block mt-3 text-center">Home</a>
        </div>
    </div>
    """
    return render_template_string(LAYOUT, content=content, keys=db.keys())

if __name__ == '__main__':
    app.run(debug=True)
