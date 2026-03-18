from flask import Flask, request, render_template_string
import sqlite3
import datetime

app = Flask(__name__)

# ---------------- DATABASE ---------------- #
def init_db():
    conn = sqlite3.connect("growmore.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, message TEXT, date TEXT)""")
    conn.commit()
    conn.close()

init_db()

# ---------------- SHARED UI COMPONENTS ---------------- #
HEADER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grow More | Premium Digital Marketing</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #020617; color: white; scroll-behavior: smooth; }
        .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .grad-text { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .service-card:hover { border-color: #38bdf8; transform: translateY(-5px); transition: all 0.3s ease; }
        .price-card:hover { border-color: #38bdf8; transform: scale(1.02); transition: all 0.3s ease; }
    </style>
</head>
<body>
    <nav class="fixed w-full z-50 glass py-4 px-[10%] flex justify-between items-center">
        <h2 class="text-2xl font-extrabold tracking-tighter">GROW<span class="text-sky-400">MORE</span></h2>
        <div class="hidden md:flex space-x-8 font-medium text-sm uppercase tracking-widest text-gray-300">
            <a href="/" class="hover:text-sky-400 transition">Home</a>
            <a href="/services" class="hover:text-sky-400 transition">Services</a>
            <a href="/pricing" class="hover:text-sky-400 transition">Pricing</a>
            <a href="/dashboard" class="hover:text-sky-400 transition text-xs border border-white/20 px-3 py-1 rounded">CRM</a>
            <button onclick="window.location.href='/#contact'" class="bg-sky-500 px-5 py-2 rounded-full text-black font-bold text-xs hover:bg-sky-400 transition">Get Started</button>
        </div>
    </nav>
"""

FOOTER_HTML = """
    <footer class="py-10 text-center text-gray-500 border-t border-gray-800 mt-20">
        <p>&copy; 2026 Grow More Agency. Elevating Brands Globally.</p>
    </footer>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>AOS.init({ duration: 1000, once: true });</script>
</body>
</html>
"""

# ---------------- ROUTES ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name, email, message = request.form.get("name"), request.form.get("email"), request.form.get("message")
        conn = sqlite3.connect("growmore.db")
        c = conn.cursor()
        c.execute("INSERT INTO leads(name,email,message,date) VALUES(?,?,?,?)", (name, email, message, str(datetime.date.today())))
        conn.commit()
        conn.close()

    hero = """
    <section class="relative h-screen flex items-center justify-center text-center px-6">
        <div class="absolute inset-0 z-0 opacity-30">
            <img src="https://images.unsplash.com/photo-1551434678-e076c223a692" class="w-full h-full object-cover">
        </div>
        <div class="relative z-10" data-aos="zoom-in">
            <span class="text-sky-400 font-bold tracking-widest text-sm uppercase">Data-Driven Growth</span>
            <h1 class="text-6xl md:text-8xl font-extrabold mb-6 mt-2">Scale <span class="grad-text">Faster</span></h1>
            <p class="text-gray-400 max-w-xl mx-auto mb-10 text-lg">We combine elite performance marketing with high-end creative design to explode your revenue.</p>
            <div class="flex flex-wrap justify-center gap-4">
                <a href="/services" class="bg-white text-black px-10 py-4 rounded-xl font-bold hover:bg-sky-400 transition">Explore Services</a>
                <a href="/pricing" class="glass px-10 py-4 rounded-xl font-bold hover:bg-white/10 transition">View Plans</a>
            </div>
        </div>
    </section>
    
    <section id="contact" class="py-24 px-[10%]" data-aos="fade-up">
        <div class="max-w-4xl mx-auto glass p-12 rounded-3xl">
            <h2 class="text-3xl font-bold mb-2">Work with Us</h2>
            <p class="text-gray-400 mb-8">Ready to grow? Fill out the form and our experts will reach out.</p>
            <form method="POST" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <input name="name" required placeholder="Name" class="bg-white/5 border border-white/10 p-4 rounded-xl focus:outline-none focus:border-sky-500">
                <input name="email" required placeholder="Email" class="bg-white/5 border border-white/10 p-4 rounded-xl focus:outline-none focus:border-sky-500">
                <textarea name="message" required placeholder="Tell us about your project goals..." class="md:col-span-2 bg-white/5 border border-white/10 p-4 rounded-xl h-32 focus:outline-none focus:border-sky-500"></textarea>
                <button type="submit" class="bg-sky-500 py-4 rounded-xl text-black font-bold uppercase tracking-widest hover:bg-sky-400">Send Inquiry</button>
            </form>
        </div>
    </section>
    """
    return render_template_string(HEADER_HTML + hero + FOOTER_HTML)

@app.route("/services")
def services():
    all_services = [
        {"title": "Social Media Marketing", "desc": "Strategic growth on Instagram, Facebook, and LinkedIn to build authority.", "icon": "📱"},
        {"title": "Paid Advertising", "desc": "High-conversion Google & Meta Ads tailored for maximum ROI and lead flow.", "icon": "🎯"},
        {"title": "SEO Optimization", "desc": "Dominate search results and capture organic traffic with data-driven SEO.", "icon": "🚀"},
        {"title": "Web Design & Dev", "desc": "Custom, high-performance websites built to convert visitors into customers.", "icon": "💻"},
        {"title": "Content Marketing", "desc": "Storytelling that resonates. We create content that sells your brand value.", "icon": "✍️"},
        {"title": "Branding & Creative", "desc": "Premium visual identities and creative assets that stand out in the crowd.", "icon": "🎨"},
        {"title": "Lead Generation", "desc": "Custom automated funnels designed to fill your pipeline with qualified leads.", "icon": "📊"}
    ]
    
    cards = "".join([f'<div class="glass p-8 rounded-2xl service-card border border-white/5" data-aos="fade-up"><div class="text-4xl mb-4">{s["icon"]}</div><h3 class="text-xl font-bold mb-3 text-sky-400">{s["title"]}</h3><p class="text-gray-400 text-sm leading-relaxed">{s["desc"]}</p></div>' for s in all_services])

    content = f"""<div class="pt-32 px-[10%] min-h-screen"><div class="text-center mb-20" data-aos="fade-down"><h1 class="text-5xl font-extrabold mb-4 grad-text">Our Services</h1><p class="text-gray-400 max-w-2xl mx-auto">Full-stack marketing solutions built for the modern digital landscape.</p></div><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">{cards}</div></div>"""
    return render_template_string(HEADER_HTML + content + FOOTER_HTML)

@app.route("/pricing")
def pricing():
    # Package Data
    plans = [
        {
            "name": "Starter",
            "price": "₹15,000",
            "desc": "Perfect for small businesses starting their digital journey.",
            "features": ["Social Media (8 Posts/mo)", "Basic SEO Audit", "1 Ad Campaign Setup", "Email Support"],
            "popular": False
        },
        {
            "name": "Intermediate",
            "price": "₹35,000",
            "desc": "The Pro package for brands ready to scale aggressively.",
            "features": ["Social Media (15 Posts/mo)", "On-Page SEO", "Meta & Google Ads", "Monthly Strategy Call"],
            "popular": True
        },
        {
            "name": "Expert",
            "price": "₹75,000",
            "desc": "Full market domination for established enterprises.",
            "features": ["Full Content Production", "Technical SEO & Backlinks", "Advanced Ad Management", "Dedicated Manager"],
            "popular": False
        }
    ]

    plan_cards = ""
    for p in plans:
        border_class = "border-sky-500 shadow-lg shadow-sky-500/20" if p['popular'] else "border-white/10"
        badge = '<span class="bg-sky-500 text-black text-[10px] font-bold px-3 py-1 rounded-full absolute -top-3 right-6">MOST POPULAR</span>' if p['popular'] else ""
        
        features_list = "".join([f'<li class="flex items-center gap-2 text-gray-400 text-sm mb-3"><span>✅</span> {f}</li>' for f in p['features']])
        
        plan_cards += f"""
        <div class="glass p-10 rounded-3xl relative price-card border {border_class}" data-aos="fade-up">
            {badge}
            <h3 class="text-xl font-bold mb-1">{p['name']}</h3>
            <div class="text-4xl font-extrabold mb-4">{p['price']}<span class="text-sm text-gray-500">/mo</span></div>
            <p class="text-gray-400 text-xs mb-8">{p['desc']}</p>
            <ul class="mb-10">{features_list}</ul>
            <button onclick="window.location.href='/#contact'" class="w-full py-4 rounded-xl font-bold {'bg-sky-500 text-black hover:bg-sky-400' if p['popular'] else 'border border-white/20 hover:bg-white/10'} transition">Choose Plan</button>
        </div>
        """

    content = f"""
    <div class="pt-32 px-[10%] min-h-screen">
        <div class="text-center mb-16" data-aos="fade-down">
            <h1 class="text-5xl font-extrabold mb-4 grad-text">Tailored Pricing</h1>
            <p class="text-gray-400 max-w-xl mx-auto">Choose a plan that fits your growth stage. No hidden fees.</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {plan_cards}
        </div>
    </div>
    """
    return render_template_string(HEADER_HTML + content + FOOTER_HTML)

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("growmore.db")
    leads = conn.cursor().execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    conn.close()
    rows = "".join([f'<tr class="border-t border-white/5"><td class="p-4 font-bold">{l[1]}</td><td class="p-4 text-sky-400">{l[2]}</td><td class="p-4 text-gray-500 text-xs">{l[4]}</td></tr>' for l in leads])
    content = f"""<div class="pt-32 px-[10%] min-h-screen"><h1 class="text-4xl font-bold mb-8 grad-text">Agency Dashboard</h1><div class="glass rounded-2xl overflow-hidden"><table class="w-full text-left"><thead class="bg-white/10 uppercase text-xs tracking-widest"><tr><th class="p-4">Client Name</th><th class="p-4">Email Address</th><th class="p-4">Date Recieved</th></tr></thead><tbody>{rows if rows else '<tr><td colspan="3" class="p-10 text-center text-gray-500">No leads yet.</td></tr>'}</tbody></table></div></div>"""
    return render_template_string(HEADER_HTML + content + FOOTER_HTML)

if __name__ == "__main__":
    app.run(debug=True)