import os
import requests
import random
import json
from datetime import datetime

# إعدادات
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BLOG_DIR = "blog"
SITEMAP_FILE = "sitemap.xml"
INDEX_FILE = "blog/index.json"

TOPICS = [
    # AI & Tech
    "AI Startup Ideas 2026", "AI Tools for Entrepreneurs", "AI in Healthcare Startups",
    "How AI is Changing SaaS", "Best AI Productivity Tools for Founders",
    "AI for Small Business Automation", "Machine Learning Startup Ideas",
    "How to Build an AI-Powered SaaS", "AI in Education Startups",
    "Voice AI Startup Opportunities", "AI in Legal Tech", "AI in Real Estate Tech",
    "Computer Vision Startup Ideas", "Generative AI Business Models",
    "AI Customer Support Tools for Startups",
    # Domains & Branding
    "Benefits of .com Domains", "Why Short Domains are Valuable",
    "How to Pick a Brandable Domain Name", "Top Domain Investment Strategies",
    "Passive Income with Domain Flipping", "How to Value a Premium Domain",
    "Domain Flipping Guide for Beginners", "Best Niches for Domain Investing 2026",
    "How to Sell a Domain on Sedo", "Expired Domains as Investment Opportunities",
    "Why Brandable Domains Beat Keyword Domains", "Domain Portfolio Management Tips",
    # SaaS & Startups
    "SaaS Growth Strategies", "Best SaaS Business Models",
    "How to Launch a Tech Startup in 2026", "How to Brand Your Tech Company",
    "No-Code Tools for Entrepreneurs", "Micro SaaS Ideas for Solo Founders",
    "How to Find Your First SaaS Customers", "Bootstrapping a SaaS in 2026",
    "SaaS Pricing Strategies That Work", "B2B SaaS Startup Ideas",
    "How to Validate a Startup Idea Fast", "Building a SaaS MVP in 30 Days",
    "Top Startup Niches to Watch in 2026", "How to Get Your First 100 SaaS Users",
    "Vertical SaaS Opportunities in 2026",
    # FinTech & Investment
    "Future of FinTech Innovation", "FinTech Startup Ideas 2026",
    "How Blockchain is Changing Finance", "Digital Banking Startup Opportunities",
    "Embedded Finance Startup Ideas", "InsurTech Startup Opportunities",
    "WealthTech Startup Ideas", "Open Banking Opportunities for Startups",
    # Other Niches
    "HealthTech Startup Ideas 2026", "EdTech Startup Opportunities",
    "CleanTech and GreenTech Startups", "LegalTech Startup Opportunities",
    "HRTech Startup Ideas", "Creator Economy Business Ideas",
    "Newsletter Business Ideas for 2026", "Remote Work Tools Startup Ideas",
    "Cybersecurity Startup Ideas", "Developer Tools Startup Opportunities",
    "MarTech Startup Ideas for 2026", "PropTech Startup Opportunities"
]

def get_unused_topic():
    """يختار topic مش مستخدم فالمقالات الأخيرة"""
    used_topics = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
                used_topics = [p["title"] for p in posts]
            except:
                pass
    available = [t for t in TOPICS if t not in used_topics]
    if not available:
        available = TOPICS  # إذا كل شي اتستخدم نرجعو للكل
    return random.choice(available)

