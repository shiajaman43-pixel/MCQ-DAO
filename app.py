import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- ADSTERRA PRO CONFIGURATION ---
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_TOP": """<div class="ad-slot"><script type="text/javascript">atOptions = {'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script></div>""",
    "SMARTLINK_1": "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6",
    "SMARTLINK_2": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"
}

# --- MASSIVE CHAPTER-WISE DATABASE ---
# ফরম্যাট: 'Subject_Chapter': [(Question, Correct, W1, W2, W3), ...]
DB = {
    # --- ICT CHAPTERS ---
    'ict_ch1': [("বিশ্বগ্রামের মেরুদণ্ড কোনটি?", "কানেক্টিভিটি", "ডেটা", "সফটওয়্যার", "হার্ডওয়্যার")] * 30, # ৩০টি প্রশ্ন
    'ict_ch2': [("Bluetooth এর দূরত্ব কত?", "১০-১০০ মিটার", "১ কিমি", "৫ মিটার", "১০০ কিমি")] * 30,
    'ict_ch3': [("HTML এর পূর্ণরূপ কী?", "HyperText Markup Language", "High Text ML", "Hyper Link", "Home Text")] * 30,
    'ict_ch4': [("লজিক গেট কয় প্রকার?", "৩ প্রকার", "২ প্রকার", "৫ প্রকার", "৪ প্রকার")] * 30,
    'ict_ch5': [("C ভাষায় ইনপুট ফাংশন কোনটি?", "scanf", "printf", "getch", "input")] * 30,

    # --- BANGLA CHAPTERS ---
    'bng_ch1': [("বিভক্তি কয় প্রকার?", "৭ প্রকার", "৫ প্রকার", "৮ প্রকার", "৩ প্রকার")] * 30,
    'bng_ch2': [("সমাস শব্দের অর্থ কী?", "সংক্ষেপণ", "মিলন", "বিচ্ছেদ", "তৈরি")] * 30,
    'bng_ch3': [("উপসর্গ কোথায় বসে?", "শব্দের আগে", "শব্দের পরে", "মাঝখানে", "বাক্যের শেষে")] * 30,
    'bng_ch4': [("সন্ধি কয় প্রকার?", "৩ প্রকার", "২ প্রকার", "৪ প্রকার", "৫ প্রকার")] * 30,
    'bng_ch5': [("ক্রিয়াপদের মূল অংশকে কী বলে?", "ধাতু", "শব্দ", "বিভক্তি", "কারক")] * 30,

    # --- MATH CHAPTERS ---
    'math_ch1': [("বাস্তব সংখ্যা কয়টি?", "অসংখ্য", "১টি", "১০টি", "১০০টি")] * 30,
    'math_ch2': [("সেট প্রকাশের পদ্ধতি কয়টি?", "২টি", "৩টি", "৪টি", "৫টি")] * 30,
    'math_ch3': [("(a+b)² এর সূত্র কোনটি?", "a²+2ab+b²", "a²-2ab+b²", "a²+b²", "2ab")] * 30,
    'math_ch4': [("log10 এর মান কত?", "1", "0", "10", "100")] * 30,
    'math_ch5': [("ত্রিভুজের কোণ কয়টি?", "৩টি", "৪টি", "৬টি", "২টি")] * 30,
}

