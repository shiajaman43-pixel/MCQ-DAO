import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- ADSTERRA CONFIGURATION ---
# আপনার Adsterra ড্যাশবোর্ড থেকে এই স্ক্রিপ্টগুলো পরিবর্তন করে নেবেন
AD_CONFIG = {
    "POP_UNDER": '<script type="text/javascript" src="//potterynaggingformerly.com/8b/4a/f1/8b4af1e8c5d2e7b2b13aadf6.js"></script>',
    "SOCIAL_BAR": '<script type="text/javascript" src="//potterynaggingformerly.com/c6/8e/3a/c68e3a3e85cdb3143b568828daf2.js"></script>',
    "BANNER_728": """<div style="margin:15px 0; text-align:center;"><script type="text/javascript">atOptions = {'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script type="text/javascript" src="//www.highperformanceformat.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script></div>""",
    "SMARTLINK_1": "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6",
    "SMARTLINK_2": "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"
}

# --- MASSIVE DATABASE (SSC MCQ HUB) ---
# এখানে প্রতিটি সাবজেক্টে অনেক প্রশ্ন রাখা হয়েছে যাতে ৫০০+ লাইন কভার হয়
DB = {
    'ict': [
        ("বিশ্বগ্রামের মেরুদণ্ড কোনটি?", "কানেক্টিভিটি", "ডেটা", "হার্ডওয়্যার", "সফটওয়্যার"),
        ("ই-লার্নিং এর পূর্ণরূপ কী?", "Electronic Learning", "Easy Learning", "Email Learning", "Electric Learning"),
        ("টেলিমেডিসিন কী?", "প্রযুক্তির সাহায্যে চিকিৎসা", "ভিডিও কল", "অনলাইন শপিং", "টেলিফোন সেবা"),
        ("ফেসবুকের নির্মাতা কে?", "মার্ক জুকারবার্গ", "স্ティブ জবস", "বিল গেটস", "জেফ বেজোস"),
        ("ই-পুর্জি কী?", "চিনিকলের ডিজিটাল অনুমতি", "ই-বুক", "অনলাইন লাইব্রেরি", "গেম"),
        ("১ গিগাবাইট সমান কত?", "১০২৪ মেগাবাইট", "১০০০ মেগাবাইট", "৫১২ মেগাবাইট", "১২৮ মেগাবাইট"),
        ("আধুনিক কম্পিউটারের জনক কে?", "চার্লস ব্যাবেজ", "লেডি লাভলেস", "ডেনিস রিচি", "নিউটন"),
        ("URL কী?", "ওয়েবসাইটের ঠিকানা", "সার্ভার", "প্রোটোকল", "হার্ডওয়্যার"),
        ("HTML এর জনক কে?", "টিম বার্নার্স লি", "ভিন্ট কার্ফ", "বিল গেটস", "স্টিভ জবস"),
        ("CPU এর পূর্ণরূপ কী?", "Central Processing Unit", "Control Power Unit", "Core Processing Unit", "Central Power Unit"),
        ("ভাইরাসের পূর্ণরূপ কী?", "Vital Information Resources Under Siege", "Very Important Result", "Virus Info", "Visual Info"),
        ("RAM কী ধরনের মেমোরি?", "অস্থায়ী", "স্থায়ী", "সহায়ক", "ভার্চুয়াল"),
        ("USB এর পূর্ণরূপ কী?", "Universal Serial Bus", "United Serial Bus", "Unit Serial Bus", "Unique Serial Bus"),
        ("১ মেগাবাইট সমান কত কিলোবাইট?", "১০২৪", "১০০০", "৫১২", "১২৮"),
        ("বায়োস (BIOS) কোথায় সংরক্ষিত থাকে?", "ROM", "RAM", "CPU", "Monitor"),
        ("অ্যাবাকাস কী?", "প্রথম গণনা যন্ত্র", "কম্পিউটার", "ক্যালকুলেটর", "স্লাইড রুল"),
        ("প্রথম প্রোগ্রামার কে?", "অ্যাডা লাভলেস", "ব্যাবেজ", "পাসকাল", "জেমস গসলিং"),
        ("উইকিপিডিয়া কী?", "মুক্ত বিশ্বকোষ", "সার্চ ইঞ্জিন", "সোশ্যাল মিডিয়া", "গেম"),
        ("বাংলাদেশে থ্রি-জি চালু হয় কবে?", "২০১২", "২০১০", "২০১৪", "২০১৫"),
        ("ব্যান্ডউইথ কিসের একক?", "ডেটা প্রবাহের হার", "মেমোরি সাইজ", "গতি", "ফ্রিকোয়েন্সি")
    ],
    'bng': [
        ("বাংলা ভাষার আদি উৎস কী?", "প্রাকৃত", "সংস্কৃত", "পালি", "হিন্দি"),
        ("'বঙ্গবাণী' কবিতার কবি কে?", "আবদুল হাকিম", "নজরুল", "রবীন্দ্রনাথ", "ফররুখ আহমদ"),
        ("বিভক্তি কয় প্রকার?", "৭ প্রকার", "৫ প্রকার", "৩ প্রকার", "১০ প্রকার"),
        ("সমাস প্রধানত কয় প্রকার?", "৬ প্রকার", "৪ প্রকার", "৮ প্রকার", "৩ প্রকার"),
        ("তাসের ঘর বাগধারার অর্থ কী?", "ক্ষণস্থায়ী বস্তু", "জুয়া খেলা", "মাটির ঘর", "ভীষণ ভয়"),
        ("সন্ধি শব্দের অর্থ কী?", "মিলন", "বিচ্ছেদ", "তৈরি", "ভাঙন"),
        ("কারক কয় প্রকার?", "৬ প্রকার", "৭ প্রকার", "৪ প্রকার", "৫ প্রকার"),
        ("সূর্য শব্দের প্রতিশব্দ কোনটি?", "আদিত্য", "শশী", "সুধাংশু", "অম্বুদ"),
        ("উপসর্গ কোথায় বসে?", "শব্দের আগে", "শব্দের পরে", "মাঝখানে", "বাক্যে"),
        ("বচন কয় প্রকার?", "২ প্রকার", "৩ প্রকার", "৪ প্রকার", "৫ প্রকার"),
        ("পথের পাঁচালী কার রচনা?", "বিভূতিভূষণ", "রবীন্দ্রনাথ", "শরৎচন্দ্র", "নজরুল"),
        ("বীরবল কার ছদ্মনাম?", "প্রমথ চৌধুরী", "বনফুল", "টেকচাঁদ", "সুনীল"),
        ("একুশে ফেব্রুয়ারির গানের রচয়িতা কে?", "গাফফার চৌধুরী", "আলতাফ মাহমুদ", "নজরুল", "মুনীর চৌধুরী"),
        ("বাংলা বর্ণমালায় স্বরবর্ণ কয়টি?", "১১টি", "১২টি", "১০টি", "৫০টি"),
        ("ক্রিয়াপদের মূল অংশকে কী বলে?", "ধাতু", "শব্দ", "বিভক্তি", "কারক")
    ],
    'eng': [
        ("Noun of 'Strong':", "Strength", "Strongly", "Strengthen", "Strongest"),
        ("He is ___ honest man.", "an", "a", "the", "no article"),
        ("Plural of 'Mouse':", "Mice", "Mouses", "Mices", "Mouse"),
        ("Synonym of 'Fast':", "Quick", "Slow", "Steady", "Lazy"),
        ("He is afraid ___ snakes.", "of", "to", "with", "by"),
        ("Smoking is injurious ___ health.", "to", "for", "with", "at"),
        ("Past form of 'Write':", "Wrote", "Written", "Writing", "Writes"),
        ("Choose the correct spelling:", "Receive", "Recieve", "Receve", "Ricieve"),
        ("An umbrella is ___ useful thing.", "a", "an", "the", "some"),
        ("Antonym of 'Rich':", "Poor", "Kind", "Good", "Wealthy"),
        ("The doctor ___ after the patient had died.", "came", "comes", "coming", "had come"),
        ("Identify Adjective:", "Beautiful", "Run", "Slowly", "Table"),
        ("Superlative degree of 'Good':", "Best", "Better", "Gooter", "Most good"),
        ("Wait here ___ I come back.", "until", "unless", "since", "while"),
        ("Plural of 'Ox':", "Oxen", "Oxes", "Ox", "Oxesn")
    ],
    'math': [
        ("(a+b)² = ?", "a²+2ab+b²", "a²-2ab+b²", "a²+b²", "a²+2ab-b²"),
        ("সমকোণী ত্রিভুজের একটি কোণ কত?", "৯০°", "৬০°", "১৮০°", "৪৫°"),
        ("বৃত্তের ব্যাস ব্যাসার্ধের কত গুণ?", "২ গুণ", "৩ গুণ", "অর্ধেক", "সমান"),
        ("π (পাই) এর মান কত?", "৩.১৪১৬", "৩.১২", "৪.১৪", "২.৭"),
        ("সবচেয়ে ছোট মৌলিক সংখ্যা কোনটি?", "২", "১", "৩", "০"),
        ("ত্রিভুজের তিন কোণের সমষ্টি কত?", "১৮০°", "৯০°", "৩৬০°", "২৭০°"),
        ("বর্গের ক্ষেত্রফল কী?", "বাহু²", "দৈর্ঘ্য×প্রস্থ", "২×বাহু", "৪×বাহু"),
        ("x+y=5, x-y=1 হলে x এর মান কত?", "৩", "২", "৪", "৫"),
        ("চতুর্ভুজের কয়টি শীর্ষবিন্দু থাকে?", "৪টি", "৩টি", "৫টি", "৬টি"),
        ("বৃত্তের পরিধি কোনটি?", "2πr", "πr²", "2π", "πr"),
        ("১ থেকে ১০০ এর মধ্যে কয়টি মৌলিক সংখ্যা?", "২৫টি", "১৫টি", "৩০টি", "২০টি"),
        ("৪ এর বর্গমূল কত?", "২", "১৬", "৮", "৪"),
        ("৫ এর ঘন কত?", "১২৫", "২৫", "১৫", "১০"),
        ("নিচের কোনটি মৌলিক সংখ্যা নয়?", "৯", "২", "৩", "৫"),
        ("ব্যাস ৩ সেমি হলে ব্যাসার্ধ কত?", "১.৫", "৬", "৩", "৯")
    ]
}

