import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'max-revenue-setup-2026'

# --- UI & High-Revenue Ad Scripts ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 1. POPUNDER AD SCRIPT (Top Priority) -->
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f8f9fa; font-family: 'Segoe UI', sans-serif; padding-bottom: 50px; }
    .card { border-radius: 15px; border: none; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
    .btn-main { background: linear-gradient(135deg, #6c5ce7, #00cec9); color: white; padding: 20px; font-size: 20px; border-radius: 12px; width: 100%; border: none; font-weight: bold; transition: 0.3s; }
    .btn-main:hover { transform: translateY(-2px); opacity: 0.9; }
    .native-ad-box { background: #fff; padding: 15px; border-radius: 12px; margin: 20px 0; border: 1px solid #eee; text-align: center; }
    .hidden { display: none; }
    .timer-text { font-size: 60px; font-weight: 800; color: #ff7675; }
    .question-card { margin-bottom: 15px; padding: 15px; background: #fff; border-radius: 10px; border-left: 5px solid #6c5ce7; }
</style>
"""

# --- Native Ad Component ---
NATIVE_AD_HTML = """
<div class="native-ad-box">
    <small class="text-muted d-block mb-2">Sponsored Content</small>
    <!-- NATIVE AD SCRIPT -->
    <script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
    <div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
</div>
"""

@app.route('/')
def main_tab():
    return render_template_string(UI_STYLE + f"""
    <div class="container mt-4 text-center">
        <h2 class="fw-bold text-dark">Quick Prep Portal</h2>
        
        {NATIVE_AD_HTML}

        <div style="margin-top: 40px;">
            <button onclick="startPrep()" class="btn-main shadow-lg">🚀 TEST MY PREPARATION</button>
            <p class="text-muted mt-3 small">Click to start your MCQ challenge</p>
        </div>

        <!-- 3 Sec Wait Overlay -->
        <div id="ad-overlay" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:80px;">
            <h4>Preparing Questions...</h4>
            <div class="timer-text" id="timer3">3</div>
            {NATIVE_AD_HTML}
        </div>
    </div>
    <script>
    function startPrep() {{
        document.getElementById('ad-overlay').classList.remove('hidden');
        let c = 3;
        let t = setInterval(() => {{
            c--; document.getElementById('timer3').innerText = c;
            if(c <= 0) {{ clearInterval(t); window.location.href = '/choice'; }}
        }}, 1000);
    }}
    </script>
    """)

@app.route('/choice')
def choice():
    return render_template_string(UI_STYLE + """
    <div class="container mt-5">
        <div class="card p-4 text-center">
            <h4 class="mb-4">Select Subject</h4>
            <div class="d-grid gap-2">
                <button onclick="window.location.href='/exam'" class="btn btn-outline-primary p-3 fw-bold">Class 10 - ICT Exam</button>
                <button class="btn btn-outline-secondary p-3 disabled">More Subjects Coming...</button>
            </div>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    questions = [
        "1. Computer-er brain kake bola hoy?", "2. HTML-er purno rup ki?", 
        "3. WWW-er ortho ki?", "4. RAM ki dhoroner memory?", 
        "5. 1 KB = koto Byte?", "6. Binary-te digit koyti?", 
        "7. Facebook-er protishthata ke?", "8. Google ki?", 
        "9. Nicher konti Input device?", "10. Software koy dhoroner?"
    ]
    q_html = "".join([f'<div class="question-card"><b>{q}</b><br><div class="mt-2"><input type="radio" name="r{i}"> Option A &nbsp; <input type="radio" name="r{i}"> Option B</div></div>' for i, q in enumerate(questions)])

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-3">
        <div id="quiz-ui">
            <h4 class="text-center mb-4">ICT Preparation Test</h4>
            {q_html}
            <button onclick="submitExam()" class="btn btn-success w-100 p-3 mb-5 fw-bold">SUBMIT ANSWERS</button>
        </div>

        <!-- 5 Sec Result Overlay -->
        <div id="result-ad" class="hidden text-center mt-5" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; padding-top:50px;">
            <h3 class="text-primary">Calculating Score...</h3>
            <div class="timer-text" id="timer5">5</div>
            {NATIVE_AD_HTML}
        </div>
    </div>
    <script>
    function submitExam() {{
        document.getElementById('quiz-ui').classList.add('hidden');
        document.getElementById('result-ad').classList.remove('hidden');
        let c = 5;
        let t = setInterval(() => {{
            c--; document.getElementById('timer5').innerText = c;
            if(c <= 0) {{ clearInterval(t); window.location.href = '/result'; }}
        }}, 1000);
    }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(UI_STYLE + f"""
    <div class="container mt-5 text-center">
        <div class="card p-5 shadow">
            <h1 class="display-4 text-success fw-bold">10 / 10</h1>
            <p class="lead">Excellent Performance!</p>
            <hr>
            {NATIVE_AD_HTML}
            <a href="/" class="btn btn-dark btn-lg w-100 mt-4">Take Another Test</a>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run()
  
