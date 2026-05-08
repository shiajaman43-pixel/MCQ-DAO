import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'direct-access-no-auth'

# --- UI Layout ---
UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
    .card { border-radius: 15px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .btn-main { background: #00b894; color: white; padding: 25px; font-size: 22px; font-weight: bold; border-radius: 15px; transition: 0.3s; width: 100%; border: none; }
    .btn-main:hover { background: #55efc4; transform: scale(1.02); }
    .ad-container { min-height: 250px; display: flex; align-items: center; justify-content: center; }
    .hidden { display: none; }
    .timer-text { font-size: 50px; font-weight: bold; color: #d63031; }
</style>
"""

# --- Routes ---

@app.route('/')
def main_tab():
    # Prothomei Main Tab jekhane ek konay ba upore ad thakbe
    return render_template_string(UI_STYLE + """
    <div class="container mt-3">
        <!-- Corner Ad Slot -->
        <div class="text-center mb-4">
             <script type="text/javascript">
                atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
             </script>
             <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
        </div>

        <div class="text-center" style="margin-top: 40px;">
            <button onclick="startPrep()" class="btn-main shadow-lg">TEST MY PREPARATION</button>
        </div>

        <!-- 3 Sec Ad Overlay -->
        <div id="ad-overlay" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:80px;">
            <h3>Preparing Your Test...</h3>
            <div class="timer-text" id="timer3">3</div>
            <div class="ad-container">
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
        <div class="card p-4">
            <h3 class="text-center mb-4">Choice Class & Subject</h3>
            <label>Select Class:</label>
            <select class="form-select mb-3"><option>Class 6</option><option>Class 7</option><option>Class 9</option><option>Class 10</option></select>
            <label>Select Subject:</label>
            <select class="form-select mb-4"><option>Mathematics</option><option>Science</option><option>ICT</option><option>English</option></select>
            <button onclick="window.location.href='/exam'" class="btn btn-primary w-100 p-3">Start MCQ Now</button>
        </div>
    </div>
    """)

@app.route('/exam')
def exam():
    return render_template_string(UI_STYLE + """
    <div class="container mt-4">
        <div id="q-box" class="card p-4">
            <h4 class="text-primary">MCQ Test Started</h4>
            <hr>
            <div class="mb-3">
                <p><b>1. What is the capital of Bangladesh?</b></p>
                <input type="radio" name="q1"> Dhaka <br>
                <input type="radio" name="q1"> Khulna
            </div>
            <button onclick="submitExam()" class="btn btn-success mt-4 w-100 p-3">Submit Exam</button>
        </div>

        <!-- 5 Sec Ad Overlay -->
        <div id="result-ad" class="hidden text-center mt-3">
            <h3>Generating Result...</h3>
            <div class="timer-text" id="timer5">5</div>
            <div class="ad-container">
                <script type="text/javascript">
                    atOptions = { 'key' : 'e0fe653541837054d29ca1be1eb04acc', 'format' : 'iframe', 'height' : 300, 'width' : 160, 'params' : {} };
                </script>
                <script type="text/javascript" src="https://www.highperformanceformat.com/e0fe653541837054d29ca1be1eb04acc/invoke.js"></script>
            </div>
        </div>
    </div>
    <script>
    function submitExam() {
        document.getElementById('q-box').classList.add('hidden');
        document.getElementById('result-ad').classList.remove('hidden');
        let c = 5;
        let t = setInterval(() => {
            c--; document.getElementById('timer5').innerText = c;
            if(c <= 0) { clearInterval(t); window.location.href = '/result'; }
        }, 1000);
    }
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(UI_STYLE + """
    <div class="container mt-5 text-center">
        <div class="card p-5">
            <h1 class="text-success">Finished!</h1>
            <p class="fs-4">You have successfully completed the test.</p>
            <div class="alert alert-info">Your Score: 10/10</div>
            <a href="/" class="btn btn-dark w-100 p-3">Take Another Test</a>
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run(debug=True)
  
