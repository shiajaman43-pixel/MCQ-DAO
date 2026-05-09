import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- AGGRESSIVE AD CONFIGURATION ---
SMARTLINK_URL = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f0f2f5; font-family: 'Lexend', sans-serif; }
    #ad-trigger-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999; background: rgba(0,0,0,0); cursor: pointer; }
    .card { border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 15px; overflow: hidden; }
    .header-box { background: linear-gradient(135deg, #1e3799, #0984e3); color: white; padding: 25px; border-radius: 0 0 20px 20px; }
    .btn-action { background: #00b894; color: white; padding: 18px; font-size: 1.2rem; font-weight: 700; border-radius: 50px; width: 100%; border: none; transition: 0.3s; margin-top: 20px; }
    .btn-action:hover { background: #009473; transform: translateY(-2px); }
    .timer-circle { font-size: 70px; font-weight: 900; color: #d63031; }
    .hidden { display: none; }
    .native-slot { background: #ffffff; border: 2px dashed #0984e3; border-radius: 10px; margin: 20px 0; min-height: 120px; position: relative; }
    .question-title { color: #2d3436; font-weight: 600; font-size: 1.1rem; }
</style>
"""

NATIVE_AD = """
<div class="native-slot">
    <script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
    <div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
</div>
"""

@app.route('/')
def index():
    return render_template_string(UI_STYLE + f"""
    <div id="ad-trigger-layer" onclick="this.style.display='none';"></div>
    <div class="header-box text-center shadow">
        <h1>Digital ICT Mock Test</h1>
        <p>Prepare for Board Exams with Real Questions</p>
    </div>
    
    <div class="container mt-4 text-center">
        {NATIVE_AD}
        <div class="card p-4">
            <h4>Instructions:</h4>
            <ul class="text-start small text-muted">
                <li>10 Multiple Choice Questions.</li>
                <li>Wait for result processing to earn certificate.</li>
            </ul>
            <button onclick="startFlow()" class="btn-action shadow">🚀 START MOCK TEST</button>
        </div>
        {NATIVE_AD}
    </div>

    <div id="loading" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:10000; text-align:center; padding-top:150px;">
        <h2 class="text-primary">Securing Connection...</h2>
        <div class="timer-circle" id="timer3">3</div>
        <p>Please wait for ad verification</p>
        {NATIVE_AD}
    </div>

    <script>
    function startFlow() {{
        window.open('{SMARTLINK_URL}', '_blank');
        document.getElementById('loading').classList.remove('hidden');
        let c = 3;
        let t = setInterval(() => {{
            c--; document.getElementById('timer3').innerText = c;
            if(c <= 0) {{ clearInterval(t); window.location.href = '/exam'; }}
        }}, 1000);
    }}
    </script>
    """)

@app.route('/exam')
def exam():
    # Real Internet Based ICT Questions
    questions = [
        ["Internet-er 'Father' kake bola hoy?", "Vint Cerf", "Charles Babbage"],
        ["Nicher konti ekti Search Engine noy?", "Bing", "Facebook"],
        ["URL-er purno rup ki?", "Uniform Resource Locator", "Universal Radio Link"],
        ["IP Address koyti bit diye toiri?", "32 bit", "64 bit"],
        ["E-mail-er jonok ke?", "Ray Tomlinson", "Bill Gates"],
        ["HTML-e boro header lekhar tag konti?", "<h1>", "<h6>"],
        ["Modem ki dhoroner device?", "Input/Output", "Only Input"],
        ["1 Terabyte = koto Gigabyte?", "1024 GB", "1000 GB"],
        ["Web page design-e konti bebohar hoy?", "CSS", "C++"],
        ["Bangladesh-e 4G seba kobe chalu hoy?", "2018", "2015"]
    ]
    
    q_html = ""
    for i, q in enumerate(questions):
        q_html += f"""
        <div class="card p-3">
            <p class="question-title">{i+1}. {q[0]}</p>
            <div class="d-flex justify-content-around">
                <label><input type="radio" name="q{i}"> {q[1]}</label>
                <label><input type="radio" name="q{i}"> {q[2]}</label>
            </div>
        </div>
        """
        if i == 4: q_html += NATIVE_AD # Add Ad in the middle of questions

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-3">
        <h4 class="text-center text-primary mb-4">Board Standard ICT MCQ</h4>
        <div id="exam-ui">
            {q_html}
            {NATIVE_AD}
            <button onclick="submitFlow()" class="btn-action shadow mb-5">✅ SUBMIT & GET RESULT</button>
        </div>

        <div id="processing" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:10000; text-align:center; padding-top:100px;">
            <h2 class="text-success">Analyzing Score...</h2>
            <div class="timer-circle" id="timer5">5</div>
            <p>Verification In Progress</p>
            {NATIVE_AD}
        </div>
    </div>

    <script>
    function submitFlow() {{
        window.open('{SMARTLINK_URL}', '_blank');
        document.getElementById('exam-ui').classList.add('hidden');
        document.getElementById('processing').classList.remove('hidden');
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
        <div class="card p-5 shadow-lg">
            <h1 class="text-success fw-bold display-1">90%</h1>
            <h3 class="mt-3">Performance: Excellent</h3>
            <p class="text-muted">You are ready for the final exam!</p>
            <hr>
            {NATIVE_AD}
            <button onclick="window.location.href='/'" class="btn btn-dark w-100 p-3 mt-3">Retake Exam</button>
        </div>
        <div class="mt-4">
            {NATIVE_AD}
        </div>
    </div>
    <script>
    // Triple Trigger: Open ad when user views result
    window.onload = function() {{
        setTimeout(() => {{ window.open('{SMARTLINK_URL}', '_blank'); }}, 2000);
    }};
    </script>
    """)

if __name__ == '__main__':
    app.run()
