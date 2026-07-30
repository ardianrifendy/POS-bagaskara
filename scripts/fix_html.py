with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken chevron classes
html = html.replace('font-size: class="acc-chevron" 12px;">▼</span>', 'font-size: 12px;" class="acc-chevron">▼</span>')

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
