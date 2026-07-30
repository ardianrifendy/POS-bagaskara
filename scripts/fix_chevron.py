with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('class="acc-chevron"> </span>', 'class="acc-chevron">▼</span>')

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
