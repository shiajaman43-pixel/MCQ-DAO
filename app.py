import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
# Apnar Smartlink ekhane bosiye din
SMARTLINK_URL = "https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js" 

UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 1. POPUNDER SCRIPT -->
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f1f3f6; font-family: 'Segoe UI', sans-serif; position: relative; }
    
    /* TRICK: Invisible Layer for Popunder & Smartlink Trigger */
    #ad-trigger-layer {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: 9999; background: rgba(0,0,0,0); cursor: pointer;
    }

    .card { border-radius: 15px; border: none; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .btn-main { background: linear-gradient(135deg, #0984e3, #6c5ce7); color: white; padding: 22px; font-size: 22px; font-weight: bold; border-radius: 15px; width: 100%; border: none; }
    .hidden { display: none; }
    .timer-text { font-size: 60px; font-weight: 800; color: #d63031; }
    .native-box { background: #fff; padding: 15px; border-radius: 12px; border: 1px solid #ddd; margin: 15px 0; }
</style>
"""

# --- NATIVE AD COMPONENT ---
NATIVE_AD = """
<div class="native-box text-center">
    <small class="text-muted d-block mb-2">Recommended Content</small>
    <script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
    <div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
</div>
"""

@app.route('/')
def main_tab():
    return render_template_string(UI_STYLE + f"""
    <div id="ad-trigger-layer" onclick="this.style.display='none';"></div>

    <div class="container mt-4 text-center">
        <h3 class="fw-bold mb-4">Preparation Test Portal</h3>
        {NATIVE_AD}

        <div style="margin-top: 40px;">
            <button onclick="startPrep()" class="btn-main shadow-lg">🚀 START PREPARATION</button>
            <p class="text-muted mt-3 small">Double click if it doesn't start</p>
        </div>

        <div id="loading" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:10000; text-align:center; padding-top:100px;">
            <h3>Loading Secure Server...</h3>
            <div class="timer-text" id="timer3">3</div>
            {NATIVE_AD}
        </div>
    </div>

    <script>
    function startPrep() {{
        // Forcefully try to open Smartlink in new tab
        window.open('{SMARTLINK_URL}', '_blank');

        document.getElementById('loading').classList.remove('hidden');
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
    <div class="container mt-5 text-center">
        <div class="card p-4">
            <h4>Select Category</h4>
            <button onclick="window.location.href='/exam'" class="btn btn-outline-primary mt-3 p-3 fw-bold">Class 10 - ICT Exam</button>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    questions = [
        "1. Computer-er brain kake bola hoy?", "2. HTML-er purno rup ki?", 
        "3. WWW mane ki?", "4. RAM ki dhoroner memory?", 
        "5. 1 Kilobyte = koto byte?", "6. Binary-te digit koyti?", 
        "7. Facebook-er founder ke?", "8. Google ki?", 
        "9. Nicher konti Input device?", "10. Software koy dhoroner?"
    ]
    q_html = "".join([f'<div class="card p-3"><b>{q}</b><br><input type="radio" name="q{i}"> Option A &nbsp; <input type="radio" name="q{i}"> Option B</div>' for i, q in enumerate(questions)])

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-3">
        <div id="quiz-ui">
            {q_html}
            <button onclick="submitExam()" class="btn btn-success w-100 p-3 mb-5 fw-bold">SUBMIT ANSWERS</button>
        </div>

        <div id="result-ad" class="hidden text-center mt-5" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:10000; padding-top:50px;">
            <h3>Processing Result...</h3>
            <div class="timer-text" id="timer5">5</div>
            {NATIVE_AD}
        </div>
    </div>

    <script>
    function submitExam() {{
        // Resulter ageo abr smartlink open korar cheshta
        window.open('{SMARTLINK_URL}', '_blank');

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
            <h1 class="text-success fw-bold">Score: 10/10</h1>
            <p class="lead">Congratulations!</p>
            {NATIVE_AD}
            <a href="/" class="btn btn-dark w-100 p-3 mt-3">Take Another Test</a>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run()
  
