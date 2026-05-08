import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'popunder-mcq-10-fix'

# --- UI Layout & Scripts ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Popunder Ad Script -->
<script src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>

<style>
    body { background: #f0f2f5; font-family: 'Segoe UI', sans-serif; padding-bottom: 50px; }
    .card { border-radius: 15px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 20px; }
    .btn-main { background: #0984e3; color: white; padding: 25px; font-size: 22px; font-weight: bold; border-radius: 15px; width: 100%; border: none; }
    .btn-main:hover { background: #74b9ff; }
    .hidden { display: none; }
    .timer-text { font-size: 50px; font-weight: bold; color: #d63031; }
    .question-block { border-bottom: 1px solid #eee; padding: 15px 0; }
</style>
"""

# --- Routes ---

@app.route('/')
def main_tab():
    return render_template_string(UI_STYLE + """
    <div class="container mt-3">
        <!-- Banner Ad Slot -->
        <div class="text-center mb-4">
             <script type="text/javascript">
                atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
             </script>
             <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>

        <div class="text-center" style="margin-top: 40px;">
            <button onclick="startPrep()" class="btn-main shadow-lg">TEST MY PREPARATION</button>
        </div>

        <div id="ad-overlay" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:80px;">
            <h3>Preparing Your Test...</h3>
            <div class="timer-text" id="timer3">3</div>
            <p>Wait for a moment</p>
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
            <h3>Choose Category</h3>
            <select class="form-select mb-3"><option>Class 10 - ICT</option></select>
            <button onclick="window.location.href='/exam'" class="btn btn-primary w-100 p-3">Start MCQ (10 Questions)</button>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    questions = [
        "1. Computer er brain kake bola hoy?",
        "2. HTML er purno rup ki?",
        "3. WWW mane ki?",
        "4. RAM ki dhoroner memory?",
        "5. 1 Kilobyte = koto byte?",
        "6. Binary paddhatite koyti digita thake?",
        "7. Facebook er founder ke?",
        "8. Google ki?",
        "9. Nicher konti Input device?",
        "10. Software koy dhoroner?"
    ]
    
    q_html = ""
    for idx, q in enumerate(questions):
        q_html += f"""
        <div class="question-block">
            <p><b>{q}</b></p>
            <input type="radio" name="q{idx}"> Option A &nbsp;&nbsp;
            <input type="radio" name="q{idx}"> Option B
        </div>
        """

    return render_template_string(UI_STYLE + f"""
    <div class="container">
        <div id="q-box" class="card p-4">
            <h4 class="text-center">ICT Preparation Test</h4>
            <hr>
            {q_html}
            <button onclick="submitExam()" class="btn btn-success mt-4 w-100 p-3">Submit Answers</button>
        </div>

        <div id="result-ad" class="hidden text-center mt-5">
            <h3>Calculating Your Score...</h3>
            <div class="timer-text" id="timer5">5</div>
            <!-- Banner Ad during wait -->
             <script type="text/javascript">
                atOptions = {{ 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {{}} }};
             </script>
             <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
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
            <h1 class="text-success">Excellent!</h1>
            <p class="fs-4">Your Score: 10 / 10</p>
            <div class="mt-4">
                <a href="/" class="btn btn-outline-dark">Back to Home</a>
            </div>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run()
  