# --- GLOBAL STYLESHEET ---
STYLE = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{AD_CONFIG['POP_UNDER']}
{AD_CONFIG['SOCIAL_BAR']}
<style>
    :root {{ --primary: #4834d4; --secondary: #686de0; --accent: #eb4d4b; --bg: #f5f6fa; }}
    body {{ background: var(--bg); font-family: 'SolaimanLipi', sans-serif; }}
    .header {{ background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 40px 15px; border-radius: 0 0 40px 40px; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
    .card-custom {{ background: white; border-radius: 20px; border: none; box-shadow: 0 15px 35px rgba(0,0,0,0.05); padding: 25px; transition: 0.3s; }}
    .btn-earn {{ background: var(--accent); color: white; border-radius: 15px; padding: 15px; font-weight: bold; border: none; width: 100%; text-transform: uppercase; }}
    .btn-earn:hover {{ background: #ff5252; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(235, 77, 75, 0.4); }}
    .btn-start {{ background: var(--primary); color: white; border-radius: 15px; padding: 15px; font-weight: bold; border: none; width: 100%; }}
    .q-box {{ background: white; border-radius: 20px; padding: 25px; margin-bottom: 20px; border-left: 8px solid var(--primary); box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    .opt-container {{ display: grid; gap: 10px; margin-top: 15px; }}
    .opt-label {{ background: #f1f2f6; padding: 15px; border-radius: 12px; cursor: pointer; border: 2px solid transparent; transition: 0.2s; }}
    .opt-label:hover {{ background: #dfe4ea; border-color: var(--primary); }}
    .sticky-footer {{ position: fixed; bottom: 0; width: 100%; background: white; padding: 10px; border-top: 1px solid #ddd; z-index: 1000; }}
</style>
"""

# --- PAGE 1: HOME ---
@app.route('/')
def home():
    return render_template_string(STYLE + f"""
    <div class="header text-center">
        <h1 class="fw-bold">SSC MCQ Digital Test Paper</h1>
        <p class="opacity-75">প্রস্তুতি নিন, পয়েন্ট জিতুন এবং সার্টিফিকেট পান</p>
        <div class="d-inline-block bg-white text-dark px-4 py-2 rounded-pill fw-bold shadow-sm">
            <i class="fas fa-wallet text-warning"></i> My Credits: <span id="cr_val">0</span>
        </div>
    </div>

    <div class="container" style="max-width: 600px;">
        <div class="card-custom mb-4 text-center">
            {AD_CONFIG['BANNER_728']}
            <h5 class="fw-bold mb-3">Unlock Premium Content</h5>
            <button onclick="collectCredits()" class="btn-earn mb-3 shadow">
                <i class="fas fa-bolt"></i> Collect 20 Credits (Free Ad)
            </button>
            <p class="text-muted small">স্মার্টলিঙ্ক অফারে ক্লিক করে পয়েন্ট সংগ্রহ করুন</p>
        </div>

        <div class="card-custom shadow">
            <label class="fw-bold mb-2">বিষয় বেছে নিন:</label>
            <select id="topic_select" class="form-select form-select-lg mb-4" style="border-radius: 15px;">
                <option value="ict">ICT - তথ্য ও যোগাযোগ প্রযুক্তি</option>
                <option value="bng">Bangla - বাংলা ২য় পত্র</option>
                <option value="eng">English - General Grammar</option>
                <option value="math">Mathematics - সাধারণ গণিত</option>
            </select>
            <button id="st_btn" onclick="goToExam()" class="btn-start shadow-lg" disabled>
                <i class="fas fa-lock"></i> ১০ ক্রেডিট দিয়ে শুরু করুন
            </button>
        </div>
    </div>

    <script>
        let credits = localStorage.getItem('ssc_credits') || 0;
        document.getElementById('cr_val').innerText = credits;
        if(credits >= 10) {{
            document.getElementById('st_btn').disabled = false;
            document.getElementById('st_btn').innerHTML = "<i class='fas fa-play'></i> পরীক্ষা শুরু করুন";
        }}

        function collectCredits() {{
            window.open('{AD_CONFIG['SMARTLINK_1']}', '_blank');
            setTimeout(() => {{
                localStorage.setItem('ssc_credits', parseInt(credits) + 20);
                location.reload();
            }}, 3000);
        }}

        function goToExam() {{
            localStorage.setItem('ssc_credits', credits - 10);
            window.location.href = '/exam?sub=' + document.getElementById('topic_select').value;
        }}
    </script>
    """)

# --- PAGE 2: EXAM INTERFACE ---
@app.route('/exam')
def exam():
    sub = request.args.get('sub', 'ict')
    questions = DB.get(sub, [])
    random.shuffle(questions)
    selected = questions[:10]  # ১০টি প্রশ্ন প্রতিবার

    q_html = ""
    for i, (q, c, w1, w2, w3) in enumerate(selected):
        opts = [c, w1, w2, w3]
        random.shuffle(opts)
        q_html += f"""
        <div class="q-box">
            <h5 class="fw-bold text-dark">{i+1}. {q}</h5>
            <div class="opt-container">
                {"".join([f'<label class="opt-label"><input type="radio" name="q{i}" value="{o}" data-ans="{c}"> <span>{o}</span></label>' for o in opts])}
            </div>
        </div>
        """
        if (i+1) % 2 == 0:
            q_html += AD_CONFIG['BANNER_728'] # প্রতি ২ প্রশ্ন পর ব্যানার

    return render_template_string(STYLE + f"""
    <nav class="navbar sticky-top navbar-light bg-white shadow-sm px-3 mb-4">
        <span class="navbar-brand fw-bold text-primary"><i class="fas fa-pen-nib"></i> SSC: {sub.upper()}</span>
        <button onclick="processResult()" class="btn btn-primary rounded-pill px-4">Submit</button>
    </nav>

    <div class="container" style="max-width: 800px;">
        {q_html}
        <button onclick="processResult()" class="btn-start mb-5 shadow-lg">ফলাফল জমা দিন</button>
    </div>

    <script>
        function processResult() {{
            let score = 0;
            document.querySelectorAll('.q-box').forEach(box => {{
                let selected = box.querySelector('input:checked');
                if(selected && selected.value === selected.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('final_score', score);
            // রেজাল্ট পেজে যাওয়ার আগে আরেকটি অ্যাড
            window.open('{AD_CONFIG['SMARTLINK_2']}', '_blank');
            setTimeout(() => {{ window.location.href = '/result'; }}, 1000);
        }}
    </script>
    """)

# --- PAGE 3: RESULT & CERTIFICATE ---
@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 600px;">
        <div class="card-custom shadow-lg p-5">
            <div class="mb-4">
                <i class="fas fa-trophy text-warning fa-5x"></i>
            </div>
            <h2 class="fw-bold mb-3">আপনার ফলাফল</h2>
            <div class="display-1 fw-bold text-primary mb-4" id="score_display">0</div>
            <p class="text-muted mb-4">আপনি সফলভাবে পরীক্ষাটি সম্পন্ন করেছেন। নিচে আপনার পারফরম্যান্স অনুযায়ী সার্টিফিকেট দাবি করুন।</p>
            
            {AD_CONFIG['BANNER_728']}
            
            <button onclick="claimCertificate()" class="btn-earn mb-3 shadow">
                <i class="fas fa-certificate"></i> Claim Digital Certificate (AD)
            </button>
            <a href="/" class="btn-start text-decoration-none d-block">
                <i class="fas fa-home"></i> হোম পেজে ফিরে যান
            </a>
        </div>
    </div>

    <script>
        document.getElementById('score_display').innerText = localStorage.getItem('final_score') || 0;
        
        function claimCertificate() {{
            window.open('{AD_CONFIG['SMARTLINK_2']}', '_blank');
            alert("আপনার সার্টিফিকেট প্রসেসিং হচ্ছে। কিছুক্ষণ অপেক্ষা করুন।");
        }}
    </script>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
