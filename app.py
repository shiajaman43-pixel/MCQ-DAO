import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'popunder-trick-2026'

# --- UI & High-Revenue Ad Scripts ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- POPUNDER SCRIPT -->
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f4f7f6; font-family: 'Segoe UI', sans-serif; position: relative; min-height: 100vh; }
    
    /* TRICK: Invisible Overlay to force ad on first click */
    #ad-trigger-layer {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 999;
        background: rgba(0,0,0,0); /* Purely invisible */
        cursor: pointer;
    }

    .card { border-radius: 15px; border: none; box-shadow: 0 5px 20px rgba(0,0,0,0.05); z-index: 10; position: relative; }
    .btn-main { background: linear-gradient(135deg, #6c5ce7, #00cec9); color: white; padding: 20px; font-size: 20px; border-radius: 12px; width: 100%; border: none; font-weight: bold; }
    .hidden { display: none; }
    .timer-text { font-size: 60px; font-weight: 800; color: #0984e3; }
    .native-box { background: #fff; padding: 10px; border-radius: 10px; border: 1px solid #ddd; margin: 15px 0; }
</style>
"""

# --- Native Ad Component ---
NATIVE_AD = """
<div class="native-box text-center">
    <small class="text-muted">Recommended</small>
    <script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
    <div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
</div>
"""

@app.route('/')
def main_tab():
    return render_template_string(UI_STYLE + f"""
    <!-- Invisible Layer for Popunder -->
    <div id="ad-trigger-layer" onclick="this.style.display='none'"></div>

    <div class="container mt-4 text-center">
        <h2 class="fw-bold">Exam Preparation</h2>
        {NATIVE_AD}

        <div style="margin-top: 50px;">
            <button onclick="startPrep()" class="btn-main shadow-lg">🚀 START PREPARATION</button>
            <p class="mt-3 text-muted">Click anywhere to begin</p>
        </div>

        <div id="ad-overlay" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
            <h4>Loading Questions...</h4>
            <div class="timer-text" id="timer3">3</div>
            {NATIVE_AD}
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
        <div class="card p-4 text-center shadow">
            <h4>Select Your Class</h4>
            <button onclick="window.location.href='/exam'" class="btn btn-outline-primary mt-3 p-3 fw-bold">Class 10 - ICT Exam</button>
            <button class="btn btn-light mt-2 text-muted" disabled>Class 9 - Science</button>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    questions = ["Computer Brain?", "HTML Full Form?", "What is WWW?", "RAM Type?", "1KB = ?", "Binary Digit?", "FB Founder?", "Google?", "Input Device?", "Software Type?"]
    q_html = "".join([f'<div class="card p-3 mb-3"><b>{i+1}. {q}</b><br><input type="radio"> Option A &nbsp; <input type="radio"> Option B</div>' for i, q in enumerate(questions)])

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-3">
        <div id="quiz-ui">
            {q_html}
            <button onclick="submitExam()" class="btn btn-success w-100 p-3 mb-5 fw-bold">SUBMIT NOW</button>
        </div>

        <div id="result-ad" class="hidden text-center mt-5" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; padding-top:50px;">
            <h3>Processing Result...</h3>
            <div class="timer-text" id="timer5">5</div>
            {NATIVE_AD}
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
        <div class="card p-5">
            <h1 class="text-success fw-bold">Result: 10/10</h1>
            <p>You have passed the ICT exam!</p>
            {NATIVE_AD}
            <hr>
            <a href="/" class="btn btn-dark w-100 p-3">Restart Test</a>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run()
