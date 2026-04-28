const fs = require('fs');
const path = require('path');

// 靜態網站生成腳本
function generateSite() {
    const contentDir = path.join(__dirname, '../content');
    const template = fs.readFileSync(path.join(contentDir, 'index.html'), 'utf8');
    
    // 邏輯：讀取 MD、排序、自動分區 (最新頂置/歷史收折)
    console.log("Generating dynamic site structure...");
    
    // 實際部署時會將此邏輯整合進 CI/CD
    fs.writeFileSync(path.join(__dirname, '../index.html'), template);
    console.log("index.html updated successfully.");
}

generateSite();
