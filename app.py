import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD CONFIGURATION ---
SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

# --- MEGA DATABASE START (SSC MCQ HUB) ---
DB = {
    # --- ICT: Chapter 1 (Information & Communication Technology) ---
    'ict_ch1': [
        ("বিশ্বগ্রামের মেরুদণ্ড কোনটি?", "কানেক্টিভিটি", "ডেটা", "হার্ডওয়্যার", "সফটওয়্যার"),
        ("ই-লার্নিং এর পূর্ণরূপ কী?", "Electronic Learning", "Easy Learning", "Email Learning", "Electric Learning"),
        ("টেলিমেডিসিন কী?", "প্রযুক্তির সাহায্যে চিকিৎসা", "ভিডিও কল", "অনলাইন শপিং", "টেলিফোন সেবা"),
        ("ফেসবুকের নির্মাতা কে?", "মার্ক জুকারবার্গ", "স্টিভ জবস", "বিল গেটস", "জেফ বেজোস"),
        ("ই-পুর্জি কী?", "চিনিকলের ডিজিটাল অনুমতি", "ই-বুক", "অনলাইন লাইব্রেরি", "গেম"),
        ("ডিজিটাল বাংলাদেশ কত সালে ঘোষণা করা হয়?", "২০০৮", "২০১০", "২০২১", "২০৪১"),
        ("একুশ শতকের সম্পদ কোনটি?", "জ্ঞান", "টাকা", "ভূমি", "যন্ত্রপাতি"),
        ("প্রথম গণনা যন্ত্র কোনটি?", "অ্যাবাকাস", "কম্পিউটার", "ক্যালকুলেটর", "স্লাইড রুল"),
        ("আধুনিক কম্পিউটারের জনক কে?", "চার্লস ব্যাবেজ", "লেডি লাভলেস", "ডেনিস রিচি", "নিউটন"),
        ("ই-গভর্ন্যান্স এর লক্ষ্য কী?", "সুশাসন", "টাকা কামানো", "সময় নষ্ট", "বিনোদন"),
        ("ইন্টারনেটের জনক কে?", "ভিন্ট কার্ফ", "টিম বার্নার্স লি", "রে টমলিনসন", "বিল গেটস"),
        ("ই-বুক বলতে কী বোঝায়?", "ইলেকট্রনিক বই", "সহজ বই", "দামি বই", "কাগজের বই"),
        ("বাংলাদেশে থ্রি-জি চালু হয় কবে?", "২০১২", "২০১০", "২০১৪", "২০১৫"),
        ("প্রোগ্রামিং এর ধারণা প্রথম কে দেন?", "অ্যাডা লাভলেস", "ব্যাবেজ", "পাসকাল", "জেমস গসলিং"),
        ("উইকিপিডিয়া কী?", "মুক্ত বিশ্বকোষ", "সার্চ ইঞ্জিন", "সোশ্যাল মিডিয়া", "গেম"),
        ("টুইটার কী?", "মাইক্রোব্লগিং সাইট", "ভিডিও সাইট", "ই-মেইল", "সার্চ ইঞ্জিন"),
        ("সবচেয়ে বড় হেডার ট্যাগ কোনটি?", "<h1>", "<h3>", "<h6>", "<head>"),
        ("CPU এর পূর্ণরূপ কী?", "Central Processing Unit", "Control Power Unit", "Core Processing Unit", "Central Power Unit"),
        ("HTML এর জনক কে?", "টিম বার্নার্স লি", "ভিন্ট কার্ফ", "বিল গেটস", "স্টিভ জবস"),
        ("Wi-Fi এর পূর্ণরূপ কী?", "Wireless Fidelity", "Wireless Fiber", "Wire Fidelity", "Win Fiber"),
        ("বাংলাদেশে ই-লার্নিং এর গুরুত্ব কী?", "শিক্ষা সহজ করা", "বিনোদন", "টাকা উপার্জন", "সময় কাটানো"),
        ("URL কী?", "ওয়েবসাইটের ঠিকানা", "সার্ভার", "প্রোটোকল", "হার্ডওয়্যার"),
        ("সার্চ ইঞ্জিন কোনটি?", "Google", "Facebook", "WhatsApp", "Excel"),
        ("ব্যান্ডউইথ কিসের একক?", "ডেটা প্রবাহের হার", "মেমোরি সাইজ", "গতি", "ফ্রিকোয়েন্সি"),
        ("১ গিগাবাইট সমান কত?", "১০২৪ মেগাবাইট", "১০০০ মেগাবাইট", "৫১২ মেগাবাইট", "১২৮ মেগাবাইট"),
        ("ই-কমার্স কী?", "অনলাইন কেনাকাটা", "গেম খেলা", "ভিডিও চ্যাট", "পড়াশোনা"),
        ("মাইক্রোসফটের প্রতিষ্ঠাতা কে?", "বিল গেটস", "মার্ক জুকারবার্গ", "এলন মাস্ক", "জেফ বেজোস"),
        ("আইসিটি এর পূর্ণরূপ কী?", "Information and Communication Technology", "Internal Tech", "Internet Tech", "Info Tech"),
        ("উইন্ডোজ কী?", "অপারেটিং সিস্টেম", "সফটওয়্যার", "হার্ডওয়্যার", "ব্রাউজার"),
        ("পাসওয়ার্ড কেন ব্যবহৃত হয়?", "নিরাপত্তার জন্য", "সৌন্দর্যের জন্য", "ভুলে যাওয়ার জন্য", "রঙের জন্য")
    ],
    
    # --- ICT: Chapter 2 (Computer & User Security) ---
    'ict_ch2': [
        ("ভাইরাসের পূর্ণরূপ কী?", "Vital Information Resources Under Siege", "Very Important Result", "Virus Info", "Visual Info"),
        ("প্রথম অ্যান্টিভাইরাস কোনটি?", "রিপার", "ক্যাসপারস্কি", "নর্টন", "আভাস্ট"),
        ("কম্পিউটারের মগজ কাকে বলা হয়?", "CPU", "RAM", "Hard Disk", "Monitor"),
        ("RAM কী ধরনের মেমোরি?", "অস্থায়ী", "স্থায়ী", "সহায়ক", "ভার্চুয়াল"),
        ("সফটওয়্যার ডিলিট করতে কোথায় যেতে হয়?", "Control Panel", "Desktop", "Recycle Bin", "My Computer"),
        ("ট্রোজান হর্স কী?", "এক ধরনের ভাইরাস", "গেম", "অ্যান্টিভাইরাস", "অ্যাপ"),
        ("টু-ফ্যাক্টর অথেন্টিকেশন কেন লাগে?", "অ্যাকাউন্ট নিরাপত্তার জন্য", "পাসওয়ার্ড পাওয়ার জন্য", "লগআউট করার জন্য", "গেম খেলার জন্য"),
        ("পাসওয়ার্ডকে কী দিয়ে সুরক্ষিত করা হয়?", "ক্যাপচা", "নাম", "ফোন নম্বর", "জন্ম তারিখ"),
        ("কম্পিউটার হ্যাং করলে কী করতে হয়?", "রিস্টার্ট", "বন্ধ করা", "ফেলে দেওয়া", "নতুন কেনা"),
        ("USB এর পূর্ণরূপ কী?", "Universal Serial Bus", "United Serial Bus", "Unit Serial Bus", "Unique Serial Bus"),
        ("পাসওয়ার্ডে কোনটির ব্যবহার বেশি নিরাপদ?", "চিহ্ন ও সংখ্যা", "নাম", "১-৬ পর্যন্ত সংখ্যা", "জন্ম তারিখ"),
        ("অপারেটিং সিস্টেম কোনটি?", "Linux", "Excel", "Photoshop", "Chrome"),
        ("ল্যাপটপের ব্যাটারি বেশি দিন টিকবে কী করলে?", "ফুল চার্জ হওয়ার পর খুলে রাখলে", "সব সময় চার্জ দিলে", "চার্জ না দিলে", "সারাদিন চালালে"),
        ("মডেম কোন ধরনের ডিভাইস?", "ইনপুট-আউটপুট", "ইনপুট", "আউটপুট", "স্টোরেজ"),
        ("কিবোর্ড কী ধরনের ডিভাইস?", "ইনপুট", "আউটপুট", "প্রসেসিং", "মেমোরি"),
        ("মনিটর কী ধরনের ডিভাইস?", "আউটপুট", "ইনপুট", "প্রসেসিং", "স্টোরেজ"),
        ("হার্ড ডিস্ক ড্রাইভ কী ধরনের মেমোরি?", "স্থায়ী", "অস্থায়ী", "প্রধান", "ভার্চুয়াল"),
        ("কম্পিউটারের গতি বাড়াতে কী ব্যবহার হয়?", "SSD", "CD", "Floppy Disk", "Modem"),
        ("ইন্টারনেটে পাসওয়ার্ড চুরির নাম কী?", "ফিশিং", "ব্রাউজিং", "চ্যাটিং", "সার্চিং"),
        ("সাইবার ক্রাইম কোনটি?", "হ্যাকিং", "পড়াশোনা", "গেম খেলা", "মুভি দেখা"),
        ("অ্যান্টিভাইরাস কোনটি?", "Avast", "Trojan", "Worm", "Spyware"),
        ("সফটওয়্যার ইন্সটল করতে কোনটি লাগে?", "Setup ফাইল", "Delete ফাইল", "Recycle বিন", "কিবোর্ড"),
        ("হার্ডওয়্যার কোনটি?", "মাউস", "উইন্ডোজ", "ভাইরাস", "এক্সেল"),
        ("পিক্সেল কিসের সাথে সম্পর্কিত?", "মনিটর", "মাউস", "কিবোর্ড", "ইউপিএস"),
        ("ইউপিএস (UPS) এর কাজ কী?", "বিদ্যুৎ চলে গেলে বিদ্যুৎ দেওয়া", "গান শোনা", "গেম খেলা", "টাইপ করা"),
        ("কম্পিউটারে তারিখ ঠিক থাকে কোন ব্যাটারির জন্য?", "CMOS", "Lithium", "Dry cell", "Lead acid"),
        ("বায়োস (BIOS) কোথায় সংরক্ষিত থাকে?", "ROM", "RAM", "CPU", "Monitor"),
        ("১ মেগাবাইট সমান কত কিলোবাইট?", "১০২৪", "১০০০", "৫১২", "১২৮"),
        ("ফায়ারওয়াল (Firewall) কী করে?", "অননুমোদিত প্রবেশ ঠেকায়", "আগুন নেভায়", "গতি বাড়ায়", "চার্জ দেয়"),
        ("অ্যাডওয়্যার (Adware) কী?", "বিজ্ঞাপন ভিত্তিক সফটওয়্যার", "গেম", "অ্যান্টিভাইরাস", "ব্রাউজার")
    ],

    # --- BANGLA (সাহিত্য ও ব্যাকরণ) ---
    'bng_all': [
        ("বাংলা ভাষার আদি উৎস কী?", "প্রাকৃত", "সংস্কৃত", "পালি", "হিন্দি"),
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
        ("উভয় পদ প্রধান কোন সমাসে?", "দ্বন্দ্ব সমাস", "দ্বিগু সমাস", "তৎপুরুষ", "অব্যয়ীভাব"),
        ("বাংলা বর্ণমালায় স্বরবর্ণ কয়টি?", "১১টি", "১২টি", "১০টি", "৫০টি"),
        ("ব্যঞ্জনবর্ণ কয়টি?", "৩৯টি", "৫০টি", "১১টি", "৪০টি"),
        ("যৌগিক স্বরবর্ণ কয়টি?", "২টি", "৫টি", "১১টি", "৭টি"),
        ("'নৈসর্গিক' শব্দের অর্থ কী?", "প্রাকৃতিক", "কৃত্রিম", "স্বর্গীয়", "সুন্দর"),
        ("'অর্বাচীন' শব্দের বিপরীত শব্দ কোনটি?", "প্রাচীন", "নতুন", "আধুনিক", "যুবক"),
        ("সূর্য শব্দের প্রতিশব্দ কোনটি?", "আদিত্য", "শশী", "সুধাংশু", "অম্বুদ"),
        ("বাক্যের মৌলিক উপাদান কী?", "শব্দ", "বর্ণ", "অর্থ", "উপসর্গ"),
        ("উপসর্গ কোথায় বসে?", "শব্দের আগে", "শব্দের পরে", "মাঝখানে", "বাক্যে"),
        ("বিভক্তিহীন নাম শব্দকে কী বলে?", "প্রাতিপদিক", "ধাতু", "পদ", "ক্রিয়া"),
        ("ক্রিয়াপদের মূল অংশকে কী বলে?", "ধাতু", "শব্দ", "বিভক্তি", "কারক"),
        ("কোনটি খাঁটি বাংলা উপসর্গ?", "অজ", "বি", "সু", "পরি"),
        ("'আম জনতা' শব্দে আম কোন ভাষার শব্দ?", "ফারসি", "আরবি", "হিন্দি", "বাংলা"),
        ("বচন কয় প্রকার?", "২ প্রকার", "৩ প্রকার", "৪ প্রকার", "৫ প্রকার"),
        ("কোনটি একবচনের উদাহরণ?", "ছেলেটি", "ছেলেরা", "মানুষগণ", "বইগুলো"),
        ("লিঙ্গান্তর হয় না কার?", "কবিরাজ", "শিক্ষক", "ছাত্র", "ধোপা")
    ],

    # --- ENGLISH (SSC Grammar Mix) ---
    'eng_all': [
        ("Identify the Noun of 'Strong':", "Strength", "Strongly", "Strengthen", "Strongest"),
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
        ("Present Continuous of 'Play':", "Playing", "Played", "Plays", "Player"),
        ("Choose the correct sentence:", "He is a doctor", "He am a doctor", "He are a doctor", "He doctor"),
        ("Superlative degree of 'Good':", "Best", "Better", "Gooter", "Most good"),
        ("Opposite of 'Boy':", "Girl", "Man", "Woman", "Sister"),
        ("Wait here ___ I come back.", "until", "unless", "since", "while"),
        ("He is afraid ___ snakes.", "of", "to", "with", "by"),
        ("Smoking is injurious ___ health.", "to", "for", "with", "at"),
        ("Past participle of 'Go':", "Gone", "Went", "Go", "Gones"),
        ("I have ___ inkpot.", "an", "a", "the", "any"),
        ("Which one is a pronoun?", "He", "Rahim", "Dhaka", "Book"),
        ("A person who writes books is an ___.", "Author", "Doctor", "Teacher", "Pilot"),
        ("Gender of 'Actor' is ___.", "Masculine", "Feminine", "Neuter", "Common"),
        ("The plural form of 'Knife' is ___.", "Knives", "Knifes", "Knife", "Knivs"),
        ("He cut a tree ___ an axe.", "with", "by", "from", "to"),
        ("Look ___ the map.", "at", "to", "on", "in"),
        ("Honesty is the best ___.", "Policy", "Poverty", "Police", "Place")
    ],

    # --- MATH (SSC Standard) ---
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
        ("নিচের কোনটি অমূলদ সংখ্যা?", "√৩", "৪", "০.৫", "২/৩"),
        ("রম্বসের ক্ষেত্রফল কোনটি?", "১/২ × কর্ণদ্বয়ের গুণফল", "দৈর্ঘ্য × প্রস্থ", "বাহু²", "২(a+b)"),
        ("বৃত্তের পরিধি কোনটি?", "2πr", "πr²", "2π", "πr"),
        ("মূলদ সংখ্যা কোনটি?", "০", "√২", "√৫", "π"),
        ("a²-b² = ?", "(a+b)(a-b)", "(a-b)²", "a²+b²", "a²+2ab+b²"),
        ("নিচের কোনটি মৌলিক সংখ্যা নয়?", "৯", "২", "৩", "৫"),
        ("২, ৪, ৬, ৮ এর গড় কত?", "৫", "৪", "৬", "১০"),
        ("ব্যাস ৩ সেমি হলে ব্যাসার্ধ কত?", "১.৫", "৬", "৩", "৯"),
        ("১০ এর ৫% কত?", "০.৫", "১", "৫", "২"),
        ("বর্গের চার কোণের সমষ্টি কত?", "৩৬০°", "১৮০°", "৯০°", "২৭০°"),
        ("একটি বৃত্তের কেন্দ্রে উৎপন্ন কোণ কত?", "৩৬০°", "১৮০°", "৯০°", "০°"),
        ("ধনাত্মক সংখ্যা কোনটি?", "৫", "-৫", "০", "সবগুলো"),
        ("৪ এর বর্গমূল কত?", "২", "১৬", "৮", "৪"),
        ("৫ এর ঘন কত?", "১২৫", "২৫", "১৫", "১০"),
        ("সমবাহু ত্রিভুজের প্রতিটি কোণ কত?", "৬০°", "৯০°", "৪৫°", "৩০°"),
        ("X² = 9 হলে X এর মান কত?", "৩", "৯", "৮১", "০")
    ]
}

