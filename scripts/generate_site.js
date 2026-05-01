const fs = require('fs');
const path = require('path');

function cleanContent(content) {
    return content.replace(/^\d+\|/gm, '');
}

function generate() {
    const postsDir = '/home/hermes/repo/content/fb_posts';
    const posts = fs.readdirSync(postsDir)
        .filter(file => file.endsWith('.md'))
        .sort().reverse() // 最新的在前面
        .map(file => {
            const content = fs.readFileSync(path.join(postsDir, file), 'utf8');
            return `<div class="post"><h3>${file.replace('.md', '')}</h3><p>${cleanContent(content).replace(/\n/g, '<br>')}</p></div>`;
        }).join('<hr>');

    const template = fs.readFileSync('/home/hermes/repo/template.html', 'utf8');
    const finalHtml = template
        .replace('<div id="hero-content">載入中...</div>', `<div class="hero-content">${posts}</div>`)
        .replace('<div id="archive-list"></div>', '<div class="archive-list"><ul><li>2026/04/29 - 系統正式上線</li></ul></div>');

    fs.writeFileSync('/home/hermes/repo/index.html', finalHtml);
}
generate();
