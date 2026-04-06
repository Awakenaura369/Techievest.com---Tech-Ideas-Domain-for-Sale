import os
import requests
import random
from datetime import datetime

# إعدادات
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BLOG_DIR = "blog"
SITEMAP_FILE = "sitemap.xml"

TOPICS = [
    "AI Startup Ideas 2026", "Benefits of .com Domains", "SaaS Growth Strategies",
    "How to Brand Your Tech Company", "Future of FinTech Innovation", 
    "Why Short Domains are Valuable", "AI Tools for Entrepreneurs"
]

def generate_article():
    topic = random.choice(TOPICS)
    prompt = f"""
    Write a professional blog post in HTML for a website called TechieVest.
    Topic: {topic}
    Requirements:
    - Use <h2> and <h3> for subheadings.
    - Style it with a dark theme (background: #050810, text: #e2e8f0).
    - Include a link back to 'https://techievest.com' calling it 'Premium Domain For Sale'.
    - Keep it SEO-friendly (600+ words).
    - Return ONLY the HTML body content.
    """
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    article_html = response.json()['choices'][0]['message']['content']
    
    # حفظ المقال
    os.makedirs(BLOG_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{BLOG_DIR}/post-{date_str}.html"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>{topic}</title><style>body{{background:#050810;color:#e2e8f0;font-family:sans-serif;padding:40px;line-height:1.6;max-width:800px;margin:auto}}a{{color:#6ee7f7}}</style></head><body>{article_html}</body></html>")
    
    return filename

def update_sitemap(new_file):
    url = f"https://techievest.com/{new_file}"
    with open(SITEMAP_FILE, "r") as f:
        lines = f.readlines()
    
    # إضافة الرابط قبل آخر سطر في Sitemap
    lines.insert(-1, f"  <url><loc>{url}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>\n")
    
    with open(SITEMAP_FILE, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    new_post = generate_article()
    update_sitemap(new_post)
    print(f"✅ Success: {new_post} generated.")
