import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD SCRIPTS ---
# আপনার পপ-আন্ডার এবং সোশ্যাল বার স্ক্রিপ্ট এখানে
POP_BAR_SCRIPTS = """
<script src="https://potterynaggingformerly.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>
<script src="https://potterynaggingformerly.com/76/41/5a/76415aaef6ad249973a92bb8f1251a22.js"></script>
"""

BANNER_AD = """
<div style="margin:20px 0; text-align:center;">
    <script type="text/javascript">
        atOptions = { 'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
    </script>
    <script type="text/javascript" src="https://potterynaggingformerly.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
</div>
"""

NATIVE_AD = """
<div style="margin:20px 0;">
    <script async="async" data-cfasync="false" src="https://potterynaggingformerly.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
    <div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
</div>
"""

SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

@app.route('/')
def index():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exam Portal 2026</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {POP_BAR_SCRIPTS}
        <style>
            body {{ background: #f0f2f5; font-family: sans-serif; }}
            .main-card {{ max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
            .btn-earn {{ background: #ff4757; color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; font-weight: bold; margin-bottom: 20px; }}
            .btn-start {{ background: #2ed573; color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; font-weight: bold; }}
            .header-info {{ background: #1e3799; color: white; padding: 20px; border-radius: 15px; margin-bottom: 25px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-card">
                <div class="header-info">
                    <h3>Exam Portal</h3>
                    <p class="m-0">Credits: <span id="cr_display">0</span></p>
                </div>

                <button onclick="getCr()" class="btn-earn">💎 GET 5 CREDITS (ADS)</button>

                <div class="mb-4">
                    <label class="fw-bold mb-2">বিষয় নির্বাচন করুন (Select Subject):</label>
                    <select id="subject_select" class="form-select form-select-lg">
                        <option value="ict">ICT (Information & Tech)</option>
                        <option value="eng">English Grammar</option>
                        <option value="gk">General Knowledge</option>
                    </select>
                </div>

                <button id="start_btn" onclick="goToExam()" class="btn-start w-100" disabled>LOCKED 🔒</button>
                
                {BANNER_AD}
            </div>
        </div>

        <script>
            let current_cr = localStorage.getItem('user_cr') || 0;
            document.getElementById('cr_display').innerText = current_cr;

            if(current_cr >= 5) {{
                document.getElementById('start_btn').disabled = false;
                document.getElementById('start_btn').innerText = "START EXAM (30 MCQ)";
            }}

            function getCr() {{
                window.open('{SMARTLINK_1}', '_blank');
                setTimeout(() => {{
                    localStorage.setItem('user_cr', parseInt(current_cr) + 5);
                    location.reload();
                }}, 2000);
            }}

            function goToExam() {{
                let sub = document.getElementById('subject_select').value;
                localStorage.setItem('user_cr', current_cr - 5);
                window.location.href = '/exam?sub=' + sub;
            }}
        </script>
    </body>
    </html>
    """)

@app.route('/exam')
def exam():
    sub = request.args.get('sub', 'ict')
    
    # সাবজেক্ট অনুযায়ী প্রশ্ন (এখানে আমি ডাটা স্ট্রাকচারটি দেখাচ্ছি)
    ict_qs = [("HTML এর জনক কে?", "টিম বার্নার্স লি", "রে টমলিনসন"), ("IP Address কত বিট?", "৩২ বিট", "১২৮ বিট")] * 15
    eng_qs = [("Which is a Noun?", "Water", "Strong"), ("Opposite of Hot?", "Cold", "Warm")] * 15
    gk_qs = [("বাংলাদেশের রাজধানী?", "ঢাকা", "সিলেট"), ("জাতীয় কবি কে?", "নজরুল", "রবীন্দ্রনাথ")] * 15

    if sub == 'eng': selected_qs = eng_qs
    elif sub == 'gk': selected_qs = gk_qs
    else: selected_qs = ict_qs

    q_list_html = ""
    for i, (q, a, b) in enumerate(selected_qs):
        q_list_html += f"""
        <div class="card p-3 mb-3 shadow-sm">
            <p class="fw-bold">{i+1}. {q}</p>
            <div class="form-check"><input class="form-check-input" type="radio" name="q{i}"> {a}</div>
            <div class="form-check"><input class="form-check-input" type="radio" name="q{i}"> {b}</div>
        </div>
        """
        # প্রতি ৫টি প্রশ্নের পর পর অ্যাড
        if (i+1) % 5 == 0:
            q_list_html += BANNER_AD if (i+1)%10==0 else NATIVE_AD

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {POP_BAR_SCRIPTS}
    </head>
    <body class="bg-light p-3">
        <div class="container" style="max-width: 600px;">
            <div class="sticky-top bg-white p-3 shadow-sm rounded mb-4 text-center">
                <h4 class="m-0 text-primary">Subject: {sub.upper()}</h4>
            </div>
            
            {q_list_html}
            
            <button onclick="finishExam()" class="btn btn-primary w-100 p-3 mb-5 shadow">SUBMIT ANSWERS</button>
        </div>

        <div id="loader" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
            <h3>Analyzing Results...</h3>
            {BANNER_AD}
        </div>

        <script>
            function finishExam() {{
                window.open('{SMARTLINK_2}', '_blank');
                document.getElementById('loader').style.display = 'block';
                setTimeout(() => {{ window.location.href = '/result'; }}, 10000);
            }}
        </script>
    </body>
    </html>
    """)

@app.route('/result')
def result():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {POP_BAR_SCRIPTS}
    </head>
    <body class="text-center p-5 bg-light">
        <div class="card p-5 shadow mx-auto" style="max-width: 500px;">
            <h1 class="text-success">Passed! 🏆</h1>
            <p class="lead">Score: 94%</p>
            {BANNER_AD}
            <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn btn-dark w-100 p-3">DOWNLOAD CERTIFICATE</button>
            <a href="/" class="d-block mt-4">Back to Home</a>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
  