# --- STYLING & CORE UI ---
STYLE = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    :root { --p-color: #6c5ce7; --s-color: #00b894; --d-color: #ff7675; }
    body { background: #f8f9fd; font-family: 'Segoe UI', sans-serif; color: #2d3436; }
    .hero-box { background: linear-gradient(135deg, var(--p-color), #a29bfe); color: white; padding: 70px 15px; border-radius: 0 0 50px 50px; text-align: center; }
    .glass-card { background: white; border-radius: 30px; padding: 35px; box-shadow: 0 20px 50px rgba(0,0,0,0.08); margin-top: -60px; border: 1px solid #fff; }
    .btn-mega { padding: 18px; border-radius: 18px; font-weight: 800; width: 100%; border: none; text-transform: uppercase; transition: 0.3s; letter-spacing: 1px; }
    .btn-reward { background: var(--d-color); color: white; margin-bottom: 25px; }
    .btn-reward:hover { background: #d63031; transform: scale(1.02); }
    .btn-action { background: var(--s-color); color: white; }
    .btn-action:disabled { background: #b2bec3; }
    .q-container { background: white; border-radius: 20px; padding: 25px; margin-bottom: 25px; border-left: 10px solid var(--p-color); box-shadow: 0 5px 15px rgba(0,0,0,0.03); }
    .opt-label { display: block; padding: 15px; margin: 12px 0; background: #f1f2f6; border-radius: 12px; cursor: pointer; border: 2px solid transparent; transition: 0.2s; }
    .opt-label:hover { background: #dfe4ea; border-color: var(--p-color); }
    input[type="radio"]:checked + span { color: var(--p-color); font-weight: bold; }
    input[type="radio"] { margin-right: 10px; accent-color: var(--p-color); }
    .sticky-header { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); padding: 15px; border-bottom: 1px solid #eee; }
</style>
"""

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(STYLE + f"""
    <div class="hero-box">
        <h1 class="fw-bold">SSC Digital Test Paper 2026</h1>
        <p class="opacity-75">অধ্যায়ভিত্তিক প্রস্তুতি এবং সার্টিফিকেট অর্জন করুন</p>
        <div class="badge bg-white text-dark p-2 px-4 rounded-pill shadow-sm"><i class="fas fa-coins text-warning"></i> My Balance: <span id="cr_val">0</span> Cr</div>
    </div>
    <div class="container" style="max-width: 650px;">
        <div class="glass-card shadow">
            <button onclick="addCr()" class="btn-mega btn-reward shadow-sm"><i class="fas fa-play-circle"></i> EARN 10 CREDITS (FREE ADS)</button>
            <label class="fw-bold text-muted small mb-2 uppercase">CHOOSE YOUR CHAPTER:</label>
            <select id="sub_list" class="form-select form-select-lg mb-4" style="border-radius: 15px;">
                <optgroup label="ICT - Class 9-10">
                    <option value="ict_ch1">ICT: Chapter 1 (Info & Tech)</option>
                    <option value="ict_ch2">ICT: Chapter 2 (Security)</option>
                </optgroup>
                <optgroup label="Main Subjects">
                    <option value="bng_all">Bangla (সাহিত্য ও ব্যাকরণ)</option>
                    <option value="eng_all">English Grammar Pro</option>
                    <option value="math_all">General Math Mastery</option>
                </optgroup>
            </select>
            <button id="st_btn" onclick="goEx()" class="btn-mega btn-action shadow" disabled>UNLOCK WITH 5 CREDITS 🔒</button>
            <div class="text-center mt-4">
                <script type="text/javascript">
                    atOptions = {{ 'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {{}} }};
                </script>
                <script type="text/javascript" src="https://potterynaggingformerly.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
            </div>
        </div>
    </div>
    <script>
        let credits = localStorage.getItem('ssc_hub_cr') || 0;
        document.getElementById('cr_val').innerText = credits;
        if(credits >= 5) {{
            document.getElementById('st_btn').disabled = false;
            document.getElementById('st_btn').innerHTML = "🚀 START FULL EXAM (30 MCQ)";
        }}
        function addCr() {{
            window.open('{SMARTLINK_1}', '_blank');
            setTimeout(() => {{
                localStorage.setItem('ssc_hub_cr', parseInt(credits) + 10);
                location.reload();
            }}, 3000);
        }}
        function goEx() {{
            localStorage.setItem('ssc_hub_cr', credits - 5);
            window.location.href = '/exam?topic=' + document.getElementById('sub_list').value;
        }}
    </script>
    """)

@app.route('/exam')
def exam():
    topic = request.args.get('topic', 'ict_ch1')
    raw_qs = DB.get(topic, [])
    # ৩০টি র‍্যান্ডমলি সিলেক্ট করা
    random.shuffle(raw_qs)
    selected = raw_qs[:30]

    q_html = ""
    for i, (q, c, w1, w2, w3) in enumerate(selected):
        opts = [c, w1, w2, w3]
        random.shuffle(opts)
        q_html += f"""
        <div class="q-container">
            <h5 class="fw-bold mb-4">{i+1}. {q}</h5>
            {"".join([f'<label class="opt-label"><input type="radio" name="q{i}" value="{o}" data-ans="{c}"> <span>{o}</span></label>' for o in opts])}
        </div>
        """
        if (i+1) % 5 == 0:
            q_html += f'<div class="text-center mb-4 bg-white p-3 rounded shadow-sm border">-- SPONSORED CONTENT --</div>'

    return render_template_string(STYLE + f"""
    <div class="sticky-header shadow-sm">
        <div class="container d-flex justify-content-between align-items-center">
            <h5 class="m-0 text-primary fw-bold uppercase"><i class="fas fa-file-alt"></i> SSC: {topic.replace('_', ' ')}</h5>
            <div class="badge bg-danger p-2 px-3"><i class="fas fa-clock"></i> 20:00 MIN</div>
        </div>
    </div>
    <div class="container mt-4" style="max-width: 850px;">
        {q_html}
        <button onclick="submitExam()" class="btn-mega btn-action mb-5 shadow-lg"><i class="fas fa-check-double"></i> FINISH & SEE GRADE</button>
    </div>
    <div id="loader" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:20%;">
        <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;"></div>
        <h2 class="mt-4 fw-bold">Generating Your SSC Scoreboard...</h2>
    </div>
    <script>
        function submitExam() {{
            let score = 0;
            document.querySelectorAll('.q-container').forEach(container => {{
                let selected = container.querySelector('input:checked');
                if(selected && selected.value === selected.getAttribute('data-ans')) score++;
            }});
            localStorage.setItem('last_score', score);
            window.open('{SMARTLINK_2}', '_blank');
            document.getElementById('loader').style.display = 'block';
            setTimeout(() => {{ window.location.href = '/result'; }}, 6000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 550px;">
        <div class="glass-card shadow-lg p-5">
            <h2 class="fw-bold mb-4">Official Exam Result</h2>
            <div class="p-4 bg-light rounded-4 mb-4 border border-primary border-dashed">
                <h6 class="text-muted text-uppercase mb-2">Total Correct Answers</h6>
                <h1 class="display-1 fw-bold text-primary" id="score_val">0</h1>
                <p class="h4">Out of 30</p>
            </div>
            <div id="gradebox" class="alert p-3 fw-bold h5"></div>
            <hr>
            <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn-mega btn-reward mt-2"><i class="fas fa-file-certificate"></i> CLAIM SSC CERTIFICATE</button>
            <a href="/" class="d-block mt-4 text-decoration-none text-muted fw-bold">← Retake New Exam</a>
        </div>
    </div>
    <script>
        let score = localStorage.getItem('last_score') || 0;
        document.getElementById('score_val').innerText = score;
        let perc = (score / 30) * 100;
        let gb = document.getElementById('gradebox');
        if(perc >= 80) {{ gb.innerText = "GRADE: A+ (Outstanding)"; gb.classList.add('alert-success'); }}
        else if(perc >= 60) {{ gb.innerText = "GRADE: A- (Great)"; gb.classList.add('alert-info'); }}
        else if(perc >= 33) {{ gb.innerText = "GRADE: Passed"; gb.classList.add('alert-warning'); }}
        else {{ gb.innerText = "GRADE: Failed (Try Again)"; gb.classList.add('alert-danger'); }}
        
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK_1}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=False)
