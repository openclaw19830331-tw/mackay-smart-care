
import os
import re

def parse_md(text):
    # 提取日期 (格式 date: YYYY-MM-DD)
    date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', text)
    date_str = date_match.group(1) if date_match else "未標示日期"
    
    # 移除 YAML 區塊與標籤，只留內容
    content = re.sub(r'---.*?---', '', text, flags=re.DOTALL)
    
    # 簡單渲染
    content = re.sub(r'# (.*)', r'<h2>\1</h2>', content)
    content = content.replace('\n', '<br>')
    
    return {
        "date": date_str,
        "html": f'<div class="post"><small style="color:#6e7681;">發佈日期: {date_str}</small>{content}</div>'
    }

template = open("/home/hermes/repo/template.html", "r").read()
content_dir = "/home/hermes/repo/content"

articles = []
for f_name in [f for f in os.listdir(content_dir) if f.endswith(".md")]:
    with open(os.path.join(content_dir, f_name), "r") as f:
        articles.append(parse_md(f.read()))

# 按日期排序 (最新在前)
articles.sort(key=lambda x: x['date'], reverse=True)

posts_html = "".join([a['html'] for a in articles])

svg = '<svg width="200" height="200"><circle cx="100" cy="100" r="50" fill="none" stroke="#00f2ff"/><text x="100" y="105" fill="#00f2ff" text-anchor="middle">SKILL TREE</text></svg>'

final = template.replace("<!-- CONTENT_START -->", posts_html).replace("<!-- SVG_SKILL_TREE -->", svg)

with open("/home/hermes/repo/index.html", "w") as f:
    f.write(final)
