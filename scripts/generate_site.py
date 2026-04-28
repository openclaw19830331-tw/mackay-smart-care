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
    svg_skill_tree = """<svg width="200" height="200" viewBox="0 0 200 200" style="display: block; margin: auto;"><polygon points="100,20 180,80 150,170 50,170 20,80" fill="none" stroke="#00f2ff" stroke-width="2"/><polygon points="100,40 160,85 140,150 60,150 40,85" fill="rgba(0, 242, 255, 0.3)" stroke="#00f2ff" stroke-width="1"/><text x="100" y="15" fill="#00f2ff" font-size="10" text-anchor="middle">AI 應用</text><text x="190" y="80" fill="#00f2ff" font-size="10" text-anchor="start">長照知識</text><text x="100" y="190" fill="#00f2ff" font-size="10" text-anchor="middle">自動化</text></svg>"""
    final_html = final_html.replace("<!-- SVG_SKILL_TREE -->", svg_skill_tree)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully generated site with {len(article_files[:3])} articles.")

if __name__ == "__main__":
    generate()
