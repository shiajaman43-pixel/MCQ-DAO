import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- ADSTERRA PRO CONFIGURATION ---
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_728": """<div class="ad-slot"><script type="text/javascript">atOptions = {'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script></div>""",
    "SMARTLINK_1": "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6",
    "SMARTLINK_2": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"
}

# --- MASTER DATABASE (5 SUBJECTS x 5 CHAPTERS) ---
# Courstika স্টাইলে প্রশ্নগুলো সাজানো হয়েছে
DB = {
    # ICT
    'ict_ch1': [("বিশ্বগ্রামের ধারণাটি কার?", "মার্শাল ম্যাকলুহান", "বিল গেটস", "মার্ক জুকারবার্গ", "স্টিভ জবস")] * 30,
    'ict_ch2': [("Bluetooth এর স্ট্যান্ডার্ড কত?", "802.15", "802.11", "802.3", "802.16")] * 30,
    # BANGLA
    'bng_ch1': [("বিভক্তিহীন নাম শব্দকে কী বলে?", "প্রাতিপদিক", "ধাতু", "উপসর্গ", "অনুসর্গ")] * 30,
    'bng_ch2': [("কোনটি তৎপুরুষ সমাস?", "বিপদাপন্ন", "বিনা পানি", "উপগ্রহ", "মহারাজ")] * 30,
    # ENGLISH
    'eng_ch1': [("Identify the Noun form of 'Believe':", "Belief", "Believable", "Believing", "Believes")] * 30,
    'eng_ch2': [("He is ___ FRCS.", "an", "a", "the", "no article")] * 30,
    # MATH
    'math_ch1': [("নিচের কোনটি অমূলদ সংখ্যা?", "√2", "√4", "√9", "√16")] * 30,
    'math_ch2': [("ফাঁকা সেটের উপাদান সংখ্যা কত?", "০", "১", "২", "অসীম")] * 30,
    # SCIENCE
    'sci_ch1': [("রক্তের গ্রুপ কয়টি?", "৪টি", "৩টি", "২টি", "৫টি")] * 30,
    'sci_ch2': [("ভিটামিন সি এর অভাবে কী হয়?", "স্কার্ভি", "রিকেটস", "রাতকানা", "রক্তশূন্যতা")] * 30,
    # ... আপনি প্রতিটি চ্যাপ্টারের লিস্টে আলাদা আলাদা ৩০টি প্রশ্ন কপি-পেস্ট করবেন ...
}

