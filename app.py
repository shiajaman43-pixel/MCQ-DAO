import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
# Apnar deya latest Smartlink
SMARTLINK_URL = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2" 

UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- POPUNDER SCRIPT -->
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f8f9fa; font-family: 'Segoe UI', sans-serif; position: relative; }
    
    /* Invisible Layer Trick for maximum clicks */
    #ad-trigger-layer {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: 9999; background: rgba(0,0,0,0); cursor: pointer;
    }

    .card { border-radius: 15px; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .btn-main { background: linear-gradient(45deg, #6c5ce7, #00b894); color: white; padding: 20px; font-size: 22px; font-weight: bold; border-radius: 15px; width: 100%; border: none; transition: 0.3s; }
    .btn-main:hover { transform: scale(1.02); filter: brightness(1.1); }
    .hidden { display: none; }
    .timer-text { font-size: 65px; font-weight: 800; color: #ff7675; }
    .native-box { background: #fff; padding: 15px; border-radius: 12px; border: 1px solid #ddd; margin: 15px 0; min-height: 100px; }
</style>
"""

# --- NATIVE AD COMPONENT ---
NATIVE_AD = """
<div class="native-box text-center">
    <small class="text-muted d-block mb-2">Advertisement</small>
    <script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
    <div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
</div>
"""

@app.route('/')
def main_tab():
    return render_template_string(UI_STYLE + f"""
    <div id="ad-trigger-layer" onclick="this.style.display='none';"></div>

    <div class="container mt-5 text-center">
        <h2 class="fw-bold text-primary">Student Prep Center</h2>
        {NATIVE_AD}

        <div style="margin-top: 50px;">
            <button onclick="startPrep()" class="btn-main shadow">🚀 START MY PREPARATION</button>
            <p class="text-muted mt-3">Click to unlock your 10-question test</p>
        </div>

        <div id="loading" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:10000; text-align:center; padding-top:100px;">
            <h3>Initializing Secure Test...</h3>
            <div class="timer-text" id="timer3">3</div>
            {NATIVE_AD}
        </div>
    </div>

    <script>
    function startPrep() {{
        // Opening your latest Smartlink
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
        <div class="card p-5">
            <h4 class="mb-4">Select Your Grade</h4>
            <button onclick="window.location.href='/exam'" class="btn btn-outline-dark p-3 fw-bold w-100 mb-3">Class 10 ICT - Final Prep</button>
            <p class="text-muted">More subjects available soon!</p>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    questions = [
        "1. Computer-er brain kake bola hoy?", "2. HTML-er purno rup ki?", 
        "3. WWW-er purno rup ki?", "4. RAM ki dhoroner memory?", 
        "5. 1 Kilobyte = koto byte?", "6. Binary-te digit koyti?", 
        "7. Facebook-er founder ke?", "8. Google ki?", 
        "9. Nicher konti Input device?", "10. Software koy dhoroner?"
    ]
    q_html = "".join([f'<div class="card p-3"><b>{q}</b><br><div class="mt-2"><input type="radio" name="q{i}"> Answer A &nbsp; <input type="radio" name="q{i}"> Answer B</div></div>' for i, q in enumerate(questions)])

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-3">
        <div id="quiz-ui">
            <h4 class="text-center mb-4 text-success">ICT Preparation Test</h4>
            {q_html}
            <button onclick="submitExam()" class="btn btn-success w-100 p-3 mb-5 fw-bold shadow">GET MY RESULT</button>
        </div>

        <div id="result-ad" class="hidden text-center mt-5" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:10000; padding-top:50px;">
            <h3>Analyzing Your Performance...</h3>
            <div class="timer-text" id="timer5">5</div>
            {NATIVE_AD}
        </div>
    </div>

    <script>
    function submitExam() {{
        // Smartlink trigger again on submit for double revenue
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
            <h1 class="display-3 text-success fw-bold">10 / 10</h1>
            <p class="lead">Great Job! You've passed the test.</p>
            <hr>
            {NATIVE_AD}
            <a href="/" class="btn btn-dark w-100 p-3 mt-4">Retake Test</a>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run()
