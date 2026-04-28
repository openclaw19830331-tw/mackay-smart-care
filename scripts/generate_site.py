import re
import os

def clean_hermes_line_numbers(content):
    # 移除 hermes_tools 讀檔時產生的 "數字|" 雜訊
    # 支持多種格式如 " 1|", "1|", "10|"
    return re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)

def md_to_html_simple(md_text):
    # 簡單標題處理
    html = md_text
    html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    # 處理列表
    html = re.sub(r'^- (.*)', r'<li>\1</li>', html, flags=re.MULTILINE)
    # 處理換行
    html = html.replace('\n', '<br>')
    return html

def generate():
    repo_dir = "/home/hermes/repo"
    template_path = os.path.join(repo_dir, "template.html")
    article_path = os.path.join(repo_dir, "content/article1.md")
    output_path = os.path.join(repo_dir, "index.html")

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 讀取並清理 Markdown
    with open(article_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()
    
    # 確保清理可能在讀取時已經存在的行號
    clean_md = clean_hermes_line_numbers(raw_md)
    content_html = md_to_html_simple(clean_md)

    # 注入模板
    final_html = template.replace("<!-- CONTENT_START -->", content_html)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print("Successfully generated clean index.html")

if __name__ == "__main__":
    generate()
