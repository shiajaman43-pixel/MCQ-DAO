import random
import json
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- ADSTERRA CONFIG (এখানে আপনার কোড বসান) ---
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_728": """<div style="margin:20px 0; text-align:center;"><script type="text/javascript">atOptions = {'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script></div>""",
    "SMARTLINK_1": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2",
    "SMARTLINK_2": "https://potterynaggingformerly.com/j0qft5iu?key=8e026f89e2d58ed640105a21f55908c6"
}

# --- DATABASE LOGIC ---
DB_FILE = 'ssc_data.json'
def load_db():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {'ict': [], 'math': [], 'english': [], 'bangla': [], 'science': []}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

# --- ROUTES ---

@app.route('/')
def home():
    db = load_db()
    return render_template_string(f"""
    <html>
    <head>
        <title>SSC Model Test</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {AD_CONFIG['POP_UNDER']}
        {AD_CONFIG['SOCIAL_BAR']}
    </head>
    <body class="bg-light text-center">
        <div class="p-5 bg-primary text-white">
            <h1>SSC Digital Exam Pro</h1>
            <p>Credits: <span id="cr">0</span></p>
        </div>
        <div class="container mt-4" style="max-width:500px;">
            {AD_CONFIG['BANNER_728']}
            <button onclick="getCr()" class="btn btn-warning w-100 mb-3 fw-bold">GET 100 CREDITS (AD)</button>
            
            <form action="/exam" class="card p-4 shadow border-0">
                <label class="mb-2 fw-bold">Select Subject:</label>
                <select name="ch" class="form-select mb-3">
                    {% for key in keys %}
                    <option value="{{key}}">{{key.upper()}} (Qs: {{data[key]|length}})</option>
                    {% endfor %}
                </select>
                <button type="submit" class="btn btn-primary">Start Exam (50 Cr)</button>
            </form>
            <br>
            <a href="/admin" class="text-muted small">Admin Panel</a>
        </div>
        <script>
            function getCr() {{ 
                window.open('{AD_CONFIG["SMARTLINK_1"]}', '_blank');
                let c = parseInt(localStorage.getItem('user_credits') || 0);
                localStorage.setItem('user_credits', c + 100);
                location.reload();
            }}
            document.getElementById('cr').innerText = localStorage.getItem('user_credits') || 0;
        </script>
    </body>
    </html>
    """, keys=db.keys(), data=db)

@app.route('/exam')
def exam():
    sub = request.args.get('ch')
    db = load_db()
    raw_qs = db.get(sub, [])
    if not raw_qs: return "No questions found! Go to admin."
    
    # ৩০টি র‍্যান্ডম প্রশ্ন এবং অপশন র‍্যান্ডমাইজ
    sampled = random.sample(raw_qs, min(len(raw_qs), 30))
    final_qs = []
    for q in sampled:
        options = q[1:]
        random.shuffle(options)
        final_qs.append({'q': q[0], 'opt': options, 'ans': q[1]})

    q_html = ""
    for i, q in enumerate(final_qs):
        q_html += f'<div class="card p-3 mb-3 text-start"><h5>{i+1}. {q["q"]}</h5>'
        for o in q['opt']:
            q_html += f'<label class="d-block p-2 border rounded mt-2"><input type="radio" name="q{i}" value="{o}" data-ans="{q["ans"]}"> {o}</label>'
        q_html += '</div>'
        if (i+1) % 5 == 0: q_html += AD_CONFIG['BANNER_728']

    return render_template_string(f"""
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light p-4">
        <div class="container" style="max-width:800px;">
            {q_html}
            <button onclick="finish()" class="btn btn-success w-100 p-3">SUBMIT EXAM</button>
        </div>
        <script>
            function finish() {{
                let score = 0;
                document.querySelectorAll('.card').forEach(c => {{
                    let sel = c.querySelector('input:checked');
                    if(sel && sel.value === sel.getAttribute('data-ans')) score++;
                }});
                localStorage.setItem('last_score', score);
                window.open('{AD_CONFIG["SMARTLINK_2"]}', '_blank');
                setTimeout(() => location.href='/result', 1000);
            }}
        </script>
    </body>
    </html>
    """)

@app.route('/result')
def result():
    return render_template_string(f"""
    <div style="text-align:center; padding:100px;">
        <h1>Your Score: <span id="s"></span>/30</h1>
        {AD_CONFIG['BANNER_728']}
        <button onclick="window.open('{AD_CONFIG['SMARTLINK_2']}')" class="btn btn-dark">Get Certificate</button>
        <br><br>
        <a href="/">Back to Home</a>
    </div>
    <script>document.getElementById('s').innerText = localStorage.getItem('last_score');</script>
    """)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = load_db()
    if request.method == 'POST':
        sub = request.form.get('sub')
        raw = request.form.get('data')
        lines = raw.strip().split('\n')
        for line in lines:
            parts = line.split('|')
            if len(parts) == 5: db[sub].append([p.strip() for p in parts])
        save_db(db)
        return "Saved! <a href='/admin'>Back</a>"
    return render_template_string("""
    <form method="POST" style="padding:50px;">
        <select name="sub">{% for k in keys %}<option value="{{k}}">{{k}}</option>{% endfor %}</select><br>
        <textarea name="data" style="width:100%; height:300px;" placeholder="Q | A | W1 | W2 | W3"></textarea><br>
        <button type="submit">Upload</button>
    </form>
    """, keys=db.keys())

if __name__ == '__main__':
    app.run(debug=True)