def generate_article():
    topic = get_unused_topic()
    prompt = f"""
    Write a professional blog post in HTML for a website called TechieVest.
    Topic: {topic}
    Requirements:
    - Use <h2> and <h3> for subheadings.
    - Style it with a dark theme (background: #050810, text: #e2e8f0).
    - Include a link back to 'https://techievest.com' calling it 'Premium Domain For Sale'.
    - Keep it SEO-friendly (600+ words).
    - Return ONLY the HTML body content, no <html>, <head>, or <body> tags.
    """

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    print("API Response:", result)  # باش نشوفو شنو رجع
    article_html = result['choices'][0]['message']['content']

    # حفظ المقال
    os.makedirs(BLOG_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{BLOG_DIR}/post-{date_str}.html"

    # استخراج أول paragraph كـ excerpt
    excerpt = ""
    try:
        start = article_html.index("<p>") + 3
        end = article_html.index("</p>", start)
        excerpt = article_html[start:end][:180].strip() + "..."
    except:
        excerpt = f"Read our latest article on {topic}."

    full_html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>{topic} – TechieVest</title>
<meta name='description' content='{excerpt[:150]}'>
<link href='https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap' rel='stylesheet'>
<style>
  :root {{ --bg:#050810; --accent:#6ee7f7; --text:#e2e8f0; --muted:#64748b; --border:rgba(110,231,247,0.12); }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'DM Sans',sans-serif; line-height:1.8; }}
  nav {{ display:flex; align-items:center; justify-content:space-between; padding:18px 48px; border-bottom:1px solid var(--border); background:rgba(5,8,16,0.9); backdrop-filter:blur(20px); position:sticky; top:0; z-index:100; }}
  .nav-logo {{ font-family:'Syne',sans-serif; font-weight:800; font-size:20px; color:var(--accent); text-decoration:none; }}
  .nav-logo span {{ color:var(--text); }}
  .back {{ font-size:13px; color:var(--muted); text-decoration:none; }}
  .back:hover {{ color:var(--accent); }}
  .wrapper {{ max-width:760px; margin:0 auto; padding:64px 32px; }}
  .post-tag {{ font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:var(--accent); margin-bottom:16px; }}
  h1 {{ font-family:'Syne',sans-serif; font-size:clamp(28px,5vw,44px); font-weight:800; letter-spacing:-1.5px; color:#fff; margin-bottom:16px; line-height:1.15; }}
  .post-meta {{ font-size:13px; color:var(--muted); margin-bottom:48px; padding-bottom:24px; border-bottom:1px solid var(--border); }}
  .content h2 {{ font-family:'Syne',sans-serif; font-size:24px; font-weight:700; color:#fff; margin:40px 0 12px; }}
  .content h3 {{ font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:var(--accent); margin:28px 0 10px; }}
  .content p {{ color:#94a3b8; font-size:15px; margin-bottom:20px; }}
  .content a {{ color:var(--accent); text-decoration:none; }}
  .content a:hover {{ text-decoration:underline; }}
  footer {{ border-top:1px solid var(--border); padding:32px; text-align:center; font-size:13px; color:var(--muted); margin-top:80px; }}
  footer a {{ color:var(--accent); text-decoration:none; margin:0 10px; }}
  @media(max-width:640px) {{ nav {{ padding:16px 20px; }} .wrapper {{ padding:48px 20px; }} }}
</style>
</head>
<body>
<nav>
  <a href='../index.html' class='nav-logo'>Techie<span>Vest</span></a>
  <a href='../index.html' class='back'>← Back to Home</a>
</nav>
<div class='wrapper'>
  <div class='post-tag'>Tech Insights</div>
  <h1>{topic}</h1>
  <div class='post-meta'>Published {datetime.now().strftime("%B %d, %Y")} &nbsp;·&nbsp; TechieVest Editorial</div>
  <div class='content'>
    {article_html}
  </div>
</div>
<footer>
  © 2026 TechieVest.com &nbsp;·&nbsp;
  <a href='../privacy-policy.html'>Privacy Policy</a>
  <a href='../terms.html'>Terms of Use</a>
  <a href='../contact.html'>Contact</a>
</footer>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_html)

    return filename, topic, excerpt, date_str

def update_index_json(filename, topic, excerpt, date_str):
    """يحدث blog/index.json بالمقال الجديد"""
    posts = []

    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
            except:
                posts = []

    # إضافة المقال الجديد في الأول
    posts.insert(0, {
        "title": topic,
        "file": filename,
        "excerpt": excerpt,
        "date": datetime.now().strftime("%B %d, %Y"),
        "date_str": date_str
    })

    # نحتفظ بآخر 20 مقال فقط
    posts = posts[:20]

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def update_sitemap(new_file):
    url = f"https://techievest.com/{new_file}"
    if not os.path.exists(SITEMAP_FILE):
        with open(SITEMAP_FILE, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>')

    with open(SITEMAP_FILE, "r") as f:
        lines = f.readlines()

    lines.insert(-1, f"  <url><loc>{url}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>\n")

    with open(SITEMAP_FILE, "w") as f:
        f.writelines(lines)

def post_to_twitter(topic, excerpt, filename):
    """ينشر tweet عند كل مقال جديد"""
    try:
        import tweepy

        client = tweepy.Client(
            consumer_key=os.getenv("X_API_KEY"),
            consumer_secret=os.getenv("X_API_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_SECRET")
        )

        post_url = f"https://techievest.com/{filename}"
        tweet = f"🚀 {topic}\n\n{excerpt[:200]}...\n\n🔗 {post_url}\n\n#TechStartup #SaaS #AI #DomainInvesting"

        # Twitter max 280 chars
        if len(tweet) > 280:
            tweet = f"🚀 {topic}\n\n🔗 {post_url}\n\n#TechStartup #SaaS #AI"

        client.create_tweet(text=tweet)
        print(f"✅ Tweet posted: {topic}")

    except Exception as e:
        print(f"⚠️ Twitter error: {e}")

if __name__ == "__main__":
    filename, topic, excerpt, date_str = generate_article()
    update_index_json(filename, topic, excerpt, date_str)
    update_sitemap(filename)
    post_to_twitter(topic, excerpt, filename)
    print(f"✅ Success: {filename} generated.")
