import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD CONFIGURATION ---
SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

# --- MEGA QUESTION DATABASE ---
# Format: (Question, Correct, Wrong1, Wrong2, Wrong3)
DB = {
    # --- ICT (Chapter 1 & 2) ---
    'ict_all': [
        ("বিশ্বগ্রামের মেরুদণ্ড কোনটি?", "কানেক্টিভিটি", "ডেটা", "হার্ডওয়্যার", "সফটওয়্যার"),
        ("ই-লার্নিং এর পূর্ণরূপ কী?", "Electronic Learning", "Email Learning", "Easy Learning", "Electric Learning"),
        ("টেলিমেডিসিন কী?", "ফোনে চিকিৎসা", "ভিডিও চ্যাট", "অনলাইন কেনাকাটা", "ই-বুক"),
        ("ফেসবুকের নির্মাতা কে?", "মার্ক জুকারবার্গ", "বিল গেটস", "স্টিভ জবস", "জেফ বেজোস"),
        ("বিংশ শতাব্দীতে সম্পদের ধারণা কোনটি?", "জ্ঞান", "টাকা", "ভূমি", "যন্ত্রপাতি"),
        ("ই-পুর্জি কী?", "চিনিকলের ডিজিটাল অনুমতি", "ই-বুক", "অনলাইন লাইব্রেরি", "গেম"),
        ("প্রথম গণনা যন্ত্রের নাম কী?", "অ্যাবাকাস", "ক্যালকুলেটর", "কম্পিউটার", "এনিয়াক"),
        ("আধুনিক কম্পিউটারের জনক কে?", "চার্লস ব্যাবেজ", "লেডি লাভলেস", "জেমস ওয়াট", "নিউটন"),
        ("ভাইরাসের পূর্ণরূপ কী?", "Vital Information Resources Under Siege", "Visual Info Resource", "Very Important Result", "Virus Info"),
        ("RAM এর কাজ কী?", "অস্থায়ী মেমোরি", "স্থায়ী মেমোরি", "গেম খেলা", "চার্জ দেওয়া"),
        ("১ গিগাবাইট সমান কত?", "১০২৪ মেগাবাইট", "১০০০ মেগাবাইট", "৫১২ মেগাবাইট", "১২৮ মেগাবাইট"),
        ("আইনস্টাইন কোন বিষয়ে বিখ্যাত?", "আপেক্ষিকতা", "কম্পিউটার", "মোবাইল", "সফটওয়্যার"),
        ("ব্যান্ডউইথ কী?", "ডেটা প্রবাহের হার", "মেমোরি সাইজ", "ইন্টারনেট কানেকশন", "সফটওয়্যার"),
        ("পাসওয়ার্ড কেন ব্যবহার করা হয়?", "নিরাপত্তার জন্য", "রঙের জন্য", "সৌন্দর্যের জন্য", "ভুলে যাওয়ার জন্য"),
        ("Windows কী ধরনের সফটওয়্যার?", "অপারেটিং সিস্টেম", "এপ্লিকেশন", "ভাইরাস", "ড্রাইভার")
    ] * 2, # মোট ৩০টি করার জন্য

    # --- ENGLISH (Grammar Mix) ---
    'eng_all': [
        ("Identify the Noun of 'Beautiful':", "Beauty", "Beautify", "Beautifully", "Beauties"),
        ("He ___ to school every day.", "goes", "go", "going", "gone"),
        ("Antonym of 'Hot':", "Cold", "Warm", "Burning", "Summer"),
        ("Choose the correct spelling:", "Receive", "Recieve", "Receve", "Ricieve"),
        ("He is ___ honest man.", "an", "a", "the", "no article"),
        ("Plural of 'Mouse':", "Mice", "Mouses", "Mices", "Mouse"),
        ("Identify the Verb:", "Eat", "Apple", "Big", "Slowly"),
        ("An umbrella is ___ useful thing.", "a", "an", "the", "some"),
        ("Past form of 'Write':", "Wrote", "Written", "Writing", "Writes"),
        ("Synonym of 'Fast':", "Quick", "Slow", "Steady", "Lazy"),
        ("Who is the writer of 'Hamlet'?", "Shakespeare", "Milton", "Keats", "Shelley"),
        ("I ___ a student.", "am", "is", "are", "was"),
        ("Antonym of 'Rich':", "Poor", "Kind", "Good", "Wealthy"),
        ("Identify Adjective:", "Beautiful", "Run", "Slowly", "Table"),
        ("Present Continuous of 'Play':", "Playing", "Played", "Plays", "Player")
    ] * 2,

    # --- BANGLA (সাহিত্য ও ব্যাকরণ) ---
    'bng_all': [
        ("বাংলা ভাষার মূল উৎস কী?", "প্রাকৃত", "সংস্কৃত", "পালি", "হিন্দি"),
        ("'বঙ্গবাণী' কবিতার কবি কে?", "আবদুল হাকিম", "নজরুল", "রবীন্দ্রনাথ", "ফররুখ আহমদ"),
        ("বিভক্তি কয় প্রকার?", "৭ প্রকার", "৫ প্রকার", "৩ প্রকার", "১০ প্রকার"),
        ("'অগ্নিবীণা' কাব্যগ্রন্থের রচয়িতা কে?", "নজরুল ইসলাম", "জসীমউদ্দীন", "জীবনানন্দ", "শামসুর রহমান"),
        ("সারাংশে কোনটি থাকে না?", "উপমা ও অলংকার", "মূল ভাব", "গদ্য", "কবিতা"),
        ("সমাস প্রধানত কয় প্রকার?", "৬ প্রকার", "৪ প্রকার", "৮ প্রকার", "৩ প্রকার"),
        ("কোনটি তৎসম শব্দ?", "চন্দ্র", "মাঠ", "পাখি", "ঘর"),
        ("শব্দের ক্ষুদ্রতম অংশকে কী বলে?", "ধ্বনি", "শব্দ", "বাক্য", "বর্ণ"),
        ("ব্যাকরণের প্রধান কাজ কী?", "ভাষার নিয়ম রক্ষা", "কথা বলা", "গল্প লেখা", "গান গাওয়া"),
        ("তাসের ঘর বাগধারার অর্থ কী?", "ক্ষণস্থায়ী বস্তু", "জুয়া খেলা", "মাটির ঘর", "ভীষণ ভয়"),
        ("একুশে ফেব্রুয়ারির গানের রচয়িতা কে?", "আবদুল গাফফার চৌধুরী", "আলতাফ মাহমুদ", "নজরুল", "মুনীর চৌধুরী"),
        ("চাচা কাহিনীর লেখক কে?", "সৈয়দ মুজতবা আলী", "হুমায়ূন আহমেদ", "রবীন্দ্রনাথ", "শরৎচন্দ্র"),
        ("সন্ধি শব্দের অর্থ কী?", "মিলন", "বিচ্ছেদ", "তৈরি", "ভাঙন"),
        ("কারক কয় প্রকার?", "৬ প্রকার", "৭ প্রকার", "৪ প্রকার", "৫ প্রকার"),
        ("উভয় পদ প্রধান কোন সমাসে?", "দ্বন্দ্ব সমাস", "দ্বিগু সমাস", "তৎপুরুষ", "অব্যয়ীভাব")
    ] * 2,

    # --- MATH (জ্যামিতি ও বীজগণিত) ---
    'math_all': [
        ("(a+b)² = ?", "a²+2ab+b²", "a²-2ab+b²", "a²+b²", "a²+2ab-b²"),
        ("বর্গের ক্ষেত্রফল কী?", "বাহু²", "দৈর্ঘ্য×প্রস্থ", "২×বাহু", "৪×বাহু"),
        ("সমকোণী ত্রিভুজের একটি কোণ কত?", "৯০°", "৬০°", "১৮০°", "৪৫°"),
        ("বৃত্তের ব্যাস ব্যাসার্ধের কত গুণ?", "২ গুণ", "৩ গুণ", "অর্ধেক", "সমান"),
        ("ত্রিভুজের তিন কোণের সমষ্টি কত?", "১৮০°", "৯০°", "৩৬০°", "২৭০°"),
        ("সবচেয়ে ছোট মৌলিক সংখ্যা কোনটি?", "২", "১", "৩", "০"),
        ("π (পাই) এর মান কত?", "৩.১৪১৬", "৩.১২", "৪.১৪", "২.৭"),
        ("x+y=5, x-y=1 হলে x এর মান কত?", "৩", "২", "৪", "৫"),
        ("আয়তক্ষেত্রের পরিসীমা কী?", "২(দৈর্ঘ্য+প্রস্থ)", "দৈর্ঘ্য×প্রস্থ", "৪×বাহু", "৩×বাহু"),
        ("লগারিদমের উদ্ভাবক কে?", "জন নেপিয়ার", "নিউটন", "পিথাগোরাস", "আর্কিমিডিস"),
        ("১ থেকে ১০০ এর মধ্যে কয়টি মৌলিক সংখ্যা?", "২৫টি", "১৫টি", "৩০টি", "২০টি"),
        ("পিথাগোরাসের উপপাদ্য কোন ত্রিভুজে ব্যবহৃত হয়?", "সমকোণী", "সমবাহু", "স্থূলকোণী", "সূক্ষ্মকোণী"),
        ("a⁰ এর মান কত?", "১", "০", "a", "Infinity"),
        ("চতুর্ভুজের কয়টি শীর্ষবিন্দু থাকে?", "৪টি", "৩টি", "৫টি", "৬টি"),
        ("নিচের কোনটি অমূলদ সংখ্যা?", "√৩", "৪", "০.৫", "২/৩")
    ] * 2
}

STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    body { background: #f0f2f5; font-family: 'Poppins', sans-serif; }
    .hero { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; padding: 60px 20px; border-radius: 0 0 50px 50px; text-align: center; }
    .main-card { background: white; border-radius: 30px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); margin-top: -40px; }
    .btn-earn { background: #ff7675; color: white; padding: 15px; border-radius: 15px; font-weight: bold; width: 100%; border: none; margin-bottom: 20px; }
    .btn-start { background: #00b894; color: white; padding: 15px; border-radius: 15px; font-weight: bold; width: 100%; border: none; }
    .q-card { background: white; border-radius: 20px; padding: 20px; margin-bottom: 25px; border-left: 10px solid #6c5ce7; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .option-btn { display: block; padding: 15px; margin: 10px 0; background: #f8f9fa; border: 2px solid #eee; border-radius: 12px; cursor: pointer; transition: 0.3s; }
    .option-btn:hover { background: #eef2f7; border-color: #6c5ce7; }
    input[type="radio"] { display: none; }
    input[type="radio"]:checked + span { color: #6c5ce7; font-weight: bold; }
</style>
"""

@app.route('/')
def home():
    return render_template_string(STYLE + f"""
    <div class="hero">
        <h1 class="fw-bold">SSC Test Paper 2026</h1>
        <p>অধ্যায়ভিত্তিক পূর্ণাঙ্গ ডিজিটাল প্রস্তুতি</p>
        <div class="badge bg-white text-dark p-2 px-4 rounded-pill shadow">Balance: <span id="cr_val">0</span> Cr</div>
    </div>
    <div class="container" style="max-width: 600px;">
        <div class="main-card">
            <button onclick="earn()" class="btn-earn shadow"><i class="fas fa-gift"></i> EARN 10 CREDITS (WATCH ADS)</button>
            <label class="fw-bold text-muted mb-2">SELECT SUBJECT:</label>
            <select id="sub_sel" class="form-select form-select-lg mb-4 shadow-sm" style="border-radius: 12px;">
                <option value="ict_all">ICT: তথ্য ও যোগাযোগ প্রযুক্তি</option>
                <option value="eng_all">English: Grammar Specialist</option>
                <option value="bng_all">Bangla: ১ম ও ২য় পত্র</option>
                <option value="math_all">Math: বীজগণিত ও জ্যামিতি</option>
            </select>
            <button id="st_btn" onclick="start()" class="btn-start shadow" disabled>NEED 5 CREDITS 🔒</button>
        </div>
    </div>
    <script>
        let cr = localStorage.getItem('ssc_credits') || 0;
        document.getElementById('cr_val').innerText = cr;
        if(cr >= 5) {{
            document.getElementById('st_btn').disabled = false;
            document.getElementById('st_btn').innerHTML = "🚀 START 30 MCQ EXAM";
        }}
        function earn() {{
            window.open('{SMARTLINK_1}', '_blank');
            setTimeout(() => {{
                localStorage.setItem('ssc_credits', parseInt(cr) + 10);
                location.reload();
            }}, 3000);
        }}
        function start() {{
            localStorage.setItem('ssc_credits', cr - 5);
            window.location.href = '/exam?sub=' + document.getElementById('sub_sel').value;
        }}
    </script>
    """)

@app.route('/exam')
def exam():
    sub = request.args.get('sub', 'ict_all')
    questions = DB.get(sub, [])
    random.shuffle(questions)
    selected = questions[:30]

    q_html = ""
    for i, (q, corr, w1, w2, w3) in enumerate(selected):
        opts = [corr, w1, w2, w3]
        random.shuffle(opts)
        q_html += f"""
        <div class="q-card">
            <h5 class="fw-bold mb-3">{i+1}. {q}</h5>
            {"".join([f'<label class="option-btn"><input type="radio" name="q{i}" value="{o}" data-ans="{corr}"><span>{o}</span></label>' for o in opts])}
        </div>
        """
        if (i+1) % 5 == 0:
            q_html += f'<div class="text-center p-3 mb-4 bg-light rounded">-- Sponsored Content --</div>'

    return render_template_string(STYLE + f"""
    <div class="container mt-4" style="max-width: 800px;">
        <div class="sticky-top bg-white p-3 shadow-sm rounded mb-4 d-flex justify-content-between align-items-center">
            <h4 class="m-0 text-primary"><b>SSC 2026:</b> {sub.split('_')[0].upper()}</h4>
            <div class="badge bg-danger p-2 px-3">Time: 20:00</div>
        </div>
        {q_html}
        <button onclick="finish()" class="btn-start mb-5 shadow-lg">✅ SUBMIT EXAM</button>
    </div>
    <div id="loading" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:20%;">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
        <h2 class="mt-4">Grading Your Test Paper...</h2>
    </div>
    <script>
        function finish() {{
            let score = 0;
            document.querySelectorAll('.q-card').forEach(card => {{
                let sel = card.querySelector('input:checked');
                if(sel && sel.value === sel.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('ssc_score', score);
            window.open('{SMARTLINK_2}', '_blank');
            document.getElementById('loading').style.display = 'block';
            setTimeout(() => {{ window.location.href = '/result'; }}, 6000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 500px;">
        <div class="main-card p-5">
            <h2 class="fw-bold mb-4">Exam Summary</h2>
            <div class="p-4 bg-light rounded-pill mb-4 border border-primary">
                <span class="text-muted d-block">YOUR SCORE</span>
                <h1 class="display-3 fw-bold text-primary mb-0" id="fs">0</h1>
                <small class="fw-bold">OUT OF 30</small>
            </div>
            <div id="msg" class="alert fw-bold p-3"></div>
            <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn-earn shadow mt-3">🎓 GET SSC CERTIFICATE</button>
            <a href="/" class="d-block mt-4 text-muted text-decoration-none">← Go Back Home</a>
        </div>
    </div>
    <script>
        let s = localStorage.getItem('ssc_score') || 0;
        document.getElementById('fs').innerText = s;
        let m = document.getElementById('msg');
        if(s >= 24) {{ m.innerText = "Excellent Performance! (A+)"; m.classList.add('alert-success'); }}
        else if(s >= 15) {{ m.innerText = "Good Job! Keep Learning."; m.classList.add('alert-info'); }}
        else {{ m.innerText = "Need Improvement! Try Again."; m.classList.add('alert-danger'); }}
        
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK_1}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=False)
