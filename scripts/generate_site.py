import re
import os
import datetime

def clean_hermes_line_numbers(content):
    return re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)

def md_to_html_simple(md_text):
    html = md_text
    html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^- \[(.*)\]\((.*)\)', r'<li><a href="\2" style="color:#00f2ff; text-decoration:none;">\1</a></li>', html, flags=re.MULTILINE)
    html = re.sub(r'^- (.*)', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = html.replace('\n', '<br>')
    return html

def generate():
    repo_dir = "/home/hermes/repo"
    template_path = os.path.join(repo_dir, "template.html")
    content_dir = os.path.join(repo_dir, "content")
    trends_path = os.path.join(content_dir, "trends/latest.md")
    output_path = os.path.join(repo_dir, "index.html")

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 1. 抓取最新的 3 篇專題文章
    article_files = [f for f in os.listdir(content_dir) if f.startswith("article_") and f.endswith(".md")]
    article_files.sort(key=lambda x: os.path.getmtime(os.path.join(content_dir, x)), reverse=True)
    
    top_articles_html = ""
    for f_name in article_files[:3]:
        with open(os.path.join(content_dir, f_name), 'r', encoding='utf-8') as f:
            md = clean_hermes_line_numbers(f.read())
            top_articles_html += f"<div class='hero-section' style='margin-bottom:20px;'>{md_to_html_simple(md)}</div>"

    # 2. 處理趨勢
    if os.path.exists(trends_path):
        with open(trends_path, 'r', encoding='utf-8') as f:
            trends_md = clean_hermes_line_numbers(f.read())
        trends_html = md_to_html_simple(trends_md)
    else:
        trends_html = "暫無最新趨勢數據"

    # 3. 注入模板
    # 這裡我們將 index.html 的 hero-section 替換成多篇文章
    final_html = template.replace('<div class="hero-section">', '<div id="articles-container">')
    final_html = final_html.replace('<!-- CONTENT_START -->', top_articles_html)
    final_html = final_html.replace('<!-- CONTENT_END -->', f"<div class='hero-section'><h2>📡 趨勢監測頻道</h2>{trends_html}</div>")
    
    # SVG 保持不變
    svg_skill_tree = """    <svg width="250" height="250" viewBox="0 0 250 250" style="display: block; margin: auto;">
        <!-- 主架構：科技與長照的融合 -->
        <circle cx="125" cy="125" r="40" fill="none" stroke="#00f2ff" stroke-width="2" stroke-dasharray="4 4"/>
        <text x="125" y="130" fill="#ffffff" font-size="12" text-anchor="middle" font-weight="bold">馬偕智慧科技</text>
        
        <!-- 節點：AI 應用 -->
        <line x1="125" y1="85" x2="125" y2="40" stroke="#00f2ff" stroke-width="2"/>
        <circle cx="125" cy="35" r="20" fill="#161b22" stroke="#00f2ff" stroke-width="2"/>
        <text x="125" y="38" fill="#00f2ff" font-size="10" text-anchor="middle">AI 應用</text>
        
        <!-- 節點：長照知識 -->
        <line x1="165" y1="125" x2="210" y2="125" stroke="#00f2ff" stroke-width="2"/>
        <circle cx="225" cy="125" r="20" fill="#161b22" stroke="#00f2ff" stroke-width="2"/>
        <text x="225" y="128" fill="#00f2ff" font-size="10" text-anchor="middle">長照知識</text>
        
        <!-- 節點：自動化 -->
        <line x1="85" y1="125" x2="40" y2="125" stroke="#00f2ff" stroke-width="2"/>
        <circle cx="25" cy="125" r="20" fill="#161b22" stroke="#00f2ff" stroke-width="2"/>
        <text x="25" y="128" fill="#00f2ff" font-size="10" text-anchor="middle">自動化</text>
        
        <!-- 節點：產學連結 -->
        <line x1="125" y1="165" x2="125" y2="210" stroke="#00f2ff" stroke-width="2"/>
        <circle cx="125" cy="225" r="20" fill="#161b22" stroke="#00f2ff" stroke-width="2"/>
        <text x="125" y="228" fill="#00f2ff" font-size="10" text-anchor="middle">產學連結</text>
    </svg>"""
    final_html = final_html.replace("<!-- SVG_SKILL_TREE -->", svg_skill_tree)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully generated site with {len(article_files[:3])} articles.")

if __name__ == "__main__":
    generate()
