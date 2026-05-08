import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'max-ads-pop-10-mcq'

# --- UI Layout & High-Revenue Ad Scripts ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- PRIMARY POPUNDER SCRIPT (Har-waqt click e ad ashbe) -->
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding-bottom: 60px; }
    .card { border-radius: 20px; border: none; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 25px; }
    .btn-main { background: linear-gradient(135deg, #0984e3, #6c5ce7); color: white; padding: 25px; font-size: 22px; font-weight: bold; border-radius: 15px; width: 100%; border: none; transition: 0.3s; }
    .btn-main:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4); }
    .hidden { display: none; }
    .timer-text { font-size: 60px; font-weight: 800; color: #ff7675; }
    .question-block { background: #fff; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #6c5ce7; }
    .option-label { cursor: pointer; display: block; padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-top: 5px; }
    .option-label:hover { background: #f1f2f6; }
</style>
"""

# --- Routes ---

@app.route('/')
def main_tab():
    return render_template_string(UI_STYLE + """
    <div class="container mt-4 text-center">
        <!-- Banner Ad -->
        <div style="min-height: 250px;">
             <script type="text/javascript">
                atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
             </script>
             <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>

        <div style="margin-top: 50px;">
            <button onclick="startPrep()" class="btn-main">🚀 START PREPARATION TEST</button>
            <p class="text-muted mt-3">Click anywhere to start</p>
        </div>

        <!-- 3 Sec Full Screen Ad Overlay -->
        <div id="ad-overlay" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
            <h2 class="mb-4">Loading Questions...</h2>
            <div class="timer-text" id="timer3">3</div>
            <div class="mt-5">
                <!-- Adsterra Banner inside Loading -->
                <script type="text/javascript">
                    atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
                </script>
                <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
            </div>
        </div>
    </div>
    <script>
    function startPrep() {
        document.getElementById('ad-overlay').classList.remove('hidden');
        let c = 3;
        let t = setInterval(() => {
            c--; document.getElementById('timer3').innerText = c;
            if(c <= 0) { clearInterval(t); window.location.href = '/choice'; }
        }, 1000);
    }
    </script>
    """)

@app.route('/choice')
def choice():
    return render_template_string(UI_STYLE + """
    <div class="container mt-5">
        <div class="card p-4 text-center">
            <h3 class="mb-4">Select Subject</h3>
            <div class="d-grid gap-3">
                <button onclick="window.location.href='/exam'" class="btn btn-outline-primary p-3">Class 10 - ICT Exam</button>
                <button onclick="window.location.href='/exam'" class="btn btn-outline-primary p-3 text-muted">Class 9 - Science (Coming Soon)</button>
            </div>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    questions = [
        "1. Computer er brain kake bola hoy?", "2. HTML er purno rup ki?", 
        "3. WWW mane ki?", "4. RAM ki dhoroner memory?", 
        "5. 1 Kilobyte = koto byte?", "6. Binary paddhatite digit koyti?", 
        "7. Facebook er founder ke?", "8. Google ki?", 
        "9. Nicher konti Input device?", "10. Software koy dhoroner?"
    ]
    
    q_html = ""
    for idx, q in enumerate(questions):
        q_html += f"""
        <div class="question-block">
            <p class="fw-bold">{q}</p>
            <label class="option-label"><input type="radio" name="q{idx}"> Answer A</label>
            <label class="option-label"><input type="radio" name="q{idx}"> Answer B</label>
        </div>
        """

    return render_template_string(UI_STYLE + f"""
    <div class="container">
        <div id="q-box">
            <div class="card p-3 mb-4 text-center bg-primary text-white">
                <h4>ICT Test (10 Questions)</h4>
            </div>
            {q_html}
            <button onclick="submitExam()" class="btn btn-success mt-4 w-100 p-3 mb-5 fw-bold">SUBMIT ANSWERS</button>
        </div>

        <!-- 5 Sec Result Ad Overlay -->
        <div id="result-ad" class="hidden text-center mt-5" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; padding-top:50px;">
            <h2 class="text-primary">Analyzing Results...</h2>
            <div class="timer-text" id="timer5">5</div>
            <div class="mt-4">
                 <script type="text/javascript">
                    atOptions = {{ 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {{}} }};
                 </script>
                 <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
            </div>
        </div>
    </div>
    <script>
    function submitExam() {{
        document.getElementById('q-box').classList.add('hidden');
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
    return render_template_string(UI_STYLE + """
    <div class="container mt-5 text-center">
        <div class="card p-5">
            <div class="mb-3">✅</div>
            <h1 class="text-success fw-bold">Test Completed!</h1>
            <p class="fs-4">You Scored: <span class="badge bg-success">10 / 10</span></p>
            <hr>
            <a href="/" class="btn btn-dark btn-lg w-100 mt-3">Restart Test</a>
            <p class="mt-4 text-muted small">Ads help us keep this site free!</p>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run()
  
