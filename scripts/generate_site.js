const fs = require('fs');
const path = require('path');

function cleanContent(content) {
    // 移除 hermes_tools 產生的行號 (例如: "1|內容")
    return content.replace(/^\d+\|/gm, '');
}

function generate() {
    const rawContent = fs.readFileSync('/home/hermes/repo/content/article1.md', 'utf8');
    const cleanBody = cleanContent(rawContent);
    const template = fs.readFileSync('/home/hermes/repo/index.html', 'utf8');

    // 將內容注入並確保 CSS 生效
    const finalHtml = template
        .replace('<div id="hero-content">載入中...</div>', `<div class="hero-content">${cleanBody.replace(/\n/g, '<br>')}</div>`)
        .replace('<div id="archive-list"></div>', '<div class="archive-list"><ul><li>2026/04/29 - 系統正式上線</li></ul></div>');

    fs.writeFileSync('/home/hermes/repo/index.html', finalHtml);
}
generate();
