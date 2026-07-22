# convert_md_to_html · 将学习资料 .md 转为网页 HTML 的完整流程

## 概述

将 Markdown 学习资料转为可直接部署到 Netlify 的网页版（兼容中文、代码高亮、目录、搜索、卡片速记） 的标准化工作流。

## 工作流

### 1. 准备材料
- 源文件：`docs/*.md`（所有笔记体、面渣、卡片、频率页）
- 输出目标：`index.html`（根目录）和 `public/index.html`（Docsify 站点）

### 2. 转换流程（Prompt）

使用以下结构提示词进行转换：

```prompt
请将下面给定的 Markdown 学习资料文件转换为 HTML 格式的网页版本。

要求：
1. 使用 Docsify 的 vue 主题风格（header、sidebar、nav、footer、code highlight、mermaid 兼容）
2. 保持所有链接、目录、卡片速记格式
3. 代码块添加高亮（highlight.js 或 inline CSS）
4. 添加 favicon 和 logo 图标
5. 增加版本号和更新日期
6. 保持中文完整性

输入文件：
{file_content}

输出格式：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta ...>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css" />
  <style> ... </style>
</head>
<body>
  <div id="app">...</div>
  <script> ... $docsify 配置 ... </script>
</body>
</html>

请输出完整 HTML 内容，代码块用 ```html 包裹。
```

### 3. 批量转换命令
```bash
python tools/convert_md_to_html.py --input docs/ --output index.html
# 或者直接调用 index.html 生成
```

### 4. 测试
- 本地：`npx serve -l 3000`
- 部署：Netlify（Publish directory = . ）

### 5. 维护
- 所有新 md 文件都通过此流程更新 index.html
- 每次生成后运行 `python tools/check_md_links.py`

## 相关文件
- `index.html`（根）
- `docs/skills/convert_md_to_html.skill.md`（本 skill）
- `tools/convert_md_to_html.py`（可选批量脚本）

[← 首页](./README.md)