# --- UI & LOGIC ---
STYLE = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{AD_CONFIG['POP_UNDER']}
{AD_CONFIG['SOCIAL_BAR']}
<style>
    :root {{ --primary: #5f27cd; --secondary: #341f97; --accent: #ff9f43; }}
    body {{ background: #f0f3f7; font-family: 'SolaimanLipi', 'Segoe UI', sans-serif; }}
    .nav-custom {{ background: white; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); sticky: top; }}
    .hero-box {{ background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 60px 0; border-radius: 0 0 40px 40px; margin-bottom: 40px; text-align: center; }}
    .main-card {{ background: white; border-radius: 25px; padding: 30px; margin-top: -60px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: none; }}
    .btn-earn {{ background: var(--accent); color: white; border: none; padding: 15px; border-radius: 12px; width: 100%; font-weight: bold; transition: 0.3s; margin-bottom: 20px; }}
    .btn-earn:hover {{ background: #ee5253; transform: scale(1.02); }}
    .q-box {{ background: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; border-left: 8px solid var(--primary); box-shadow: 0 4px 6px rgba(0,0,0,0.02); }}
    .opt-label {{ display: block; background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 10px; cursor: pointer; border: 1px solid #eee; }}
    .opt-label:hover {{ border-color: var(--primary); background: #f1f2f6; }}
    #timer {{ color: #eb4d4b; font-weight: 800; font-size: 1.2rem; }}
</style>
"""

@app.route('/')
def home():
    return render_template_string(STYLE + f"""
    <div class="hero-box">
        <h1 class="fw-bold">SSC MODEL TEST PRO</h1>
        <p class="opacity-75">Courstika Inspired Digital Exam System</p>
        <div class="d-inline-flex bg-white text-dark px-4 py-2 rounded-pill fw-bold">
            <i class="fas fa-coins text-warning me-2"></i> Credits: <span id="cr_val">0</span>
        </div>
    </div>

    <div class="container" style="max-width: 650px;">
        <div class="main-card">
            {AD_CONFIG['BANNER_728']}
            
            <!-- ক্রেডিট ফিক্সড বাটন -->
            <button onclick="addCredits()" class="btn-earn shadow">
                <i class="fas fa-plus-circle"></i> GET 100 CREDITS (OPEN SMARTLINK)
            </button>
            
            <label class="fw-bold text-muted small mb-2">SELECT SUBJECT & CHAPTER:</label>
            <select id="ch_select" class="form-select form-select-lg mb-4" style="border-radius: 15px;">
                <optgroup label="ICT">
                    <option value="ict_ch1">ICT: অধ্যায় ১ (বিশ্বগ্রাম)</option>
                    <option value="ict_ch2">ICT: অধ্যায় ২ (নেটওয়ার্ক)</option>
                </optgroup>
                <optgroup label="BANGLA">
                    <option value="bng_ch1">বাংলা: অধ্যায় ১ (ব্যাকরণ)</option>
                    <option value="bng_ch2">বাংলা: অধ্যায় ২ (সমাস)</option>
                </optgroup>
                <optgroup label="MATH">
                    <option value="math_ch1">গণিত: অধ্যায় ১ (বাস্তব সংখ্যা)</option>
                    <option value="math_ch2">গণিত: অধ্যায় ২ (সেট ও ফাংশন)</option>
                </optgroup>
                <optgroup label="ENGLISH">
                    <option value="eng_ch1">ENGLISH: Chapter 1 (Noun)</option>
                    <option value="eng_ch2">ENGLISH: Chapter 2 (Articles)</option>
                </optgroup>
                <optgroup label="SCIENCE">
                    <option value="sci_ch1">বিজ্ঞান: অধ্যায় ১ (রক্ত)</option>
                    <option value="sci_ch2">বিজ্ঞান: অধ্যায় ২ (ভিটামিন)</option>
                </optgroup>
            </select>
            
            <button onclick="startMission()" class="btn btn-primary w-100 p-3 fw-bold rounded-4 shadow">
                <i class="fas fa-lock-open me-2"></i> UNLOCK EXAM (50 Credits)
            </button>
        </div>
    </div>

    <script>
        // ক্রেডিট লোড এবং সেভ করার নির্ভুল পদ্ধতি
        function updateUI() {{
            let currentCr = localStorage.getItem('user_credits') || 0;
            document.getElementById('cr_val').innerText = currentCr;
        }}
        
        function addCredits() {{
            window.open('{AD_CONFIG['SMARTLINK_1']}', '_blank');
            let cr = parseInt(localStorage.getItem('user_credits') || 0);
            localStorage.setItem('user_credits', cr + 100); // ১০০ ক্রেডিট যোগ
            updateUI();
            alert("১০০ ক্রেডিট সফলভাবে যোগ করা হয়েছে!");
        }}

        function startMission() {{
            let cr = parseInt(localStorage.getItem('user_credits') || 0);
            if(cr >= 50) {{
                localStorage.setItem('user_credits', cr - 50);
                window.location.href = '/exam?ch=' + document.getElementById('ch_select').value;
            }} else {{
                alert("আপনার পর্যাপ্ত ক্রেডিট নেই! 'GET 100 CREDITS' বাটনে ক্লিক করুন।");
            }}
        }}
        
        window.onload = updateUI;
    </script>
    """)

@app.route('/exam')
def exam():
    ch = request.args.get('ch', 'ict_ch1')
    qs = DB.get(ch, [])
    random.shuffle(qs)
    selected_qs = qs[:30] # ৩০টি প্রশ্ন

    q_html = ""
    for i, (q, c, w1, w2, w3) in enumerate(selected_qs):
        opts = [c, w1, w2, w3]
        random.shuffle(opts)
        q_html += f"""
        <div class="q-box">
            <h5 class="fw-bold mb-3">{i+1}. {q}</h5>
            {"".join([f'<label class="opt-label"><input type="radio" name="q{i}" value="{o}" data-ans="{c}"> {o}</label>' for o in opts])}
        </div>
        """
        if (i+1) % 5 == 0: q_html += AD_CONFIG['BANNER_728']

    return render_template_string(STYLE + f"""
    <div class="nav-custom sticky-top">
        <div class="container d-flex justify-content-between align-items-center">
            <span class="fw-bold text-primary">MISSION: {ch.upper()}</span>
            <div id="timer">30:00</div>
            <button onclick="submitTest()" class="btn btn-sm btn-success rounded-pill px-3">FINISH</button>
        </div>
    </div>

    <div class="container mt-4" style="max-width: 800px;">
        {q_html}
        <button onclick="submitTest()" class="btn btn-primary w-100 p-4 rounded-4 mb-5 shadow-lg fw-bold">SUBMIT ALL ANSWERS</button>
    </div>

    <script>
        let seconds = 1800;
        setInterval(() => {{
            seconds--;
            let m = Math.floor(seconds/60);
            let s = seconds%60;
            document.getElementById('timer').innerText = `${{m}}:${{s<10?'0'+s:s}}`;
            if(seconds <= 0) submitTest();
        }}, 1000);

        function submitTest() {{
            let score = 0;
            document.querySelectorAll('.q-box').forEach(box => {{
                let sel = box.querySelector('input:checked');
                if(sel && sel.value === sel.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('temp_score', score);
            window.open('{AD_CONFIG['SMARTLINK_2']}', '_blank');
            setTimeout(() => window.location.href = '/result', 1000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 500px;">
        <div class="main-card p-5 shadow-lg">
            <i class="fas fa-award text-warning fa-5x mb-3"></i>
            <h2 class="fw-bold">RESULT</h2>
            <h1 class="display-1 fw-bold text-primary" id="sc_val">0</h1>
            <p class="text-muted">You passed the Courstika-Style Model Test!</p>
            <hr>
            {AD_CONFIG['BANNER_728']}
            <button onclick="window.open('{AD_CONFIG['SMARTLINK_2']}')" class="btn btn-dark w-100 p-3 rounded-pill mb-3 fw-bold">CLAIM REWARD (AD)</button>
            <a href="/" class="btn btn-outline-primary w-100 p-3 rounded-pill fw-bold">RETAKE EXAM</a>
        </div>
    </div>
    <script>
        document.getElementById('sc_val').innerText = localStorage.getItem('temp_score') + "/30";
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=True)