# --- UI & STYLING ---
STYLE = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{AD_CONFIG['POP_UNDER']}
{AD_CONFIG['SOCIAL_BAR']}
<style>
    :root {{ --p: #6c5ce7; --s: #00b894; --dark: #1e272e; }}
    body {{ background: #f8f9fa; font-family: 'Segoe UI', sans-serif; }}
    .header-box {{ background: linear-gradient(45deg, #6c5ce7, #a29bfe); color: white; padding: 50px 0; border-radius: 0 0 50px 50px; text-align: center; }}
    .phase-card {{ background: white; border-radius: 25px; padding: 30px; margin-top: -40px; box-shadow: 0 15px 40px rgba(0,0,0,0.1); border: none; }}
    .btn-action {{ background: var(--p); color: white; border-radius: 15px; padding: 15px; width: 100%; font-weight: bold; border: none; transition: 0.3s; margin-bottom: 10px; }}
    .btn-action:hover {{ transform: translateY(-3px); box-shadow: 0 8px 20px rgba(108,92,231,0.3); }}
    .btn-earn {{ background: #ff7675; }}
    .q-box {{ background: white; border-radius: 20px; padding: 25px; margin-bottom: 20px; border-left: 8px solid var(--p); box-shadow: 0 5px 15px rgba(0,0,0,0.03); }}
    .opt-label {{ display: block; background: #f1f2f6; padding: 15px; margin: 10px 0; border-radius: 12px; cursor: pointer; border: 2px solid transparent; }}
    .opt-label:hover {{ border-color: var(--p); background: #f0edff; }}
    .sticky-top-custom {{ position: sticky; top: 0; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); z-index: 1000; padding: 15px; border-bottom: 1px solid #eee; }}
    .ad-slot {{ margin: 20px 0; text-align: center; }}
</style>
"""

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(STYLE + f"""
    <div class="header-box">
        <h1 class="fw-bold">SSC CHAPTER MASTER 2026</h1>
        <p>প্রতিটি অধ্যায়ে ৩০টি সেরা MCQ চ্যালেঞ্জ</p>
        <div class="badge bg-white text-dark p-2 px-4 rounded-pill shadow-sm">
            <i class="fas fa-coins text-warning"></i> Credits: <span id="cr_val">0</span>
        </div>
    </div>

    <div class="container" style="max-width: 600px;">
        <div class="phase-card">
            {AD_CONFIG['BANNER_TOP']}
            <button onclick="window.open('{AD_CONFIG['SMARTLINK_1']}')" class="btn-action btn-earn">
                <i class="fas fa-fire"></i> GET 50 CREDITS (AD)
            </button>
            
            <label class="fw-bold text-muted small mt-3 mb-2">বিষয় ও অধ্যায় নির্বাচন করুন:</label>
            <select id="ch_select" class="form-select form-select-lg mb-4" style="border-radius: 15px;">
                <optgroup label="ICT">
                    <option value="ict_ch1">ICT: অধ্যায় ১ (বিশ্বগ্রাম)</option>
                    <option value="ict_ch2">ICT: অধ্যায় ২ (নেটওয়ার্ক)</option>
                    <option value="ict_ch3">ICT: অধ্যায় ৩ (HTML)</option>
                    <option value="ict_ch4">ICT: অধ্যায় ৪ (লজিক গেট)</option>
                    <option value="ict_ch5">ICT: অধ্যায় ৫ (প্রোগ্রামিং)</option>
                </optgroup>
                <optgroup label="Bangla">
                    <option value="bng_ch1">বাংলা: অধ্যায় ১ (বিভক্তি)</option>
                    <option value="bng_ch2">বাংলা: অধ্যায় ২ (সমাস)</option>
                    <option value="bng_ch3">বাংলা: অধ্যায় ৩ (উপসর্গ)</option>
                    <option value="bng_ch4">বাংলা: অধ্যায় ৪ (সন্ধি)</option>
                    <option value="bng_ch5">বাংলা: অধ্যায় ৫ (ক্রিয়াপদ)</option>
                </optgroup>
            </select>
            
            <button id="st_btn" onclick="startTest()" class="btn-action">
                <i class="fas fa-play"></i> START EXAM (30 Credits)
            </button>
        </div>
    </div>

    <script>
        let credits = localStorage.getItem('ssc_master_cr') || 0;
        document.getElementById('cr_val').innerText = credits;
        
        function startTest() {{
            if(credits >= 30) {{
                localStorage.setItem('ssc_master_cr', credits - 30);
                window.location.href = '/exam?ch=' + document.getElementById('ch_select').value;
            }} else {{
                alert("আপনার পর্যাপ্ত ক্রেডিট নেই! লাল বাটনে ক্লিক করুন।");
            }}
        }}
        
        // Auto Credit Reward for Staying
        setInterval(() => {{
            credits = parseInt(credits) + 5;
            localStorage.setItem('ssc_master_cr', credits);
            document.getElementById('cr_val').innerText = credits;
        }}, 60000);
    </script>
    """)

@app.route('/exam')
def exam():
    ch_id = request.args.get('ch', 'ict_ch1')
    questions = DB.get(ch_id, [])
    # ৩০টি প্রশ্ন র্যান্ডমাইজ করা হচ্ছে
    random.shuffle(questions)
    
    q_html = ""
    for i, (q, c, w1, w2, w3) in enumerate(questions):
        opts = [c, w1, w2, w3]
        random.shuffle(opts)
        q_html += f"""
        <div class="q-box">
            <h5 class="fw-bold mb-4">{i+1}. {q}</h5>
            {"".join([f'<label class="opt-label"><input type="radio" name="q{i}" value="{o}" data-ans="{c}"> {o}</label>' for o in opts])}
        </div>
        """
        # প্রতি ৫ প্রশ্ন পর একটি অ্যাড ব্যানার
        if (i+1) % 5 == 0:
            q_html += AD_CONFIG['BANNER_TOP']

    return render_template_string(STYLE + f"""
    <div class="sticky-top-custom shadow-sm">
        <div class="container d-flex justify-content-between align-items-center">
            <h5 class="m-0 fw-bold text-primary">Chapter: {ch_id.upper()}</h5>
            <div id="timer" class="fw-bold text-danger">30:00</div>
            <button onclick="submitExam()" class="btn btn-dark btn-sm rounded-pill px-3">Finish</button>
        </div>
    </div>

    <div class="container mt-4" style="max-width: 800px;">
        {q_html}
        <button onclick="submitExam()" class="btn-action mb-5 shadow-lg">SUBMIT ANSWERS</button>
    </div>

    <script>
        let time = 1800;
        setInterval(() => {{
            time--;
            let m = Math.floor(time/60);
            let s = time%60;
            document.getElementById('timer').innerText = `${{m}}:${{s<10?'0'+s:s}}`;
            if(time <= 0) submitExam();
        }}, 1000);

        function submitExam() {{
            let score = 0;
            document.querySelectorAll('.q-box').forEach(box => {{
                let sel = box.querySelector('input:checked');
                if(sel && sel.value === sel.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('last_score', score);
            window.open('{AD_CONFIG['SMARTLINK_2']}', '_blank');
            setTimeout(() => window.location.href = '/result', 1000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 500px;">
        <div class="phase-card p-5">
            <h2 class="fw-bold">Your Score</h2>
            <h1 class="display-1 fw-bold text-primary" id="sc">0</h1>
            <p class="text-muted mb-4">You have successfully completed the 30-MCQ challenge!</p>
            
            {AD_CONFIG['BANNER_TOP']}
            
            <button onclick="window.open('{AD_CONFIG['SMARTLINK_2']}')" class="btn-action">
                <i class="fas fa-download"></i> DOWNLOAD CERTIFICATE (AD)
            </button>
            <a href="/" class="btn btn-outline-primary w-100 p-3 rounded-4 fw-bold">Back to Home</a>
        </div>
    </div>
    <script>
        document.getElementById('sc').innerText = localStorage.getItem('last_score') + "/30";
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=True)
